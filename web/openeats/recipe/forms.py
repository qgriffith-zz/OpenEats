from django.forms import ModelForm
from django.template.loader import render_to_string
import django.forms as forms
from django.forms.models import BaseInlineFormSet
from django.core.mail import EmailMessage, BadHeaderError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.http import HttpResponse

from openeats.recipe.models import Recipe
from openeats.recipe_groups.models import Course, Cuisine


class SelectWithPop(forms.Select):
    """
    Add's a link to a select box to popup a form to allow you to add new items
    to a select box via a form. You need to include the js RelatedObjectLookups
    on the main form
    """
    def render(self, name, * args, ** kwargs):
        html = super(SelectWithPop, self).render(name, * args, ** kwargs)
        popupplus = render_to_string("recipe_groups/popupplus.html", {'field': name})
        return html + popupplus


class RecipeForm(ModelForm):
    """ Used to create new recipes the course and cuisine field are created with a
        speical widget that appends a link and graphic to the end of select field to allow
        users to add new items via a popup form
    """
    course = forms.ModelChoiceField(Course.objects, widget=SelectWithPop)
    cuisine = forms.ModelChoiceField(Cuisine.objects, widget=SelectWithPop)

    class Meta:
        model = Recipe
        exclude=('slug', 'ingredient')


class IngItemFormSet(BaseInlineFormSet):
    """Require at least two ingredient in the formset to be completed."""
    def clean(self):
        super(IngItemFormSet, self).clean()
        for error in self.errors:
            if error:
                return
        completed = 0
        for cleaned_data in self.cleaned_data:
            if cleaned_data and not cleaned_data.get('DELETE', False):
                completed += 1
        if completed < 2:
            raise forms.ValidationError("At least two %s are required." %
                                        self.model._meta.object_name.lower())


class RecipeSendMail(forms.Form):
    """Recipe form to send a recipe via email"""
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request must be supplies'")
        super(RecipeSendMail, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request

    to_email = forms.EmailField(widget=forms.TextInput(), label=_('email address'))
    id = forms.CharField(widget=forms.HiddenInput())
    #from_site = Site.objects.get_current()

    def _get_recipe(self):
        if self.is_valid():
            recipe = Recipe.objects.get(pk=self.cleaned_data['id'])
            self.recipe = recipe
            return self.recipe
        else:
            raise ValueError(_('Can not get the recipe id from invalid form data'))


    def get_body(self):
        """get the recipe and return the message body for the email"""
        template_name = 'recipe/recipe_mail_body.html'  # template that contains the email body and also shared by the grocery print view
        message = loader.render_to_string(template_name, {'recipe': self._get_recipe()}, context_instance=RequestContext(self.request))
        return message

    def get_toMail(self):
        """gets the email to send the list to from the form"""
        if self.is_valid():
            return self.cleaned_data['to_email']
        else:
            raise ValueError(_('Can not get to_email from invalid form data'))

    def save(self, fail_silently=False):
        """ sends the email message"""
        self.subject = _(str(self.from_site) + ' recipe: ' + self._get_recipe().title)
        self.from_email =  self.request.user.email
        if self.subject and self.get_body() and self.from_email:
            try:
                msg = EmailMessage(self.subject, self.get_body(), self.from_email, [self.get_toMail()])
                msg.content_subtype = 'html'
                msg.send()
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            return HttpResponse(_('Email Sent'))
        else:
            return HttpResponse('Make sure all fields are entered and valid.')