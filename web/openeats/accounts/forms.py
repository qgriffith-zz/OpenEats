from django.forms import ModelForm
from django import forms
from django.forms.widgets import RadioSelect
from django.contrib.auth.models import User

from openeats.accounts.models import UserProfiles


class ProfileForm(ModelForm):
    """Override the default profile model to add a gender radio select and to
       Allow users to edit their emails on the profile page"""

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass
    email = forms.EmailField(label="email")
   
    class Meta:
        model = UserProfiles
        exclude = ('user',)
        widgets = {
            'gender': RadioSelect(),
        }

    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(ProfileForm, self).save(*args, **kwargs)
        return profile