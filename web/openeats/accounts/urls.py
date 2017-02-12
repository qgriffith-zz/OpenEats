from django.conf.urls import  url

from openeats.accounts import views


urlpatterns =  [
    url(r'^create/$',
        views.create_profile,
        name='profiles_create_profile'),
    url(r'^edit/$',
        views.edit_profile,
        name='profiles_edit_profile'),
    url(r'^(?P<username>[\w.@+-]+)/$',
        views.profile_detail,
        name='profiles_profile_detail'),
    url(r'^$',
        views.ProfileListView.as_view(),
        name='profiles_profile_list'),
]

