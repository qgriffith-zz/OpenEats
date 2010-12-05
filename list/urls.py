from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^grocery/$', 'list.views.index', name="grocery_list"),
    url(r'^grocery/delete/(?P<id>\d+)/$', 'list.views.groceryDelete', name='grocery_delete'),
    url(r'^grocery/create/$', 'list.views.groceryCreate', name="grocery_create"),
    url(r'^grocery/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryShow', name='grocery_show'),
    url(r'^grocery/print/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryShow', {'template_name':'list/grocery_print.html',}, name='grocery_print'),
   )