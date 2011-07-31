from django.conf.urls.defaults import *
from views import RecentRecipesFeed,TopRecipesFeed

urlpatterns = patterns('',
    (r'^recent/$', RecentRecipesFeed()),
    (r'^top/$', TopRecipesFeed()),
)