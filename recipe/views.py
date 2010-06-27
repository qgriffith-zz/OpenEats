from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory, inlineformset_factory
from models import Recipe, RecipeIngredient
from ingredient.models import Ingredient
from forms import RecipeForm

'''def index(request):
    recipes = get_list_or_404(Recipe.objects.order_by('pub_date', 'title')[:10])
    return render_to_response('recipe/index.html', {'recipes':recipes},context_instance=RequestContext(request))'''

@login_required
def recipe(request):        
    IngFormSet = inlineformset_factory(Recipe, RecipeIngredient, extra=5)
    if request.method=='POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = IngFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            new_recipe = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.recipe_id = new_recipe.id
                instance.save()
            return redirect(new_recipe.get_absolute_url())
    else:
        form = RecipeForm()
        formset = IngFormSet(queryset=RecipeIngredient.objects.none())
    return render_to_response('recipe/recipe_form.html', {'form': form, 'formset' : formset,}, context_instance=RequestContext(request))

