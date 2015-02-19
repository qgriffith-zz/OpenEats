# For users using the postgres database settings for openeats project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = True

ADMINS = (
    # ('Your Name', 'youremail@email.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s

LANGUAGES = (
     ('en', ugettext('English')),
     ('de', ugettext('German')),
     ('es', ugettext('Spanish')),
   )


SITE_ID = 1

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

CACHE_BACKEND = "file://"+os.path.join(BASE_PATH, 'cache')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_PATH, 'site-media')
STATIC_ROOT = os.path.join(BASE_PATH, 'static-files')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site-media/'
STATIC_URL = '/static-files/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/site-media/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tk1ig_pa_p9^muz4vw4%#q@0no$=ce1*b$#s343jouyq9lj)k33j('

AUTH_PROFILE_MODULE = 'accounts.UserProfiles'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.static',
    "navbar.context_processors.navbars",
    "openeats.context_processors.oelogo",
    "openeats.context_processors.oetitle",

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'pagination.middleware.PaginationMiddleware',
    
)

LOCALE_PATHS = (
  os.path.join(BASE_PATH, 'locale',)
)

ROOT_URLCONF = 'openeats.urls'

TEMPLATE_DIRS = (
   os.path.join(BASE_PATH, 'templates'),
)

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'taggit',
    'taggit_templatetags',
    #'south',
    'navbar',
    'disqus',
    'registration',
    'rosetta',
    'profiles',
    'imagekit',
    'djangoratings',
    'haystack',
    'indexer',
    'paging',
    'pagination',
    'django_extensions',
    'relationships',
    'tastypie',
    'openeats',
    'openeats.recipe',
    'openeats.recipe_groups',
    'openeats.ingredient',
    'openeats.accounts',
    'openeats.news',
    'openeats.list',
)


#OpenEats2 Settings
OELOGO = 'images/oelogo.png'
OETITLE = 'OpenEats2 Dev'


INTERNAL_IPS = ('127.0.0.1',)

### DEBUG-TOOLBAR SETTINGS
DEBUG_TOOLBAR_CONFIG = {
'INTERCEPT_REDIRECTS': False,
}

#Email Server Settings
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT =''
#EMAIL_USE_TLS = True

#registration
LOGIN_REDIRECT_URL = "/recipe/"
ACCOUNT_ACTIVATION_DAYS = 7

#Haystack config
HAYSTACK_SITECONF = 'openeats.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH =  os.path.join(BASE_PATH, 'search_index')

GRAPPELLI_ADMIN_TITLE = OETITLE
GRAPPELLI_INDEX_DASHBOARD = 'openeats.dashboard.CustomIndexDashboard'

PAGINATION_DEFAULT_PAGINATION = 10

try:
    from local_settings import *
except ImportError:
    pass
