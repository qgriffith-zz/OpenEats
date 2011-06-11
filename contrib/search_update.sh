#!/bin/bash

#############################################################################
# This script will update your search index. To schedule this on            #
# a regular bases you can run it from CRON                                  #
#                                                                           #
#  Instructions:                                                            #
#                                                                           #
#  Set vwrapper to the path of your virtualenvwrapper_bashrc script most    #
#  installs will have it located at /usr/local/bin/virtualenvwrapper_bashrc #
#                                                                           #
#  Set WORKON_HOME to the location you created your virtenv directory       #
#                                                                           #
#  Set oevirt to the name of the virtenv you created for OpenEats2          #
#                                                                           #
#  Set oedir to the full path of where you installed OpenEats2              #
#                                                                           #
#                                                                           #
#############################################################################




vwrapper=''
WORKON_HOME=''
oevirt=''
oedir=''

source $vwrapper
workon $oevirt

echo 'updating index..............'

cd $oedir
python ./manage.py update_index




