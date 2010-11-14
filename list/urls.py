from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^grocery/$', 'list.views.index', name="grocery_list"),

   )