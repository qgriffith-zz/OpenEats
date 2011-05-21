from django.test import TestCase
from models import Recipe
from recipe_groups.models import Course,Cuisine
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import close_connection
from django.core import signals
from django.core.handlers.wsgi import WSGIHandler
from StringIO import StringIO
import twill

class RecipeTestCase(TestCase):
    '''Test the Recipe Create Form'''
    fixtures = ['test_user_data.json','course_data.json', 'cuisine_data.json'] #load a user up and course and cuisine data
    
    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.assertEquals(self.user.username, 'testUser') #make sure the user works
        twill.set_output(StringIO())
        self.old_propagate = settings.DEBUG_PROPAGATE_EXCEPTIONS
        settings.DEBUG_PROPAGATE_EXCEPTIONS = True
        signals.request_finished.disconnect(close_connection)
        twill.add_wsgi_intercept(TWILL_TEST_HOST, 80, WSGIHandler)
        self.browser = twill.get_browser()

    def testRecipeRedirect(self):
        '''Test that if a user who is not authenticated trys to create a recipe will be sent to the login page'''
        response = self.client.get(reverse('new_recipe'))
        self.assertEqual(response.status_code, 302)

    def testRecipeForm(self):
              
        self.browser.go(reverse_for_twill('django.contrib.auth.views.login'))
        twill.commands.formvalue(2, 'username', 'testUser')
        twill.commands.formvalue(2, 'password', 'password')
        self.browser.submit('login')
        twill.commands.url(reverse_for_twill('recipe_index') + '$')

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
        twill.commands.find('Chef') #this should be found on the page if the recipe was saved and we got sent to the recipe show view

    def testPrivateRecipe(self):
        '''Test a recipe marked private can't be visted by another user'''
        privateUser = User.objects.create(username='privateUser') #create a new user to create a private recipe
        privateUser.set_password('password')
        privateUser.save()
        course = Course.objects.get(pk=1)
        cuisine = Cuisine.objects.get(pk=1)

        recipe = Recipe.objects.create(title="Private Recipe", author=privateUser, course=course, cuisine=cuisine, info="private stuff"
        , directions='private dancer', cook_time = 60, servings = 4, shared = Recipe.PRIVATE_SHARED)
        
        '''Login as the Private User'''
        self.browser.go(reverse_for_twill('django.contrib.auth.views.login'))
        twill.commands.formvalue(2, 'username', 'privateUser')
        twill.commands.formvalue(2, 'password', 'password')
        self.browser.submit('login')
        twill.commands.url(reverse_for_twill('recipe_index') + '$')

        '''Head over to the new recipe page'''

        self.browser.go(recipe.get_absolute_url())
        twill.commands.code(200) #make sure we got there
        twill.commands.find('Chef:') #if the page loaded we should find this word
        self.browser.go(reverse_for_twill('django.contrib.auth.views.logout'))
        
        '''Login as non-private User'''
        self.browser.go(reverse_for_twill('django.contrib.auth.views.login'))
        twill.commands.formvalue(2, 'username', 'testUser')
        twill.commands.formvalue(2, 'password', 'password')
        self.browser.submit('login')
        twill.commands.url(reverse_for_twill('recipe_index') + '$')

        '''Head over to the new recipe page'''

        self.browser.go(recipe.get_absolute_url())
        twill.commands.code(404) #should be sent to a 404 now since the recipe is private
        self.browser.go(reverse_for_twill('django.contrib.auth.views.logout'))



 
    def tearDown(self):
        User.objects.all().delete()
        Recipe.objects.all().delete()
        self.browser.go(reverse_for_twill('django.contrib.auth.views.logout'))
        twill.remove_wsgi_intercept(TWILL_TEST_HOST, 80)
        signals.request_finished.connect(close_connection)
        settings.DEBUG_PROPAGATE_EXCEPTIONS = self.old_propagate
        twill.commands.reset_output()


TWILL_TEST_HOST = 'twilltest'
def reverse_for_twill(named_url):
    '''used to create the reverse URL'''
    return 'http://' + TWILL_TEST_HOST + reverse(named_url)