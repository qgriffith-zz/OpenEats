Changelog
==========

Version 2.1
--------------
* Upgraded Django to 1.3
* Added CSRF protection for AJAX calls
* Upgraded to django-grappelli 2.3.3
* Removed grappelli from the root dir of OpenEats, it now installs like all the ohter thrid party apps
* Removed admin_tools third party app
* Setup grappelli dashboard to replace the admin_tools dashboard
* Setup static files a new feature in Django 1.3. This pulls in all the third party apps images, css files.
  replaces the need to do symnlinks to them
* Upgraded django-imagekit to 0.3.6
* Upgraded django-debug-toolbar to 0.8.5
* Upgraded south to 0.7.3
* Upgraded django-haystack to 1.2.4
* Upgraded Whoosh to 1.8.4
* Upgraded django-rosetta to 0.6.2
* Upgraded django-sentry to 1.8.6.2
* Upgraded django-webtest to 1.4.1
* Upgraded django-relationships to 0.3.0
* Upgraded django-ratings to 0.3.6
* Added the ability for users to change the tile of the site via settings.py
* Added the ability to change and clear a picture on a recipe when edited

Version 2.2
--------------
* Added meta keywords and description to the main page
* Added meta keywords using recipe titles and tages to the recipe detail page
* Fixed bug of ratings not showing up on a recipe till a user voted on them even if another user had rated the recipe
* Added a top recipe view that shows the top 20 recipes
* Added a most recent recipes view that shows the 20 most recent recipes
* Added recent recipe rss feed
* Added user created aisles for grocery lists
* Added recipes displayed on grocery list when they are added to a list
* Added django-tastypie package for API
* Fixed urls.py by removing a url to a package that is not not used anymore

Version 2.3
--------------
* Added instructions and a special settings file to support PostgreSQL
* Moved the api module to the contrib folder
* Sorted grocery list and shared grocery list by created date
* Changed the submit button text on all forms to make more sense
* Changed the design of the title bar that is found above all the category list of recipes
* Removed the "follow me" link from a users profile if they are viewing their own profile.
* Branched the django ratings application and updated it to work with django 1.3
* Lots of CSS tweaks
* Upgraded to Django 1.3.1
* Moved all the CSS, images, and JS to a new folder called static to be more in-line with the Django 1.3 way of doing things
* Upgraded Grapelli to version 2.3.4
* Upgraded django-generic-flatblocks to 0.9.1
* Removed the plugin django-reversion 
* Upgraded django-imagekit to 0.4.0
* Changed the site Logo

Version 2.4
--------------
* Added a new news section now you can have more then one news story and decide which one appears on the front page
* Added the ability to email recipes to friends
* Added grocery list API
* Upgraded django-tastypie
* Complete UI over haul using Twitter Bootstrap
* Changed image size for recipe pictures
* Upgraded Grapelli to version 2.3.7
* Removed un-needed java script libraries
* Code clean up
* several small bug fixes

