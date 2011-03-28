from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^following/(?P<username>[\w-]+)/$', 'friends.views.follow_list', name="friends_following"),

   )