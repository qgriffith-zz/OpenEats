from django.conf.urls.defaults import *
from views import RecentRecipesFeed

urlpatterns = patterns('',

    (r'^recent/$', RecentRecipesFeed()),

)