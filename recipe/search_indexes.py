import datetime
from haystack.indexes import *
from haystack import site
from models import Recipe

class RecipeIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='author')
    pub_date = DateTimeField(model_attr='pub_date')

    def get_queryset(self):
        """Used when the entire index for the recipe model is updated"""
        return Recipe.objects.filter(pub_date__lte=datetime.datetime.now())

site.register(Recipe, RecipeIndex)