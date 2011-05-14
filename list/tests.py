from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from list.models import GroceryList, GroceryItem, GroceryShared, GroceryAisle

class listViewsTestCase(TestCase):
    fixtures=['user_data.json', 'list_test_data.json', 'aisle_data.json']
    def test_index(self):
        self.client.login(username="testUser", password='password')
        self.user = User.objects.get(pk=2)
        resp = self.client.get(reverse('grocery_list'))
        self.assertEqual(resp.status_code, 200)
    


