import helpers.signals  #needed to import the signal for when a user is saved their profile is created
from registration.views import RegistrationView
from relationships.listeners import attach_relationship_listener
attach_relationship_listener()
register = RegistrationView.as_view()

# Uncomment the next two lines to enable the admin:

from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth import views as  auth_views


from openeats.accounts import views
from openeats.accounts.forms import ProfileForm
from openeats import recipe
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/logout/$', views.logout_page, name='accounts.views.logout_page'),
    url(r'^accounts/signIn/$', views.signIn_page, name='accounts.views.signIn_page'),
    url(r'^accounts/ajax-signIn/$', auth_views.login, {'template_name': 'accounts/ajax_signIn.html',}, name='login'),
    url(r'^accounts/ajax-create/$', register, {'backend': 'registration.backends.default.DefaultBackend','template_name': 'accounts/ajax_create.html',}),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/edit', views.edit_profile, {'form_class': ProfileForm,}),
    url(r'^profiles/', include('openeats.accounts.urls')),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^follow/', include('relationships.urls')),
    url(r'^friends/', include('openeats.friends.urls')),
    url(r'^feed/', include('openeats.feed.urls')),
    url(r'^groups/', include('openeats.recipe_groups.urls')),
    url(r'^recipe/', include('openeats.recipe.urls')),
    url(r'^ingredient/', include('openeats.ingredient.urls')),
    url(r'^list/', include('openeats.list.urls')),
    url(r'^tags/', include('openeats.tags.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^news/', include('openeats.news.urls')),
    url(r'^languages/', include('openeats.languages.urls')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^$', recipe.views.index),
]

if settings.SERVE_MEDIA:
    urlpatterns += [
        url(r'^site-media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT})
    ]

if settings.DEBUG:

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
