from django.conf.urls import url

from openeats.tags import views

urlpatterns = [
    url(r'^recipe/(?P<tag>[-\w]+)/$', views.recipeTags, name="recipe_tags"),
]
