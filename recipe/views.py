from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory, inlineformset_factory
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404
from models import Recipe, StoredRecipe
from ingredient.models import Ingredient
from forms import RecipeForm, BaseIngFormSet
from djangoratings.views import AddRatingView
from django.utils import simplejson


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

@login_required
def recipeRate(request, object_id, score):
    params = {
        'content_type_id': 16,  #this is the content type id of the recipe models per django.contrib.contentetype
        'object_id': object_id,
        'field_name': 'rating', # this should match the field name defined in your model
        'score': score,
    }
    results = {}
    response = AddRatingView()(request, **params)
    results['message'] = response.content
    r = Recipe.objects.get(pk=object_id) #get recipe object so we can return the average rating
    avg = r.rating.score / r.rating.votes
    results['avg'] = avg
    results['votes'] = r.rating.votes
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype="application/json")

@login_required
def recipeStore(request, object_id):
    '''Take the recipe id and the user id passed via the url check that the recipe is not already stored for that user then store it if it is'''
    stored = StoredRecipe.objects.filter(recipe=object_id, user=request.user.id)
    if stored:
        return HttpResponse("Recipe already in your favorites!")
    else: #save the recipe
        r = get_object_or_404(Recipe, pk=object_id)
        new_store = StoredRecipe(recipe=r, user=request.user)
        new_store.save()
        return HttpResponse("Recipe added to your favorites!")
        

@login_required
def recipeUnStore(request):
    '''Take the recipe id via the url check that the recipe is not already stored for that user then remove it if it is'''
    if request.method == 'POST':
        if request.POST['recipe_id']:
            try:
                stored_recipe = StoredRecipe.objects.get(recipe=request.POST['recipe_id'], user=request.user.id)
            except StoredRecipe.DoesNotExist:
                raise Http404
            stored_recipe.delete()
            return redirect("/recipe/ajax-favrecipe/")
    

@login_required
def recipeUserFavs(request):
    '''returns a list of a users favorite recipes'''
    stored_list = StoredRecipe.objects.filter(user=request.user.id)
    recipe_list = []
    for stored in stored_list:
        recipe_list.append(stored.recipe)
    return render_to_response('recipe/recipe_userfav.html', {'recipe_list': recipe_list}, context_instance=RequestContext(request))



    
