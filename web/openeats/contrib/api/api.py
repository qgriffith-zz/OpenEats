from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from taggit.models import Tag

from openeats.ingredient.models import Ingredient
from openeats.recipe.models import Recipe
from openeats.list.models import GroceryList, GroceryItem,GroceryAisle


class IngredientResource(ModelResource):
    class Meta:
        queryset = Ingredient.objects.all()
        include_resource_uri = False


class AuthorResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        include_resource_uri = False

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        include_resource_uri = False

class RecipeResource(ModelResource):
    ingredients = fields.ToManyField(IngredientResource, 'ingredients', full=True)
    author = fields.OneToOneField(AuthorResource, 'author', full=True)
    tags = fields.OneToManyField(TagResource, 'tags', full=True)
    class Meta:
        queryset = Recipe.objects.filter(shared=Recipe.SHARE_SHARED)
        excludes = ['id']
        include_resource_url = False

class AisleItemsResource(ModelResource):
    class Meta:
        queryset = GroceryAisle.objects.all()
        excludes = ['id']
        include_resource_uri = False


class ListItemsResource(ModelResource):
    location = fields.OneToOneField(AisleItemsResource, 'aisle', full=True, null=True)
    class Meta:
        queryset = GroceryItem.objects.all()
        excludes = ['id']
        include_resource_uri = False

class GroceryResource(ModelResource):
    author = fields.OneToOneField(AuthorResource, 'author', full=True)
    items = fields.ToManyField(ListItemsResource, 'items', full=True)
    
    class Meta:
        queryset = GroceryList.objects.all()
        resource_name = 'lists'
        list_allowed_methods = ['get',]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(author=request.user)