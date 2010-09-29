from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages

def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out!.')
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)