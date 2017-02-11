import datetime

from haystack import indexes

from openeats.recipe.models import Recipe


class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    course = indexes.CharField(model_attr='course')
    cuisine = indexes.CharField(model_attr='cuisine')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        """Used when the entire index for the recipe model is updated"""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now(), shared=0)
