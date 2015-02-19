from django.conf.urls import *
from tastypie.api import Api
from api import RecipeResource, GroceryResource

v1_api = Api(api_name='v1')
v1_api.register(RecipeResource())
v1_api.register(GroceryResource())
urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)