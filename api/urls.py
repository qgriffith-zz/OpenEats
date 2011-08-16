from django.conf.urls.defaults import *
from tastypie.api import Api
from api import RecipeResource

recipe_resource = RecipeResource()

urlpatterns = patterns('',
    (r'^v1/', include(recipe_resource.urls)),
)