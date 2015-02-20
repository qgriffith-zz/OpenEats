from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^list/$', 'news.views.list', name="news_list"),
    url(r'^entry/(?P<slug>[\w-]+)/$', 'news.views.entry', name="news_entry"),
)