from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _


def logout_page(request):
    """this replaces the normal logout view found in django.contrib.auth with a view that logs the user out and redirects them to the main page
       and displays a message
    """

    logout(request)
    output = _('You have been logged out!.')
    messages.success(request, output)
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def signIn_page(request):
    """This combines the sign in and the create user forms into one page using jquery UI tabs and is called from the nav bar"""

    return render_to_response('accounts/signIn_page.html', context_instance=RequestContext(request))
