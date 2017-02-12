from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView


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

    return render(request, 'accounts/signIn_page.html')


def create_profile(request, form_class=None, success_url=None,
                   template_name='profiles/create_profile.html',
                   extra_context=None):
    """Create a profile for the current user, if one doesn't already exist."""

    try:
        profile_obj = request.user.profile
        return HttpResponseRedirect(reverse('profiles_edit_profile'))
    except ObjectDoesNotExist:
        pass

    #
    # We set up success_url here, rather than as the default value for
    # the argument. Trying to do it as the argument's default would
    # mean evaluating the call to reverse() at the time this module is
    # first imported, which introduces a circular dependency: to
    # perform the reverse lookup we need access to profiles/urls.py,
    # but profiles/urls.py in turn imports this module.
    #

    if success_url is None:
        success_url = reverse('profiles_profile_detail',
                              kwargs={ 'username': request.user.username })
    if form_class is None:
        form_class = utils.get_profile_form()
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()

    return render(request, template_name, { 'form': form })

@login_required
def edit_profile(request, form_class=None, success_url=None,
                 template_name='profiles/edit_profile.html',
                 extra_context=None):
    """Edit the current user's profile."""
    try:
        profile_obj = request.user.profile
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))

    if success_url is None:
        success_url = reverse('profiles_profile_detail', kwargs={ 'username': request.user.username })
    if form_class is None:
        form_class = utils.get_profile_form()
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(instance=profile_obj)

    return render(request, template_name,{ 'form': form, 'profile': profile_obj, } )


def profile_detail(request, username, public_profile_field=None,
                   template_name='profiles/profile_detail.html',
                   extra_context=None):
    """Detail view of a user's profile."""

    user = get_object_or_404(User, username=username)
    try:
        profile_obj = user.profile
    except ObjectDoesNotExist:
        raise Http404
    if public_profile_field is not None and \
       not getattr(profile_obj, public_profile_field):
        profile_obj = None

    return render(request, template_name, { 'profile': profile_obj })


class ProfileListView(ListView):
    """A list of user profiles."""

    public_profile_field = None
    template_name = 'profiles/profile_list.html'

    def get_model(self):
        return utils.get_profile_model()

    def get_queryset(self):
        queryset = self.get_model()._default_manager.all()
        if self.public_profile_field is not None:
            queryset = queryset.filter(**{self.public_profile_field: True})
        return queryset
