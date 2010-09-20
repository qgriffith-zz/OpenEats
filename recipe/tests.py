from django.test import TestCase
from models import Recipe
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import close_connection
from django.core import signals
import twill

class RecipeTestCase(TestCase):
    '''Test the Recipe Create Form'''
    fixtures = ['data_user.json','course_data.json', 'cuisine_data.json'] #load a user up and course and cuisine data
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertEquals(self.user.username, 'testUser') #make sure the user works

    def testRecipeRedirect(self):
        '''Test that if a user who is not authenticated trys to create a recipe will be sent to the login page'''
        response = self.client.get(reverse('new_recipe'))
        self.assertEqual(response.status_code, 302)

    def testRecipeForm(self):
        from django.core.handlers.wsgi import WSGIHandler
        self.old_propagate = settings.DEBUG_PROPAGATE_EXCEPTIONS
        settings.DEBUG_PROPAGATE_EXCEPTIONS = True
        signals.request_finished.disconnect(close_connection)
        twill.add_wsgi_intercept(TWILL_TEST_HOST, 80, WSGIHandler)
        self.assertTrue(self.client.login(username=self.user.username,
            password='password'), "Logging in user %s, pw %s failed." %
            (self.user.username, self.user.password))
        twill.add_wsgi_intercept(TWILL_TEST_HOST, 80, WSGIHandler)

        self.browser = twill.get_browser()
        self.browser.go(reverse_for_twill('django.contrib.auth.views.login'))
        twill.commands.formvalue(2, 'username', 'testUser')
        twill.commands.formvalue(2, 'password', 'password')
        self.browser.submit('login')

        self.browser.go(reverse_for_twill('new_recipe'))
        twill.commands.find('title') #lets make sure we got to the recipe form
        twill.commands.formvalue(2, 'title', 'Test Recipe')
        twill.commands.formvalue(2, 'course', '1')
        twill.commands.formvalue(2, 'cuisine', '1')
        twill.commands.formvalue(2, 'info', 'Test of a twill recipe')
        twill.commands.formvalue(2, 'cook_time', '60')
        twill.commands.formvalue(2, 'servings', '4')
        twill.commands.formvalue(2, 'directions', 'Test of a twill recipe')
        twill.commands.formvalue(2, 'id_ingredient_set-0-quantity', '10')
        twill.commands.formvalue(2, 'id_ingredient_set-0-measurement', 'cups')
        twill.commands.formvalue(2, 'id_ingredient_set-0-title', 'carrots')
        twill.commands.formvalue(2, 'id_ingredient_set-0-preparation', 'gratted')
        self.browser.submit('New Recipe')

 
    def tearDown(self):
        User.objects.all().delete()
        Recipe.objects.all().delete()


TWILL_TEST_HOST = 'twilltest'
def reverse_for_twill(named_url):
    '''used to create the reverse URL'''
    return 'http://' + TWILL_TEST_HOST + reverse(named_url)