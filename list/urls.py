from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^grocery/$', 'list.views.index', name="grocery_list"),
    url(r'^grocery/recipe/(?P<recipe_slug>[-\w]+)/$', 'list.views.groceryAddRecipe', name='grocery_addrecipe'),
    url(r'^grocery/mail/(?P<gid>\d+)/$', 'list.views.groceryMail', name='grocery_mail'),
    url(r'^grocery/delete/(?P<id>\d+)/$', 'list.views.groceryDelete', name='grocery_delete'),
    url(r'^grocery/ajaxdelete/$', 'list.views.groceryAjaxDelete', name='grocery_Ajaxdelete'),
    url(r'^grocery/aisle/ajaxdelete/$', 'list.views.groceryAisleAjaxDelete', name="grocery_aisledelete"),
    url(r'^grocery/create/$', 'list.views.groceryCreate', name="grocery_create"),
    url(r'^grocery/edit/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryCreate', name='grocery_edit'),
    url(r'^grocery/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryShow', name='grocery_show'),
    url(r'^grocery/print/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryShow', {'template_name':'list/grocery_print.html',}, name='grocery_print'),
    url(r'^grocery/share/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryShareList', name='grocery_share'),
    url(r'^grocery/unshare/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'list.views.groceryUnShareList', name='grocery_unshare'),
    url(r'^grocery/grocery-ajax/$', 'list.views.groceryProfile', name="grocery_profile"),
    url(r'^grocery/aisle/$', 'list.views.groceryAisle', name="grocery_aisle"),
)