from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from openeats.recipe.models import Recipe

from openeats.list.models import GroceryList,GroceryShared


class listViewsTestCase(TestCase):
    fixtures=['test_user_data.json', 'list_test_data.json', 'aisle_data.json',
        'test_friend_data.json', 'course_data.json', 'cuisine_data.json', 'recipe_data.json', 'ing_data.json']
    def setUp(self):
        self.client.login(username="testuser", password='password')

    def test_index(self):
        """test we get a list of grocery list for a giving user"""
        resp = self.client.get(reverse('grocery_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('glists' in resp.context)
        self.assertEqual([glist.pk for glist in resp.context['glists']], [1])

        #test if you are not logged in you get sent to the login page
        self.client.logout()
        resp = self.client.get(reverse('grocery_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/accounts/login/?next=/list/grocery/')

    def test_detail(self):
        """test we get a list and all of its items"""
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('list' in resp.context)
        list = resp.context['list']
        self.assertEqual(list.pk, 1)
        self.assertEqual(list.title, "test")
        self.assertEqual(list.items.count(), 2)
        items = list.items.all()
        self.assertEqual(items[0].item, '1 loaf bread')
        self.assertEqual(items[0].aisle.aisle, 'bakery')

        #make sure a non-existent list throws a 404
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testuser', 'slug':'test2'}))
        self.assertEqual(resp.status_code, 404)

        #make sure another user can't see someones list
        self.client.logout()
        self.client.login(username="testuser2", password="password")
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_list'))

    def test_post(self):
        """do a simple test to test the list edit form"""
        list = GroceryList.objects.get(pk=1)
        data = {
            'title':'test',
            'author':2,
            'items-TOTAL_FORMS': 1,
            'items-INITIAL_FORMS':0,
            'items-0-id': str(list.id),
            'items-0-item': '1 gallon milk',
            'items-0-aisle': 1,
            'items-1-item': '1 loaf bread',
            'items-1-aisle': 3,
            'items-2-item': '1 carton eggs',
            'items-2-aisle': 1,
        }

        self.assertEqual(list.items.count(), 2)
        resp = self.client.post(reverse('grocery_edit',kwargs={'user':'testuser', 'slug':'test'}), data)
        self.assertEqual(resp.status_code, 302)
        #FAIL
        self.assertRedirects(resp, reverse('grocery_show',kwargs={'user':'testuser', 'slug':'test'}))
        self.assertRedirects(resp, '/list/grocery/testuser/test/')

        self.assertEqual(list.items.count(), 3)

    def test_bad_post(self):
        """test that the grocery list form fails when it should"""

        #make sure a non-existent list can't be edited
        resp = self.client.post(reverse('grocery_edit',kwargs={'user':'testuser', 'slug':'test333'}))
        self.assertEqual(resp.status_code, 404)

        #send no data
        list = GroceryList.objects.get(pk=1)
        no_title = {
            'items-TOTAL_FORMS': 1,
            'items-INITIAL_FORMS':0,
            'items-0-id': str(list.id),
        }
        no_item = {
            'title':'test',
            'author':2,
            'items-TOTAL_FORMS': 1,
            'items-INITIAL_FORMS':0,
            'items-0-id': str(list.id),
        }

        resp = self.client.post(reverse('grocery_edit',kwargs={'user':'testuser', 'slug':'test'}),no_title)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "This field is required")

        resp = self.client.post(reverse('grocery_edit',kwargs={'user':'testuser', 'slug':'test'}),no_item)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['formset'].errors, [{'item': [u'This field is required.']}])

    def test_shared(self):
        """test sharing a list allows only the shared user to access the list"""
        user1 = User.objects.get(pk=2)
        user2 = User.objects.get(pk=3)
        self.assertEqual(user1.username, 'testuser')
        self.assertEqual(user2.username, 'testuser2')

        #test the users are friends
        self.assertTrue(user1.relationships.filter(username=user2.username))
        self.assertTrue(user2.relationships.filter(username=user1.username))

        #share the list to testuser2
        resp = self.client.post(reverse('grocery_share',kwargs={'user':'testuser', 'slug':'test'}),{'shared_to':3})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/list/grocery/testuser/test/')
        list = GroceryList.objects.get(pk=1)
        self.assertTrue(list.get_shared())
        self.assertEqual(list.get_shared_to(), user2)

        #test the custom save method to make sure that shared_by was automatically set to the primary user
        shared = GroceryShared.objects.get(pk=1)
        self.assertEqual(shared.shared_by, user1)

        #shared user should be able to access the list now
        self.client.logout()
        self.client.login(username='testuser2', password='password')
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('grocery_edit', kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 200)

        #shared user should not be able to delete the list
        resp = self.client.get(reverse('grocery_delete', kwargs={'id':list.id}))
        self.assertEqual(resp.status_code, 404)

        #shared user should be able to add something to the list
        self.test_post()

        #make sure someone else who the list is not shared to can't access the list
        self.client.logout()
        self.client.login(username='testuser3', password='password')
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('grocery_edit', kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)

        #test the shared user can unshare the list
        self.client.logout()
        self.client.login(username='testuser2', password='password')
        resp = self.client.post(reverse('grocery_unshare',kwargs={'user':'testuser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_list'))
        self.assertFalse(list.get_shared())

    def test_delete(self):
        """test that only the owner of a list can delete it"""

        #santity check make sure the list is owned by testuser
        list = GroceryList.objects.get(pk=1)
        self.assertEqual(list.author.username, 'testuser')

        # try deleting an list that doesn't exist should give you a 404
        resp = self.client.post(reverse('grocery_delete', kwargs={'id':10000}))
        self.assertEqual(resp.status_code, 404)

        #try deleting a grocery list that does not belong to the user should give a 404
        self.client.logout()
        self.client.login(username='testuser2', password='password')
        resp = self.client.post(reverse('grocery_delete', kwargs={'id':list.id}))
        self.assertEqual(resp.status_code, 404)

        #removing the list
        self.client.logout()
        self.client.login(username='testuser', password='password')
        resp = self.client.post(reverse('grocery_delete', kwargs={'id':list.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_list'))
        self.assertFalse(GroceryList.objects.filter(pk=1))

    def test_addRecipe(self):
        """test adding recipe ingredients to a list"""
        recipe = Recipe.objects.get(pk=1)
        list = GroceryList.objects.get(pk=1)

        #sanity check
        self.assertEqual(recipe.slug, 'tasty-chili')
        self.assertEqual(list.title, "test")
        self.assertEqual(list.items.count(), 2)
        self.assertFalse(GroceryList.objects.filter(pk=2))

        resp = self.client.post(reverse('grocery_addrecipe',kwargs={'recipe_slug':recipe.slug}),
            {'lists':1, 'recipe_id':recipe.id})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], '/list/grocery/edit/testuser/test/')

        #test we now have more items
        updated_list = GroceryList.objects.get(pk=1)
        self.assertEqual(updated_list.items.count(), 14)

        #test trying to do a recipe that does not exist
        resp = self.client.post(reverse('grocery_addrecipe',kwargs={'recipe_slug':'bad-recipe'}),
            {'lists':1, 'recipe_id':30000})
        self.assertEqual(resp.status_code, 404)

        #test creating a new list instead of adding to an existing list
        resp = self.client.post(reverse('grocery_addrecipe',kwargs={'recipe_slug':recipe.slug}),
            {'recipe_slug':recipe.slug, 'lists':0, 'recipe_id':recipe.id}, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(GroceryList.objects.get(pk=2))
        new_list = GroceryList.objects.get(pk=2)
        self.assertEqual(new_list.items.count(), 12)
