from django.test import TestCase
from models import Recipe

class RecipeTestCase(TestCase):
    fixtures = ['recipe_data.json', 'recipe']  #load up a recipe so we can do stuff with it

    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)

    def testRecipe(self):
        self.assertEquals(self.recipe.title, 'Chili')
        self.assertEquals(self.recipe.slug, 'chili')
        self.recipe.servings = 10
        self.recipe.save()
        self.assertNotEqual(self.recipe.servings, 20)
        response = self.client.get("/recipe/chili/") #this should be good because a recipe does exist
        self.failUnlessEqual(response.status_code, 200)

    def tearDown(self):
        self.recipe.delete()
        response = self.client.get("/recipe/chili/") #this should be good because we deleted the recipe
        self.failUnlessEqual(response.status_code, 404)