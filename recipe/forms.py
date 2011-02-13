from django.forms import ModelForm
from django.template.loader import render_to_string
from models import Recipe
from recipe_groups.models import Course, Cuisine
import django.forms as forms
from django.forms.models import BaseInlineFormSet

class SelectWithPop(forms.Select):
    '''
    Add's a link to a select box to popup a form to allow you to add new items
    to a select box via a form. You need to include the js RelatedObjectLookups
    on the main form
    '''
    def render(self, name, * args, ** kwargs):
        html = super(SelectWithPop, self).render(name, * args, ** kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name})
        return html + popupplus

class RecipeForm(ModelForm):
    ''' Used to create new recipes the course and cuisine field are created with a
        speical widget that appends a link and graphic to the end of select field to allow
        users to add new items via a popup form
    '''
    course = forms.ModelChoiceField(Course.objects, widget=SelectWithPop)
    cuisine = forms.ModelChoiceField(Cuisine.objects, widget=SelectWithPop)
    class Meta:
        model = Recipe
        exclude=('slug','ingredient')

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
