from django.forms import ModelForm, forms
import django.forms as forms
from models import GroceryList
from django.forms.models import BaseInlineFormSet
from recipe.models import Recipe

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
        self.fields['lists'] = forms.ChoiceField(choices=[ (o.id, str(o)) for o in lists])
