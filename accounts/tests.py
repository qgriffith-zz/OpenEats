from django.test import TestCase
from django.contrib.auth.models import User

class AccountTestCase(TestCase):
    fixtures = ['data_user.json',' auth_user']
    def setUp(self):
        pass
    def testLogin(self):
       self.assertTrue(self.client.login(username='testUser', password='password'))