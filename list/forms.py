from django.forms import ModelForm
import django.forms as forms
from models import GroceryList
from django.forms.models import BaseInlineFormSet

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



