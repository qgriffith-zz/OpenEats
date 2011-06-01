#############
Configuration
#############

This document covers the configuration settings for OpenEats2

Database
=========
To setup Django for your database refer to the 'Django Database'_ document

.. _Django Database: https://docs.djangoproject.com/en/1.2/intro/tutorial01/#database-setup

Email
======
To setup your email server open up the settings.py file located in the OpenEats2 directory and fill in the following
settings with your own email server settings::

    #Email Server Settings
    DEFAULT_FROM_EMAIL = ''
    EMAIL_HOST = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT =
    #EMAIL_USE_TLS = True

.. note:: If you do not have your own email server you can use Gmail if you have a gmail account. Follow this 'gmail guide'_
          to learn how.
.. _gmail guide: http://komunitasweb.com/2010/06/sending-email-using-gmail-account-in-django/

Logo
=====
If you want to change the logo to your own logo you can modify the OELOGO setting in the setting.py file::

    #OpenEats2 Settings
    OELOGO = 'images/oelogo.png'

Change the oelogo.png to what ever your logo image name is and place your new logo in *site-media/images* directory

#########
Comments
#########

OpenEats2 uses 'Disqus'_ for its comment system.  In order to use Disqus on your OpenEats2 site you will need to apply
for an API key and register your site.

Disqus API Key
===============
To get your own Disqus API key visit the `Disqus register`_ site and sign up.  Make sure you enter the fully qualified domain
name of where you are hosting OpenEats2.

Disqus Configuration
---------------------
Once you have register your site with Disqus you will need to add the following to your settings.py file::

    #Disqus settings
    DISQUS_API_KEY = "your API key"
    DISQUS_WEBSITE_SHORTNAME = "the shortname you entered when you registered"

.. _Disqus: http://disqus.com/
.. _Disqus register: http://disqus.com/admin/register/



