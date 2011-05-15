from django.test import TestCase
from django.core.urlresolvers import reverse
from list.models import GroceryList,GroceryShared
from django.contrib.auth.models import User

class listViewsTestCase(TestCase):
    fixtures=['test_user_data.json', 'list_test_data.json', 'aisle_data.json','test_friend_data.json']
    def setUp(self):
        self.client.login(username="testUser", password='password')

    def test_index(self):
        '''test we get a list of grocery list for a giving user'''
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
        '''test we get a list and all of its items'''
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('list' in resp.context)
        list = resp.context['list']
        self.assertEqual(list.pk, 1)
        self.assertEqual(list.title, "test")
        self.assertEqual(list.groceryitem_set.count(), 2)
        items = list.groceryitem_set.all()
        self.assertEqual(items[0].item, '1 loaf bread')
        self.assertEqual(items[0].aisle.aisle, 'bakery')

        #make sure a non-existent list throws a 404
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test2'}))
        self.assertEqual(resp.status_code, 404)

        #make sure another user can't see someones list
        self.client.logout()
        self.client.login(username="testUser2", password="password")
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_list'))

    def test_post(self):
        '''do a simple test to test the list edit form'''
        list = GroceryList.objects.get(pk=1)
        data = {
            'title':'test',
            'author':2,
            'groceryitem_set-TOTAL_FORMS': 1,
            'groceryitem_set-INITIAL_FORMS':0,
            'groceryitem_set-0-id': str(list.id),
            'groceryitem_set-0-item': '1 gallon milk',
            'groceryitem_set-0-aisle': 1,
            'groceryitem_set-1-item': '1 loaf bread',
            'groceryitem_set-1-aisle': 3,
            'groceryitem_set-2-item': '1 carton eggs',
            'groceryitem_set-2-aisle': 1,
        }

        self.assertEqual(list.groceryitem_set.count(), 2)
        resp = self.client.post(reverse('grocery_edit',kwargs={'user':'testUser', 'slug':'test'}), data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_show',kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(list.groceryitem_set.count(), 3)


    def test_shared(self):
        '''test sharing a list allows only the shared user to access the list'''
        user1 = User.objects.get(pk=2)
        user2 = User.objects.get(pk=3)
        self.assertEqual(user1.username, 'testUser')
        self.assertEqual(user2.username, 'testUser2')
       
        #test the users are friends
        self.assertTrue(user1.relationships.filter(username=user2.username))
        self.assertTrue(user2.relationships.filter(username=user1.username))

        #share the list to testUser2
        resp = self.client.post(reverse('grocery_share',kwargs={'user':'testUser', 'slug':'test'}),{'shared_to':3})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_show',kwargs={'user':'testUser', 'slug':'test'}))
        list = GroceryList.objects.get(pk=1)
        self.assertTrue(list.get_shared())
        self.assertEqual(list.get_shared_to(), user2)

        #test the custom save method to make sure that shared_by was automatically set to the primary user
        shared = GroceryShared.objects.get(pk=1)
        self.assertEqual(shared.shared_by, user1)

        #shared user should be able to access the list now
        self.client.logout()
        self.client.login(username='testUser2', password='password')
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('grocery_edit', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 200)

        #shared user should not be able to delete the list
        resp = self.client.get(reverse('grocery_delete', kwargs={'id':list.id}))
        self.assertEqual(resp.status_code, 404)

        #make sure someone else who the list is not shared to can't access the list
        self.client.logout()
        self.client.login(username='testUser3', password='password')
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('grocery_edit', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)

        #test the shared user can unshare the list
        self.client.logout()
        self.client.login(username='testUser2', password='password')
        resp = self.client.post(reverse('grocery_unshare',kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_list'))
        self.assertFalse(list.get_shared())






        



