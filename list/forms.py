from django.forms import ModelForm
import django.forms as forms
from models import GroceryList

class GroceryListForm(ModelForm):
    '''used to create a new grocery list for a user'''
    class Meta:
        model = GroceryList
        exclude=('slug')