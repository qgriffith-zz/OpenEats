############
Installation
############
This document assumes you are familiar with Python and Django.

************
Requirements
************
* `Python`_ 2.6 or a higher release of 2.x
* `Django`_ 1.2.4
* `South`_ 0.7.2
* `django-disqus`_ 0.4.1
* `django-imagekit`_ 0.3.3
* `django-reversion`_ 1.3.1
* `django-taggit`_ 0.9.3
* `akismet`_ 0.2.0
* `PIL`_ 1.1.7
* `django_navbar`_ 0.3.0
* `django-profiles`_ 0.2
* `feedparser`_ 4.1
* `html5lib`_ 0.90
* `whoosh`_ 1.8.3
* `django-generic-flatblocks`_
* `django-haystack`_ 1.2.3
* `django-taggit-templatetags`_ 0.4.6dev
* `reportlab`_ 2.5
* `django-admin-tools`_ 0.3.0
* `django-registration`_ 0.8-alpha-1
* `django-relationships`_
* `django-ratings`_

************
Optional
************
* `webtest`_ 1.2.3 used for testing
* `django-webtest`_ 1.2.1 used for testing
* `django-sentry`_ 1.3.13 used for debugging and troubleshooting errors
* `django-indxer`_ 0.2 used by django-sentry
* `django-paging`_ 0.2.2 used by django-sentry
* `django-extensions`_ 0.6 extra management commands
* `django-rosetta`_ 0.6.0 used to ease translations
* `django-debug-toolbar`_ 0.8.4 used to help troubleshooting

.. _Python: http://www.python.org
.. _Django: http://www.djangoproject.com
.. _PIL: http://www.pythonware.com/products/pil/
.. _South: http://south.aeracode.org/
.. _django-disqus: https://github.com/arthurk/django-disqus
.. _django-imagekit: https://bitbucket.org/jdriscoll/django-imagekit/overview
.. _django-reversion: https://github.com/etianen/django-reversion
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
.. _django-admin-tools: https://bitbucket.org/izi/django-admin-tools/wiki/Home
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

***************************
Python Virtual Environment
***************************
The easiest way to install OpenEats2, is to create a python virtual environment.  This allows for
keeping all the packages for OpenEats2 in a separate place.  Saving the hassel of dealing with application dependencies.


Installing virtualenv
=======================

To install `virtualenv`_ from the command line type

.. code-block:: bash
    pip install virtualenv

.. _virtualenv: http://pypi.python.org/pypi/virtualenv

You will also want to install the `virtualenvwrapper`_ package to make management of hte virtual environment simpler

.._virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/

To install `virtualenvwrapper`_  from the command line type

.. code-block:: bash
    pip install virtualenvwrapper


Creating the virtualenv
========================

To create the skeleton virtualenv run the following commands

.. code-block:: bash
    export WORKON_HOME=~/Envs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv openeats
    workon openeats

.. note:: You can set your workon home directory anywhere you want it doesn't have to be in the Envs directory
          The virtualenvwrapper.sh may not be located in /usr/local/bin it varies by operating system

***************************
Installing
***************************

* Download the latest package from `github`_
* Unzip the files into a directory that your web server can access
* Install the `requirements`_

.._github: https://github.com/qgriffith/OpenEats


.. _requirements:
Installing Requirements packages
================================
To install all the packages that OpenEats2 requires perform the following steps.

* Activate your virtualenv
* Change to the directory that you unzipped the OpenEats2 files into
* Run the following command

.. code-block:: bash
    pip install -r OE2_Requirements.txt






