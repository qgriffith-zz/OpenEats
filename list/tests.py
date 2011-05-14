from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from list.models import GroceryList, GroceryItem, GroceryShared, GroceryAisle

class listViewsTestCase(TestCase):
    fixtures=['user_data.json', 'list_test_data.json', 'aisle_data.json']
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
        



