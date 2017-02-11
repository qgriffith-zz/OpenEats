from django.conf.urls import url

from openeats.recipe import views
from openeats.helpers.recipe_views import RecentRecipeView, TopRecipeView


urlpatterns = [
    url(r'^new/$', views.recipe, name="new_recipe"),
    url(r'^mail/(?P<id>\d+)/$', views.recipeMail, name='recipe_mail'),
    url(r'^edit/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.recipe, name='recipe_edit'),
    url(r'^print/(?P<slug>[-\w]+)/$', views.recipePrint, name="print_recipe"),
    url(r'^cook/(?P<slug>[-\w]+)/$', views.CookList.as_view()),
    url(r'^report/(?P<slug>[-\w]+)/$', views.recipeReport, name='recipe_report'),
    url(r'^store/(?P<object_id>\d+)/$', views.recipeStore, name='recipe_store'),
    url(r'^unstore/$', views.recipeUnStore, name='recipe_unstore'),
    url(r'^ajaxnote/$', views.recipeNote),
    url(r'^ajaxulist/(?P<shared>[-\w]+)/(?P<user>[-\w]+)/$', views.recipeUser),
    url(r'^ajax-raterecipe/(?P<object_id>\d+)/(?P<score>\d+)/$', views.recipeRate, name='recipe_rate'),
    url(r'^ajax-favrecipe/$', views.recipeUserFavs),
    url(r'^recent/$', RecentRecipeView.as_view(), name='recipe_recent'),
    url(r'^top/$', TopRecipeView.as_view(), name='recipe_top'),
    url(r'^(?P<slug>[-\w]+)/$', views.recipeShow, name='recipe_show'),
    url(r'^export/(?P<slug>[-\w]+)/$', views.exportPDF, name='recipe_export'),
    url(r'^$', views.index, name='recipe_index'),
]
