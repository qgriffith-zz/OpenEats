from django.conf.urls import *

urlpatterns = patterns('',
   (r'^auto/$', 'ingredient.views.autocomplete_ing'),
)