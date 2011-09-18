#############
Admin Page
#############

OpenEats2 has an Admin backend to allow the administrator of the site manager their OpenEats2 site.

Access Admin Site
==================

To access the Admin site point your browser to the following URL::

    http://yourdomain/admin

You will be prompted to login with a userid and password the defaults are::

    user: admin
    password: password

You will want to change this as soon as you login by click on the *users* link inside the admin page

.. _site-name:

Change Site Name
==================
You will want to change the site name on the Admin page to match your domain name. To do so click on the *sites* link
on the Admin Page then click on the current entry for site name which should be *example* then change that to match your
domain name, with out the *http or www* part

.. note::  Do not just delete the name that is currently there. Django expects your site name to start with the primary key
           of 1 in the database.  If you delete the site name and add a new one it will have the id of 2. So edit the site name
           that is already there.
