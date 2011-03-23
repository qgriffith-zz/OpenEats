from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^recipe/(?P<tag>[-\w]+)/$', 'tags.views.recipeTags', name="recipe_tags"),
   )