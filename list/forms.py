from django.forms import ModelForm, forms
import django.forms as forms
from django.http import HttpResponse, HttpResponseRedirect
from models import GroceryList
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template import loader, RequestContext
from django.contrib.sites.models import Site

class GroceryListForm(ModelForm):
    '''used to create a new grocery list for a user'''
    class Meta:
        model = GroceryList
        exclude=('slug')

class GroceryItemFormSet(BaseInlineFormSet):
     """Require at least one form in the formset to be completed."""
     def clean(self):
         super(GroceryItemFormSet, self).clean()
         for error in self.errors:
             if error:
                 return
         completed = 0
         for cleaned_data in self.cleaned_data:
             if cleaned_data and not cleaned_data.get('DELETE', False):
                 completed += 1
         if completed < 1:
             raise forms.ValidationError("At least one %s is required." %
                self.model._meta.object_name.lower())



class GroceryUserList(forms.Form):
    '''used to pull a list of a users grocery list and add them to a select box on a form'''
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) #get the user passed to the form off of the keyword argument
        super(GroceryUserList, self).__init__(*args, **kwargs)
        lists = GroceryList.objects.filter(author=user)
        choices=[ (o.id, str(o)) for o in lists]
        choices.append((0,'new'))
        choices.sort()
        self.fields['lists'] = forms.ChoiceField( widget = forms.Select(), choices=choices, initial=0)

class GrocerySendMail(forms.Form):
    '''Grocery form to send a grocery list to someone in email'''
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request must be supplies'")
        super(GrocerySendMail, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request
        #set up the return email address and sender name to the user logged in
        if request.user.is_authenticated():
            self.fields['email'].initial= request.usser.email

    to_email = forms.EmailField(widget=forms.TextInput(),label=_('Your email address'))

    from_email = settings.DEFAULT_FROM_EMAIL
    from_site = Site.objects.get_current()
    subject = _('Grocery list from ' + from_site)
    template_name = 'list/email_body.html' #template that contains the email body
    list = GroceryList.objects.get(pk = request.POST[gid])
    message = loader.render_to_string(template_name, {list: list})

    def save(self, fail_silently=False):
        ''' sends the email message'''
        if self.subject and self.message and self.from_email:
            try:
                send_mail(self.subject, self.message, self.from_email, [self.to_email])
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            return HttpResponse(_('Email Sent'))
        else:
         return HttpResponse('Make sure all fields are entered and valid.')



        

    
