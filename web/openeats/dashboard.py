"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'openeats.oedashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.LinkList(
           title=_('Quick Links'),
           layout='inline',
           column=1,
           collapsible=True,
           css_classes=('collapse closed',),
           children=(
           {
                    'title': _('Return to site'),
                    'url': '/',
                },
                {
                    'title': _('Change password'),
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': _('Log out'),
                    'url': reverse('admin:logout')
                },
           )

       ))

        # append a group for "Administration"
        self.children.append(modules.Group(
            _('Administration'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Administration'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*','registration','openeats.accounts'),
                ),
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title="OpenEats2 Applications",
            collapsible=True,
            column=1,
            models=('openeats.*','recipe*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Third Party Applications'),
            column=1,
            collapsible=True,
            exclude=('django.contrib.*','openeats.*','recipe*',)
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                                    {
                    'title': _('OpenEats Forum'),
                    'url': 'http://oe2.openeats.org/forum/',
                    'external': True,
                },
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
            ]
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest OpenEats2 News'),
            column=2,
            feed_url='http://oe2.openeats.org/blog/feed/latest',
            limit=5
        ))



