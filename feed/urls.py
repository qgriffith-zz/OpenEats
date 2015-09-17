from django.conf.urls import *
from views import RecentRecipesFeed,TopRecipesFeed,TaggedRecipesFeed

urlpatterns = patterns('',
    (r'^recent/$', RecentRecipesFeed()),
    (r'^top/$', TopRecipesFeed()),
    (r'^tag/(?P<tag>[-\w]+)/$', TaggedRecipesFeed()),
)
