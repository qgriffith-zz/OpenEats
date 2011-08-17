##################
Exporting Recipes
##################

You can export individual recipes or every recipe you have on your site into the common MealMaster format.

Exporting Individual Recipes
=============================
To export individual recipes login to the Admin part of the site :doc:`admin`. Click on the *Recipes* link.
Then place a check mark in the box next to each recipe you want to export.  At the bottom of the page there is
a dropdown from the dropdown select *Export MealMaster* A file will be downloaded to your computer with the exported
recipes.

Export all Recipes
===================
To export all the recipes on your site to the MealMaster format, you will need to run a command from the directory you
installed OpenEats2.  Activate your virtualenv, see :ref:`virtualenv-label` then run the following command from the
OpenEats2 directory::

    ./manage.py export_recipes > recipe.txt

This will create a file called recipe.txt which will contain all the recipes on your site in the MealMaster format