from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^grocery/$', 'list.views.index', name="grocery_list"),
    url(r'^grocery/delete/(?P<id>\d+)/$', 'list.views.groceryDelete', name='grocery_delete'),

   )