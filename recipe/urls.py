from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import Recipe

recipe_info={
    'queryset': Recipe.objects.all(),
}


urlpatterns = patterns('',
    (r'^(?P<slug>[-\w]+)/$', list_detail.object_detail, recipe_info),
    (r'^', 'openeats.recipe.views.index')
   )
