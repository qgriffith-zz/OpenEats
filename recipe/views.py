from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory, inlineformset_factory
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import Recipe
from ingredient.models import Ingredient
from forms import RecipeForm, BaseIngFormSet
import json

'''def index(request):
    recipes = get_list_or_404(Recipe.objects.order_by('pub_date', 'title')[:10])
    return render_to_response('recipe/index.html', {'recipes':recipes},context_instance=RequestContext(request))'''

@login_required
def recipe(request):        
    IngFormSet = inlineformset_factory(Recipe, Ingredient, extra=5)
   # ing_title = Ingredient.objects.values_list('title', flat=True).order_by('title')
  
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
        formset = IngFormSet(queryset=Ingredient.objects.none())
    return render_to_response('recipe/recipe_form.html', {'form': form, 'formset' : formset,}, context_instance=RequestContext(request))

def recipeUser(request, shared, user):
    '''Returns a list of recipes for a giving user'''
    if shared =='share':
        recipe_list = Recipe.objects.filter(author__username=user, shared = Recipe.SHARE_SHARED)
    else:
        recipe_list = Recipe.objects.filter(author__username=user, shared = Recipe.PRIVATE_SHARED)
    '''paginator = Paginator(recipe_list, 10)

     # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        recipes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        recipes = paginator.page(paginator.num_pages)'''
    
    return render_to_response('recipe/recipe_userlist.html', {'recipe_list': recipe_list, 'user': user, 'shared': shared}, context_instance=RequestContext(request))

