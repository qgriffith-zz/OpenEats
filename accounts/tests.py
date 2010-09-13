from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfiles

class AccountTestCase(TestCase):
    fixtures = ['data_user.json',' auth_user']
    def setUp(self):
        self.newUser = User.objects.create(username='newUser')
        self.newUser.set_password('password')
        self.newUser.save()
        self.assertEquals(self.newUser.username, 'newUser')
        self.newProfile = UserProfiles.objects.create(user=self.newUser, location="TestVille")
                
    def testLogin(self):
        '''Test that the login page works for a user that was loaded from a fixture'''
        self.assertTrue(self.client.login(username='testUser', password='password'))
        self.client.logout()
       
    def testProfile(self):
        '''Test that creation of a profile and edit the profile'''
        self.login = self.client.login(username='newUser', password='password')
        self.assertTrue(self.login)
        response = self.client.get('/profiles/newUser/')
        self.failUnlessEqual(response.status_code, 200)
        self.newProfile.location = "MyVille"
        self.newProfile.save()
        self.assertEquals(self.newProfile.location, 'MyVille')
           
    def tearDown(self):
       self.client.logout()
       User.objects.all().delete()
       UserProfiles.objects.all().delete()
        
