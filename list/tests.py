from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from list.models import GroceryList, GroceryItem, GroceryShared, GroceryAisle

class listViewsTestCase(TestCase):
    fixtures=['test_user_data.json', 'list_test_data.json', 'aisle_data.json']
    def setUp(self):
        self.client.login(username="testUser", password='password')

    def test_index(self):
        '''test we get a list of grocery list for a giving user'''
        resp = self.client.get(reverse('grocery_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('glists' in resp.context)
        self.assertEqual([glist.pk for glist in resp.context['glists']], [1])

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

        #make sure a non-existent list throws a 404
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test2'}))
        self.assertEqual(resp.status_code, 404)

        #make sure another user can't see someones list
        self.client.logout()
        self.client.login(username="testUser2", password="password")
        resp = self.client.get(reverse('grocery_show', kwargs={'user':'testUser', 'slug':'test'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('grocery_list'))



        



