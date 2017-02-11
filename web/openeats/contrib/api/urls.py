from django.conf.urls import include, url

from tastypie.api import Api

from openeats.contrib.api.api import RecipeResource, GroceryResource


v1_api = Api(api_name='v1')
v1_api.register(RecipeResource())
v1_api.register(GroceryResource())

urlpatterns = [
    url(r'^', include(v1_api.urls))
]
