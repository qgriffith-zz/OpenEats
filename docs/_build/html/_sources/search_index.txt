#############
Search Index
#############

The search feature on OpenEats2 is handled by two different applications; `django-haystack`_ and `whoosh`_

.. _whoosh: https://bitbucket.org/mchaput/whoosh/wiki/Home
.. _django-haystack: http://haystacksearch.org/

Updating the Index
===================
You have two options when updating the search index;

* Real time, as a recipe is added or deleted the index is updated, this is the default method.
* Scheduled, you can run a script every x minutes to update the index

Real time Updates
------------------
By default OpenEats2 ships with real time update dates out of the box; meaning if a recipe is added the search index
is updated.  There are some downsides to this.  If you have a real active site, updating the index in real time could
cause a huge slow down.  The handoff between the database save and the search index update could cause some weird issues
in your database such as items only being half saved, this would happen during a heavy load on the system.

.. note:: If you are going to run OpenEats2 on Apache with mod_wsgi, you will need to enable `mod_wsgi`_ to run in daemon
          mode for real time updates.  Otherwise everyone once in a while you will get an error that the index can't be
          updated because of garbage collection on Apache.

.. _mod_wsgi: http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIDaemonProcess


Schedule Updates
------------------
If you do not wish to run real time updates you can set the index to be update via a script that you run on a schedule.
To do this you will want to edit the *recipe/search_indexes.py* file::

    Change line

    class RecipeIndex(RealTimeSearchIndex):

    to

    class RecipeIndex(SearchIndex):

After the change you will need to restart your web server. An example of a script that will update the index can be
found in the contrib folder of your OpenEats2 project. With out the script you can run the following commands from your
virtenv::

    ./manage.py rebuild_index  *this command creates the index
    ./manage.py update_index   *this updates an existing index

