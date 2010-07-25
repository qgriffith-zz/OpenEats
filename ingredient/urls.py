from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^auto/$', 'ingredient.views.autocomplete_ing'),
   )