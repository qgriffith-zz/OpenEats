from django.conf.urls import url

from openeats.friends import views

urlpatterns = [
    url(r'^following/(?P<username>[\w-]+)/$', views.follow_list, name="friends_following"),
    url(r'^feed/(?P<username>[\w-]+)/$', views.feed, name="friends_feed"),
]