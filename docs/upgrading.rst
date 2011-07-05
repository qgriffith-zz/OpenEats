###########
Upgrade
###########

Upgrade 2.0 to 2.1
=====================
This procedure covers how to upgrade your existing 2.0 OpenEats2 site to version 2.1



Install
---------

* Download the latest package from `github`_
* Unzip the file
* Backup your database
* Backup your current site files
* From the unzip file, copy everything other then the settings.py, site-media/upload and site-media/uploads file into your current openeats directory, over writting
  what is already there

.. _github: https://github.com/qgriffith/OpenEats


Config File Changes
---------------------
Some minor changes need to be made to the settings.py file of your current site.

Remove the following from the installed apps section of the settings.py file

* admin_tools.theming
* admin_tools.menu
* admin_tools.menu

Add the following to the installed apps section of the settings.py file on the *first* line::

    'grappelli.dashboard',

Add the following to the installed apps section of the settings.py file::

        'django.contrib.staticfiles',

Remove the following from the *context processors* section of the settings.py file::

    "grappelli.context_processors.admin_template_path",

Add the following to the *context processors* section of the settings.py file::

    "openeats.context_processors.oetitle",

Add the following line to the settings.py file::

     LOCALE_PATHS = (
        os.path.join(BASE_PATH, 'locale',)
     )

Remove the following lines in your settings.py file::

    ADMIN_TOOLS_INDEX_DASHBOARD = 'openeats.dashboard.CustomIndexDashboard'
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'openeats.dashboard.CustomAppIndexDashboard'

Add the following line to your settings.py file::

    GRAPPELLI_INDEX_DASHBOARD = 'openeats.dashboard.CustomIndexDashboard'

Add the following lines to your settings.py file::

    STATIC_ROOT = os.path.join(BASE_PATH, 'static-files')
    STATIC_URL = '/static-files/'

Change the *ADMIN_MEDIA_PREFIX* setting in the settings.py file to this::

    ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

Add the following line under the *OpenEats Settings* section of the settings.py file::

    OETITLE="OpenEats2"

You can set this to anything you want your site title to be, it doesn't have to be set to *OpenEats2*

Removing directories
----------------------

The following directories are no longer needed for version 2.1 and can be removed

* grappelli
* site-media/admin
* site-media/admin_tools

Upgrade third party apps
-------------------------

To upgrade all the packages that OpenEats2 requires perform the following steps.

* Activate your virtualenv
* Change to the directory that you unzipped the OpenEats2 files into
* Run the following command::

    pip install -r OE2_Requirements.txt --upgrade

Database changes
------------------

Running the following command from the OpenEats2 directory::

    ./manage.py syncdb
    ./manage.py migrate djangoratings 0001 --fake
    ./manage.py migrate djangoratings 0002 --fake
    ./manage.py migrate djangoratings 0003
    ./manage.py migrate djangoratings 0004 --fake
    ./manage.py migrate djangoratings 0005 --fake
    ./manage.py migrate djangoratings
    ./manage.py migrate sentry 0001 --fake
    ./manage.py migrate sentry 0002 --fake
    ./manage.py migrate sentry 0003 --fake
    ./manage.py migrate sentry 0004 --fake
    ./manage.py migrate sentry 0005 --fake
    ./manage.py migrate sentry 0006 --fake
    ./manage.py migrate sentry 0007 --fake
    ./manage.py migrate sentry 0008 --fake
    ./manage.py migrate sentry 0009 --fake
    ./manage.py migrate sentry
    ./manage.py migrate

Third Party static files
--------------------------

Django 1.3 offers a new feature that pulls in all the css and image files from third party apps into one folder.
This does away with having to setup symnlinks to them yourself.  The files are stored in the static-files directory.
To get the initial files set run the following command::

    ./manage.py collectstatic


Rebuild Search Index
---------------------

The search engine was updated as part of this release so it is a good idea to run the folloiwng command to rebuild it::

    ./manage.py rebuild_index

Running
-------
After the upgrade you can run the following command to start the internal Django webserver.  This will allow you to
test your site::

    ./manage.py runserver 8000

