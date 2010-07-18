from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import Recipe

recipe_info={
    'queryset': Recipe.objects.all(),
    "template_object_name": 'recipe',
}

recipe_list={
    'queryset': Recipe.objects.order_by('pub_date', 'title')[:10],
    "template_object_name": 'recipe',
    'template_name': 'recipe/index.html',
}


urlpatterns = patterns('',
    (r'^new/$', 'recipe.views.recipe'),
    (r'^print/(?P<slug>[-\w]+)/$', list_detail.object_detail, {'queryset': Recipe.objects.all(), "template_object_name": 'recipe',"template_name": 'recipe/recipe_print.html',}),
    (r'^(?P<slug>[-\w]+)/$', list_detail.object_detail, recipe_info),
    (r'^', list_detail.object_list, recipe_list),
   )
