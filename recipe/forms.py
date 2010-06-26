from django.forms import ModelForm
from django.template.loader import render_to_string
from models import Recipe, RecipeIngredient
from recipe_groups.models import Course
import django.forms as forms


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
    course = forms.ModelChoiceField(Course.objects, widget=SelectWithPop)
    class Meta:
        model = Recipe
        exclude=('slug','ingredient')


