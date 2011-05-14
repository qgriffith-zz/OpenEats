from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import Recipe

recipe_info={
    'queryset': Recipe.objects.all(),
    "template_object_name": 'recipe',
}

recipe_list={
    'queryset': Recipe.objects.filter(shared=Recipe.SHARE_SHARED).order_by('pub_date', 'title')[:10],
    "template_object_name": 'recipe',
    'template_name': 'recipe/index.html',
}


urlpatterns = patterns('',
    url(r'^new/$', 'recipe.views.recipe', name="new_recipe"),
    url(r'^edit/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'recipe.views.recipe', name='recipe_edit'),
    url(r'^print/(?P<slug>[-\w]+)/$', 'recipe.views.recipePrint', name="print_recipe"),
    (r'^cook/(?P<slug>[-\w]+)/$', list_detail.object_detail, {'queryset': Recipe.objects.all(), "template_object_name": 'recipe',"template_name": 'recipe/recipe_cook.html',}),
    url(r'^report/(?P<slug>[-\w]+)/$', 'recipe.views.recipeReport', name='recipe_report'),
    (r'^store/(?P<object_id>\d+)/$', 'recipe.views.recipeStore'),
    (r'^unstore/$', 'recipe.views.recipeUnStore'),
    (r'^ajaxnote/$', 'recipe.views.recipeNote'),
    (r'^ajaxulist/(?P<shared>[-\w]+)/(?P<user>[-\w]+)/$', 'recipe.views.recipeUser'),
    (r'^ajax-raterecipe/(?P<object_id>\d+)/(?P<score>\d+)/$', 'recipe.views.recipeRate'),
    (r'^ajax-favrecipe/$', 'recipe.views.recipeUserFavs'),
    (r'^(?P<slug>[-\w]+)/$', 'recipe.views.recipeShow'),
    url(r'^export/(?P<slug>[-\w]+)/$', 'recipe.views.exportPDF', name='recipe_export'),
    url(r'^$', 'recipe.views.index', name='recipe_index'),

   )
