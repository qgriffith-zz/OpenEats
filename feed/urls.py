from django.conf.urls import *
from views import RecentRecipesFeed,TopRecipesFeed

urlpatterns = patterns('',
    (r'^recent/$', RecentRecipesFeed()),
    (r'^top/$', TopRecipesFeed()),
)