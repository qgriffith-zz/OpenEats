import datetime
from haystack.indexes import *
from haystack import site
from models import Recipe

class RecipeIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='author')
    course = CharField(model_attr='course')
    cuisine = CharField(model_attr='cuisine')
    pub_date = DateTimeField(model_attr='pub_date')
    def get_queryset(self):
        """Used when the entire index for the recipe model is updated"""
        return Recipe.objects.filter(shared=Recipe.SHARE_SHARED, pub_date__lte=datetime.datetime.now()) #only index shared recipes no private

site.register(Recipe, RecipeIndex)