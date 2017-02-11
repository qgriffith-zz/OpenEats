from django.conf.urls import url

from openeats.list import views


urlpatterns = [
    url(r'^grocery/$', views.index, name="grocery_list"),
    url(r'^grocery/recipe/(?P<recipe_slug>[-\w]+)/$', views.groceryAddRecipe, name='grocery_addrecipe'),
    url(r'^grocery/mail/(?P<gid>\d+)/$', views.groceryMail, name='grocery_mail'),
    url(r'^grocery/delete/(?P<id>\d+)/$', views.groceryDelete, name='grocery_delete'),
    url(r'^grocery/ajaxdelete/$', views.groceryAjaxDelete, name='grocery_Ajaxdelete'),
    url(r'^grocery/aisle/ajaxdelete/$', views.groceryAisleAjaxDelete, name="grocery_aisledelete"),
    url(r'^grocery/create/$', views.groceryCreate, name="grocery_create"),
    url(r'^grocery/edit/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.groceryCreate, name='grocery_edit'),
    url(r'^grocery/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.groceryShow, name='grocery_show'),
    url(r'^grocery/print/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.groceryShow, {'template_name':'list/grocery_print.html',}, name='grocery_print'),
    url(r'^grocery/share/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.groceryShareList, name='grocery_share'),
    url(r'^grocery/unshare/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.groceryUnShareList, name='grocery_unshare'),
    url(r'^grocery/grocery-ajax/$', views.groceryProfile, name="grocery_profile"),
    url(r'^grocery/aisle/$', views.groceryAisle, name="grocery_aisle"),
]
