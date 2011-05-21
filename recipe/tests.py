from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class recipeViewsTestCase(WebTest):
    fixtures = ['test_user_data.json','course_data.json', 'cuisine_data.json']

    def test_redirect(self):
        '''test that if a user is not logged in and they try to create a recipe they are sent to the login page'''
        resp = self.app.get(reverse('new_recipe'))
        self.assertEqual(resp.status, '302 FOUND')
