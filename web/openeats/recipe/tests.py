from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from openeats.recipe.models import Recipe, StoredRecipe


class recipeViewsTestCase(WebTest):
    fixtures = ['test_user_data.json','course_data.json', 'cuisine_data.json', 'recipe_data.json', 'ing_data.json']
    extra_environ = {'REMOTE_ADDR': '127.0.0.1'}
    csrf_checks = False

    def test_redirect(self):
        """test that if a user is not logged in and they try to create a recipe they are sent to the login page"""
        resp = self.client.get(reverse('new_recipe'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('new_recipe'))

    def test_detail(self):
        """test that you can access a recipe detail page"""
        recipe = Recipe.objects.get(pk=1)
        resp = self.client.get(reverse('recipe_show',kwargs={'slug': recipe.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('recipe' in resp.context)
        self.assertTrue(resp.context['recipe'].slug, 'chili')
        ing = recipe.ingredients.all()
        self.assertTrue(ing[0], 'black pepper')

        #make sure a non-existent recipe throws a 404
        resp = self.client.get(reverse('recipe_show',kwargs={'slug': 'badrecipe'}))
        self.assertEqual(resp.status_code, 404)

    def test_create(self):
        """test the creation of a recipe using the form"""
        resp = self.app.get(reverse('new_recipe'), user='testuser')
        self.assertEqual(resp.status, '200 OK')
        form = resp.forms[2]
        form['title'] = 'my recipe'
        form['course'] = "1"
        form['cuisine'] = "2"
        form['info'] = "this is my recipe"
        form['cook_time'] = "20"
        form['servings'] = "2"
        form['shared'] = "1"  #making the recipe private
        form['tags'] = 'recipe'
        form['directions'] = "cook till done"
        form['ingredients-0-quantity'] = "2"
        form['ingredients-0-measurement'] = 'cups'
        form['ingredients-0-title'] = 'flour'
        form['ingredients-1-quantity'] = "1"
        form['ingredients-1-measurement'] = 'cup'
        form['ingredients-1-title'] = 'water'
        resp = form.submit()
        self.assertEqual(resp.context.dicts[1]['object'].title, 'my recipe')
        recipe = Recipe.objects.get(slug=resp.context.dicts[1]['object'].slug)
        self.assertTrue(recipe)

    def test_private(self):
        """makes sure only the owner of a private recipe can view it"""

        #sanity check make sure the recipe is private
        self.test_create() #call the create recipe test from above to load the DB with a private recipe
        recipe = Recipe.objects.get(title="my recipe")
        self.assertEqual(recipe.shared, 1)

        resp = self.app.get(reverse('recipe_show',kwargs={'slug': recipe.slug}), user='testuser2',status=404)
        self.assertEqual(resp.status, '404 Not Found')

        #test that the owner of the recipe can access it
        resp = self.app.get(reverse('recipe_show',kwargs={'slug': recipe.slug}), user='testuser')
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.context['recipe'].title, 'my recipe')

    def test_rate(self):
        """test that you can rate a recipe"""

        #sainty check there should be no ratings right now"""
        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.rating.votes, 0)

        #add a vote
        resp = self.app.get(reverse('recipe_rate',kwargs={'object_id':1, 'score':4}), user='testuser')
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue('Vote recorded.' in resp)

    def test_store(self):
        """test a user can store a recipe"""
        recipe = Recipe.objects.get(pk=1)
        user = User.objects.get(username='testuser')

        #sanity check make sure the recipe isn't already stored
        stored = StoredRecipe.objects.filter(user=user, recipe=recipe)
        self.assertFalse(stored)

        resp = self.app.post(reverse('recipe_store',kwargs={'object_id':1}),{'object_id':1}, user='testuser')
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue('Recipe added to your favorites!' in resp)

        #try storing a recipe that you already have stored
        resp = self.app.post(reverse('recipe_store',kwargs={'object_id':1}),{'object_id':1}, user='testuser')
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue('Recipe already in your favorites!' in resp)

        #check it is really stored in the DB
        stored = StoredRecipe.objects.get(user=user, recipe=recipe)
        self.assertTrue(stored)

    def test_unstore(self):
        """test a user can unstore a recipe"""
        recipe = Recipe.objects.get(pk=1)
        user = User.objects.get(username='testuser')

        self.test_store()  #call this to store a recipe in the DB

        resp = self.app.post(reverse('recipe_unstore'),{'recipe_id':1}, user='testuser')
        self.assertEqual(resp.status, '302 Found')

        #verify it was removed from the DB
        stored = StoredRecipe.objects.filter(user=user, recipe=recipe)
        self.assertFalse(stored)

        #try to store a non-existent recipe should raise 404
        resp = self.app.post(reverse('recipe_unstore'),{'recipe_id':10000}, user='testuser', status=404)
        self.assertEqual(resp.status, '404 Not Found')

    def test_report(self):
        """test that a recipe is reported bad when a user reports it"""
        recipe = Recipe.objects.get(pk=1)
        self.assertFalse(recipe.get_reported())
        resp = self.app.post(reverse('recipe_report', kwargs={'slug':recipe.slug}),user='testuser2')
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue('Recipe reported to the moderators!' in resp)

        #check it updated the DB
        recipe = Recipe.objects.get(pk=1)
        self.assertTrue(recipe.get_reported())

        #try to report a recipe that does not exist
        resp = self.app.post(reverse('recipe_report', kwargs={'slug':'bad-recipe'}),user='testuser2', status=404)
        self.assertEqual(resp.status, '404 Not Found')

        #try to report a recipe that is already reported
        resp = self.app.post(reverse('recipe_report', kwargs={'slug':recipe.slug}),user='testuser2')
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue('Recipe has already been reported!' in resp)


    def test_print(self):
        """test the print view comes up"""
        recipe = Recipe.objects.get(pk=1)
        resp  = self.client.get(reverse('print_recipe', kwargs={'slug': recipe.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['recipe'].slug, recipe.slug)
        self.assertEqual(resp.templates[0].name, 'recipe/recipe_print.html')

    def test_edit(self):
        recipe = Recipe.objects.get(pk=1)

        #sanitty check
        self.assertEqual(recipe.author.username, 'admin')
        self.assertEqual(recipe.servings, 8)
        self.assertEqual(recipe.ingredients.count(), 12)
        resp = self.app.get(reverse('recipe_edit', kwargs={'user':'admin', 'slug':recipe.slug}), user='admin')
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue(resp.forms[2])
        form = resp.forms[2]
        form['servings'] = "10"
        form['ingredients-13-quantity'] = "1"
        form['ingredients-13-measurement'] = 'cup'
        form['ingredients-13-title'] = 'cheddar cheese'
        resp = form.submit()
        self.assertEqual(resp.context.dicts[1]['object'].slug, 'tasty-chili')
        self.assertEqual(resp.request.url, "http://localhost" + reverse('recipe_edit', kwargs={'user':'admin', 'slug':recipe.slug}))

        #make sure the form saved our changes
        recipe = Recipe.objects.get(pk=1) #got to get the recipe again so that it gets our new numbers after the save
        self.assertEqual(recipe.servings, 10)
        self.assertEqual(recipe.ingredients.count(), 13)

        #test editing a non-existant recipe
        resp = self.app.get(reverse('recipe_edit', kwargs={'user':'admin', 'slug':'bad-recipe'}), user='admin', status=404)
        self.assertEqual(resp.status, '404 Not Found')

        #try having another user edit someone elses recipe
        resp = self.app.get(reverse('recipe_edit', kwargs={'user':'admin', 'slug':recipe.slug}), user='testuser', status=404)
        self.assertEqual(resp.status, '404 Not Found')






