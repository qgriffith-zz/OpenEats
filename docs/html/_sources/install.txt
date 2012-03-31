############
Installation
############
This document assumes you are familiar with Python and Django.

************
Requirements
************
* `Python`_ 2.6 or a higher release of 2.x
* `Django`_ 1.3.1
* `South`_ 0.7.3
* `django-disqus`_ 0.4.1
* `django-imagekit`_ 0.4.0
* `django-taggit`_ 0.9.3
* `akismet`_ 0.2.0
* `PIL`_ 1.1.7
* `django_navbar`_ 0.3.0
* `django-profiles`_ 0.2
* `feedparser`_ 4.1
* `html5lib`_ 0.90
* `whoosh`_ 1.8.4
* `django-haystack`_ 1.2.4
* `django-taggit-templatetags`_ 0.4.6dev
* `reportlab`_ 2.5
* `django-registration`_ 0.8-alpha-1
* `django-relationships`_ 0.3.0
* `django-ratings`_ 0.3.6
* `django-grappelli`_ 2.3.7

************
Optional
************
* `webtest`_ 1.2.3 used for testing
* `django-webtest`_ 1.4.1 used for testing
* `django-sentry`_ 1.10.1 used for debugging and troubleshooting errors
* `django-indxer`_ 0.3.0 used by django-sentry
* `django-paging`_ 0.2.4 used by django-sentry
* `django-extensions`_ 0.6 extra management commands
* `django-rosetta`_ 0.6.2 used to ease translations
* `django-debug-toolbar`_ 0.8.5 used to help troubleshooting
* `django-tastypie`_ 0.9.11
* `lxml`_ 2.3

.. _Python: http://www.python.org
.. _Django: http://www.djangoproject.com
.. _PIL: http://www.pythonware.com/products/pil/
.. _South: http://south.aeracode.org/
.. _django-disqus: https://github.com/arthurk/django-disqus
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit/
.. _django-taggit: https://github.com/alex/django-taggit/
.. _akismet: http://pypi.python.org/pypi/akismet/0.2.0
.. _django_navbar: http://code.google.com/p/django-navbar/
.. _django-profiles: https://bitbucket.org/ubernostrum/django-profiles/wiki/Home
.. _feedparser: http://www.feedparser.org/
.. _html5lib: http://code.google.com/p/html5lib/
.. _whoosh: https://bitbucket.org/mchaput/whoosh/wiki/Home
.. _django-generic-flatblocks: https://github.com/bartTC/django-generic-flatblocks/tree
.. _django-haystack: http://haystacksearch.org/
.. _django-taggit-templatetags: https://github.com/feuervogel/django-taggit-templatetags
.. _reportlab: http://www.reportlab.com/software/opensource/
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/downloads/django-registration-0.8-alpha-1.tar.gz
.. _django-relationships: https://github.com/coleifer/django-relationships/tarball/4b56427b78ea5313b5a30cff51251bcf7712df4c
.. _django-ratings: https://github.com/dcramer/django-ratings/tarball/3c31fac17a8a1b53628101e7addb8f5db7d775fe
.. _webtest: http://pypi.python.org/pypi/WebTest/0.9
.. _django-webtest: http://pypi.python.org/pypi/django-webtest
.. _django-sentry: https://github.com/dcramer/django-sentry
.. _django-indxer: http://pypi.python.org/pypi/django-indexer/0.2
.. _django-paging: http://pypi.python.org/pypi/django-paging/0.2.2
.. _django-extensions: http://pypi.python.org/pypi/django-extensions/0.6
.. _django-rosetta: http://code.google.com/p/django-rosetta/
.. _django-debug-toolbar: http://pypi.python.org/pypi/django-debug-toolbar/0.8.4
.. _django-grappelli: http://code.google.com/p/django-grappelli/
.. _django-tastypie: http://readthedocs.org/docs/django-tastypie/en/v0.9.9/
.. _lxml: http://lxml.de/

***************************
Python Virtual Environment
***************************
The easiest way to install OpenEats2, is to create a python virtual environment.  This allows for
keeping all the packages for OpenEats2 in a separate place.  Saving the hassle of dealing with application dependencies.


Installing virtualenv
=======================

To install `virtualenv`_ from the command line type::

    pip install virtualenv

