from django.conf.urls import url

from openeats.feed.views import RecentRecipesFeed,TopRecipesFeed

urlpatterns = [
    url(r'^recent/$', RecentRecipesFeed()),
    url(r'^top/$', TopRecipesFeed()),
]