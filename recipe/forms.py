from django.forms import ModelForm
from django.template.loader import render_to_string
from models import Recipe
from recipe_groups.models import Course, Cuisine
from ingredient.models import Ingredient
import django.forms as forms
from django.forms.models import BaseModelFormSet

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

class BaseIngFormSet(BaseModelFormSet):
    ''' Used to add an ingredient formset to the recipe form turns the ingredient from a select field to an input field
        that then uses auto complete
    '''
    def add_fields(self, form, index):
        super(BaseIngFormSet, self).add_fields(form,index)
        form.fields["ingredient"] =  forms.CharField()