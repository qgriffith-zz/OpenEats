############
Testing
############

OpenEats2 comes with several built in test to make sure the code is working as designed. To run the test make sure
you have installed the following packages in your virtuenv

* `webtest`_ 1.2.3 used for testing
* `django-webtest`_ 1.2.1 used for testing

.. _webtest: http://pypi.python.org/pypi/WebTest/0.9
.. _django-webtest: http://pypi.python.org/pypi/django-webtest

Running Test
=============
To run the test run the following command once you are in your virtuenv::

    ./manage.py test recipe

*recipe* can be replaced with which ever app you want to test. Currently the following apps have tests

* recipe
* accounts
* list