You will also want to install the `virtualenvwrapper`_ package to make management of the virtual environment simpler

To install `virtualenvwrapper`_  from the command line type::

    pip install virtualenvwrapper

.. _virtualenv-label:

Creating the virtualenv
========================

To create the skeleton virtualenv run the following commands::

    export WORKON_HOME=~/Envs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv openeats --no-site-packages
    workon openeats

.. note:: You can set your workon home directory anywhere you want it doesn't have to be in the Envs directory
          The virtualenvwrapper.sh may not be located in /usr/local/bin it varies by operating system.  For help
          with `virtualenvwrapper`_ vist their site.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/

***************************
Installing
***************************

* Download the latest package from `github`_
* Unzip the files into a directory that your web server can access
* Make sure the directory is called openeats or python won't be able to find it
* Install the required packages

.. _github: https://github.com/qgriffith/OpenEats


.. _requirements:

Installing Requirements packages
================================
To install all the packages that OpenEats2 requires perform the following steps.

* Activate your virtualenv
* Change to the directory that you unzipped the OpenEats2 files into
* Run the following command::

    pip install -r OE2_Requirements.txt

Database
=========
OpenEats2 has been tested with `MySQL`_ and `SQLite`_ and minimal testing has been done with `PostgreSQL_`  Technically it should be able to work under
any `django supported`_ database.  SQLite is built into python and does not require any additional software.


MySQL
------

To install the `MySQL-Python`_ module perform the following steps

* Activate your OpenEats2 virtualenv
* Run the following command::

    pip install mysql-python


PostgresSQL
------------

To install the `Postgres`_ module perform the following steps

* Activate your OpenEats2 virtualenv
* Run the following command::

    pip install psycopg2

There is a small issue with PostgresSQL that will cause you an error when loading the data.  To get around this issue
perform the following steps;

* Copy the postgres_settings.py to settings.py.
* Then skip running the migrate command from the *Required Data* section below.
* After running the ./manage.py syncdb command from the *Required Data* section, edit the settings.py file and remove the *#* from in front of the word *south* in the file and save it.
* Then run the command *./manage.py migrate --fake*.
* Continue with the rest of the instructions as normal.

.. _MySQL-Python: https://sourceforge.net/projects/mysql-python/
.. _MySQL: http://www.mysql.com
.. _SQLite: http://www.sqlite.org/
.. _django supported: https://docs.djangoproject.com/en/1.2/ref/databases/
.. _PostgreSQL: http://www.postgresql.org/
.. _Postgres: http://initd.org/psycopg/

Load Initial Data
==================

OpenEats2 comes with default data that needs to be loaded into the database.

Required Data
--------------

Running the following command from the OpenEats2 directory, should load the required data::

    ./manage.py syncdb --all
    ./manage.py migrate --fake
    ./manage.py loaddata fixtures/navbar_about_data.json

.. note:: Before you run this make sure you have setup your database in the settings.py file.
          For more information on this see :ref:`database-config`

Optional Data
--------------

You can pre-load courses and cuisines by running the following commands from the OpenEats2 directory::

    ./manage.py loaddata recipe_groups/fixtures/course_data.json
    ./manage.py loaddata recipe_groups/fixtures/cuisine_data.json
    

Collecting Static Files
------------------------
To collect the static files from the third party applications run the following command::

    ./manage.py collectstatic

Running
-------
After the install you can run the following command to start the internal Django webserver.  This will allow you to
test your site prior to setting up a "real" webserver such as Apache::

    ./manage.py runserver 8000


This will bind the webserver to port 8000 on 127.0.0.1 otherwise known as localhost.  If you are deploying OpenEats2 to
a remote server and not your local computer run the following command instead::

    ./manage.py runserver 0.0.0.0:8000

You should then be able to access your new OpenEats2 site by pointing your browser to your URL with port 8000::

    http://yoursite:8000

.. note::  You should not run OpenEats2 in production with the built in webserver.  You will want to setup `Apache`_ or
           `Ngnix`_ Check out the `Django Apache WSGI`_ document for more info.

.. _Apache: http://www.apache.org
.. _Ngnix: http://nginx.org/
.. _Django Apache WSGI: https://docs.djangoproject.com/en/1.2/howto/deployment/modwsgi/


Site Name
----------
You will need to set up your site name before you can use certain features. See :ref:`site-name`