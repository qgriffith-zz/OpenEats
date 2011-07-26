from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic import ListView
from models import Recipe

rating_qs = Recipe.objects.extra(select={'rate': '((100/%s*rating_score/(rating_votes+%s))+100)/2' % (Recipe.rating.range, Recipe.rating.weight)})
urlpatterns = patterns('',
    url(r'^new/$', 'recipe.views.recipe', name="new_recipe"),
    url(r'^edit/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'recipe.views.recipe', name='recipe_edit'),
    url(r'^print/(?P<slug>[-\w]+)/$', 'recipe.views.recipePrint', name="print_recipe"),
    (r'^cook/(?P<slug>[-\w]+)/$', list_detail.object_detail, {'queryset': Recipe.objects.all(), "template_object_name": 'recipe',"template_name": 'recipe/recipe_cook.html',}),
    url(r'^report/(?P<slug>[-\w]+)/$', 'recipe.views.recipeReport', name='recipe_report'),
    url(r'^store/(?P<object_id>\d+)/$', 'recipe.views.recipeStore', name='recipe_store'),
    url(r'^unstore/$', 'recipe.views.recipeUnStore', name='recipe_unstore'),
    (r'^ajaxnote/$', 'recipe.views.recipeNote'),
    (r'^ajaxulist/(?P<shared>[-\w]+)/(?P<user>[-\w]+)/$', 'recipe.views.recipeUser'),
    url(r'^ajax-raterecipe/(?P<object_id>\d+)/(?P<score>\d+)/$', 'recipe.views.recipeRate', name='recipe_rate'),
    (r'^ajax-favrecipe/$', 'recipe.views.recipeUserFavs'),
    url(r'^recent/$', ListView.as_view(queryset=Recipe.objects.filter(shared=Recipe.SHARE_SHARED).order_by('-pub_date', 'title')[:20],context_object_name='recipe_list')),
    url(r'^top/$', ListView.as_view(queryset=rating_qs.filter(shared=Recipe.SHARE_SHARED).order_by('-rate')[:20],context_object_name='recipe_list')),
    url(r'^(?P<slug>[-\w]+)/$', 'recipe.views.recipeShow', name='recipe_show'),
    url(r'^export/(?P<slug>[-\w]+)/$', 'recipe.views.exportPDF', name='recipe_export'),
    url(r'^$', 'recipe.views.index', name='recipe_index'),
   )
