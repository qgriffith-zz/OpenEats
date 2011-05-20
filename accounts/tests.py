from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class accountViewsTestCase(WebTest):
    fixtures = ['test_user_data.json']
    setup_auth = False
    def test_login(self):
        '''used to test the login form'''

        #sanity check to make sure the data loaded
        user = User.objects.get(username="testUser")
        self.assertEqual(user.username, 'testUser')
        self.assertTrue(user.check_password('password'))

        #login to the form
        form = self.app.get(reverse('auth_login')).forms[1]
        form['username'] = 'testUser'
        form['password'] = 'password'
        resp = form.submit()
        self.assertEqual(resp.status, '302 FOUND')
        self.assertEqual(resp.location, 'http://localhost:80' + reverse('recipe_index'))
        

