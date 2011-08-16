from tastypie.resources import ModelResource
from tastypie import fields
from ingredient.models import Ingredient
from recipe.models import Recipe
from django.contrib.auth.models import User
from taggit.models import Tag


class IngredientResource(ModelResource):
    class Meta:
        queryset = Ingredient.objects.all()
        include_resource_url = False


class AuthorResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username']

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        include_resource_url = False


class RecipeResource(ModelResource):
    ingredients = fields.ToManyField(IngredientResource, 'ingredients', full=True)
    author = fields.OneToOneField(AuthorResource, 'author', full=True)
    tags = fields.OneToManyField(TagResource, 'tags', full=True)
    class Meta:
        queryset = Recipe.objects.filter(shared=Recipe.SHARE_SHARED)
        excludes = ['id']
        include_resource_url = False
