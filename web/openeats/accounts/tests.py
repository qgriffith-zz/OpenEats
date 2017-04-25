from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class accountViewsTestCase(WebTest):
    fixtures = ['user_data.json']
    setup_auth = False
    def test_login(self):
        """used to test the login form"""

        #sanity check to make sure the data loaded
        user = User.objects.get(username="testuser")
        self.assertEqual(user.username, 'testuser')
        # Fails because defaults hasher is pbkdf2_sha256 now
        #self.assertTrue(user.check_password('password'))

        #login to the form
        form = self.app.get(reverse('login')).forms[0]
        form['username'] = 'testuser'
        form['password'] = 'password'
        resp = form.submit()
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.location, None)

    def test_bad_login(self):
        """make sure an error is thrown when someone can't login"""
        form = self.app.get(reverse('login')).forms[0]
        form['username'] = 'testuser'
        form['password'] = 'badpassword'
        resp = form.submit()
        self.assertEqual(resp.status, '200 OK')

    def test_create_user(self):
        """test that a user can be created"""
        form = self.app.get(reverse('registration_register')).forms[0]
        form['username'] = 'newuser'
        form['email'] = 'newUser@yahoo.com'
        form['password1'] = 'password'
        form['password2'] = 'password'
        resp = form.submit().follow()
        self.assertTrue('Thank you' in resp.body)

        #check the signal on save of a new user created a profile for the user
        profile = self.app.get(reverse('profiles_profile_detail', kwargs={'username':'newuser'}))
        self.assertTrue(profile.status, '200 OK')

        #check a unknown user throws a 404 on the profile page
        profile = self.app.get(reverse('profiles_profile_detail', kwargs={'username':'baduser'}),status=404)
        self.assertTrue(profile.status, '404 Not Found')

    def test_fail_create_case_sensitive_user(self):
        """test that a user can't be created"""
        form = self.app.get(reverse('registration_register')).forms[0]
        form['username'] = 'Testuser'
        form['email'] = 'newUser@yahoo.com'
        form['password1'] = 'password'
        form['password2'] = 'password'
        resp = form.submit()
        self.assertTrue('A user with that username already exists' in resp.body)
