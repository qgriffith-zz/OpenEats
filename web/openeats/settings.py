# Django settings for openeats project.
import os


DEBUG = False
if os.environ.get('DEBUG', 'True').lower() == 'true':
    DEBUG = True

SERVE_MEDIA = True

ADMINS = (
    # ('Your Name', 'youremail@email.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('DATABASE_NAME', 'openeats'),                      # Or path to database file if using sqlite3.
        'USER': os.environ.get('DATABASE_USER', 'openeats'),                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'admin'),                      # Not used with sqlite3.
        'HOST': 'database',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Madrid')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', '127.0.0.1')]

ugettext = lambda s: s

LANGUAGES = (
     ('es', ugettext('Spanish')),
     ('en', ugettext('English')),
     ('de', ugettext('German')),
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
STATIC_ROOT = os.path.join(BASE_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site-media/'
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.

SECRET_KEY = [os.environ.get('SECRET_KEY', 'tk1ig_pa_p9^muz4vw4%#q@0no$=ce1*b$#s343jouyq9lj)k33j(')]

AUTH_PROFILE_MODULE = 'accounts.UserProfiles'


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_PATH, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.media',
            "openeats.context_processors.oelogo",
            "openeats.context_processors.oetitle",
        ]
    }
}]

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware'
)

STATICFILES_DIRS = [
    os.path.join(BASE_PATH, 'static_files')
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

LOCALE_PATHS = (
  [os.path.join(BASE_PATH, 'locale',)]
)

ROOT_URLCONF = 'openeats.urls'

INSTALLED_APPS = (
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'grappelli',
    'grappelli.dashboard',
    'taggit',
    'taggit_templatetags2',
    'disqus',
    'registration',
    'rosetta',
    'imagekit',
    'djangoratings',
    'django_extensions',
    'relationships',
    'haystack',
    'pagination',
    'tastypie',
    'openeats',
    'openeats.recipe',
    'openeats.recipe_groups',
    'openeats.ingredient',
    'openeats.accounts',
    'openeats.news',
    'openeats.list',
    'debug_toolbar',
)


#OpenEats2 Settings
OELOGO = 'images/oelogo.png'
OETITLE = os.environ.get('OETITLE', 'OpenEats2 Dev')


INTERNAL_IPS = ('127.0.0.1',)

#Email Server Settings
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_USE_TLS = False
if os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true':
    EMAIL_USE_TLS = True

#registration
LOGIN_REDIRECT_URL = "/recipe/"
ACCOUNT_ACTIVATION_DAYS = 7

#Haystack config
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH':    os.path.join(BASE_PATH, 'search_index')
    }
}


GRAPPELLI_ADMIN_TITLE = OETITLE
GRAPPELLI_INDEX_DASHBOARD = 'openeats.dashboard.CustomIndexDashboard'

PAGINATION_DEFAULT_PAGINATION = 10


