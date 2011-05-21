from django_webtest import WebTest
from django.core.urlresolvers import reverse
from recipe.models import Recipe
from django.contrib.auth.models import User

class recipeViewsTestCase(WebTest):
    fixtures = ['test_user_data.json','course_data.json', 'cuisine_data.json', 'recipe_data.json', 'ing_data.json']

    def test_redirect(self):
        '''test that if a user is not logged in and they try to create a recipe they are sent to the login page'''
        resp = self.client.get(reverse('new_recipe'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('new_recipe'))

    def test_detail(self):
        '''test that you can access a recipe detail page'''
        recipe = Recipe.objects.get(pk=1)
        resp = self.client.get(reverse('recipe_show',kwargs={'slug': recipe.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('recipe' in resp.context)
        self.assertTrue(resp.context['recipe'].slug, 'chili')
        ing = recipe.ingredient_set.all()
        self.assertTrue(ing[0], 'black pepper')

        #make sure a non-existent recipe throws a 404
        resp = self.client.get(reverse('recipe_show',kwargs={'slug': 'badrecipe'}))
        self.assertEqual(resp.status_code, 404)


