from django.test import TestCase
from models import Ingredient
from recipe.models import Recipe

class IngredientTestCase(TestCase):
    fixtures = ['recipe_data.json', 'recipe']  #load up a recipe so we can assign an ingredient to it
    def setUp(self):
        recipe = Recipe.objects.get(pk=1)
        self.ing = Ingredient.objects.create(title="bacon", quantity=1, measurement="pound", recipe=recipe)

    def testIng(self):
        self.assertEquals(self.ing.title, 'bacon')

    def tearDown(self):
        self.ing.delete()

