from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, Http404
from models import Recipe, StoredRecipe, NoteRecipe
from ingredient.models import Ingredient
from forms import RecipeForm,IngItemFormSet
from djangoratings.views import AddRatingView
from django.utils import simplejson
from django.db.models import F

def index(request):
    recipe_list = Recipe.objects.filter(shared=Recipe.SHARE_SHARED).exclude(photo='').order_by('-pub_date')[0:6]
    return render_to_response('recipe/index.html', {'new_recipes' : recipe_list}, context_instance=RequestContext(request))

def recipeShow(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    #setting the four previously viewed recipes in the user session so they can be easily accessed on the sidebar
    if 'recipe_history' in request.session:
       sessionlist = request.session['recipe_history']
       if [recipe.title, recipe.get_absolute_url()] not in sessionlist:
            sessionlist.append(([recipe.title, recipe.get_absolute_url()]))
            if len(sessionlist) > 4:
                sessionlist.pop(0)
            request.session['recipe_history'] = sessionlist
    else:
        request.session['recipe_history'] = [[recipe.title, recipe.get_absolute_url()]]

    if request.user.is_authenticated():
        note = request.user.noterecipe_set.filter(recipe=recipe, author=request.user)
    else:
        note = None
    
    if recipe.shared == Recipe.PRIVATE_SHARED and recipe.author != request.user: #check if the recipe is a private recipe if so through a 404 error
        raise Http404("Recipe %s is marked Private"  % recipe.slug)
    else:
        return render_to_response('recipe/recipe_detail.html', {'recipe': recipe, 'note': note}, context_instance=RequestContext(request))
    
def recipePrint(request, slug):
     recipe = get_object_or_404(Recipe, slug=slug)

     if request.user.is_authenticated():
        note = request.user.noterecipe_set.filter(recipe=recipe, author=request.user)
     else:
         note = None
     
     if recipe.shared == Recipe.PRIVATE_SHARED and recipe.author != request.user: #check if the recipe is a private recipe if so through a 404 error
        raise Http404("Recipe %s is marked Private"  % recipe.slug)
     else:
        return render_to_response('recipe/recipe_print.html', {'recipe': recipe, 'note': note},context_instance=RequestContext(request))

@login_required
def recipe(request):        
    IngFormSet = inlineformset_factory(Recipe, Ingredient, extra=15, formset=IngItemFormSet) #creat the ingredient form with 15 empty fields
     
    if request.method=='POST':
        form = RecipeForm(data = request.POST, files = request.FILES)
        formset = IngFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            new_recipe = form.save()
            instances = formset.save(commit=False)#save the ingredients seperatly
            for instance in instances:
                instance.recipe_id = new_recipe.id #set the recipe id foregin key to the this recipe id
                instance.save()
            return redirect(new_recipe.get_absolute_url())
    else:
        form = RecipeForm()
        form.fields['related'].queryset =  Recipe.objects.filter(author__username=request.user.username).exclude(related = F('id')).filter(related__isnull=True).order_by('-pub_date')[:5]
        formset = IngFormSet(queryset=Ingredient.objects.none())
    return render_to_response('recipe/recipe_form.html', {'form': form, 'formset' : formset,}, context_instance=RequestContext(request))

def recipeUser(request, shared, user):
    '''Returns a list of recipes for a giving user if shared is set to share then it will show the shared recipes if it is set to private
       then only the private recipes will be shown this is mostly used for the users profile to display the users recipes
    '''
    if shared =='share':
        recipe_list = Recipe.objects.filter(author__username=user, shared = Recipe.SHARE_SHARED)
    else:
        recipe_list = Recipe.objects.filter(author__username=user, shared = Recipe.PRIVATE_SHARED)
       
    return render_to_response('recipe/recipe_userlist.html', {'recipe_list': recipe_list, 'user': user, 'shared': shared}, context_instance=RequestContext(request))

@login_required
def recipeRate(request, object_id, score):
    ''' Used for users to rate recipes '''
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
    '''Take the recipe id and the user id passed via the url check that the recipe is not
       already stored for that user then store it if it is
    '''
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
    '''Take the recipe id via the url check that the recipe is not already
       stored for that user then remove it if it is
    '''
    if request.method == 'POST':
        if request.POST['recipe_id']:
            try:
                stored_recipe = StoredRecipe.objects.get(recipe=request.POST['recipe_id'], user=request.user.id)
            except StoredRecipe.DoesNotExist:
                raise Http404
            stored_recipe.delete()
            return redirect('/recipe/ajax-favrecipe/')
    

@login_required
def recipeUserFavs(request):
    '''returns a list of a users favorite recipes'''
    stored_list = StoredRecipe.objects.filter(user=request.user.id)
    recipe_list = []
    for stored in stored_list:
        recipe_list.append(stored.recipe)
    return render_to_response('recipe/recipe_userfav.html', {'recipe_list': recipe_list}, context_instance=RequestContext(request))

@login_required
def recipeNote(request):
    '''This is called by the jquery inline edit on the recipe detail template to allow users to add notes to recipes'''

    user = request.user
    
    if request.POST['recipe']:
        try:
            recipe = Recipe.objects.get(pk=request.POST['recipe'])
        except Recipe.DoesNotExist:
            raise Http404
        note = request.POST['note']

    cur_note = NoteRecipe.objects.filter(author=user, recipe=recipe)

    if cur_note: #check to see if the user already has a note if so re-save it with the new text
        if len(note) == 0 or note.isspace(): #they must want to delete the note so they sent nothing in the text field
            cur_note[0].delete()
        else:
            cur_note[0].text = note
            cur_note[0].save()
    else:
        if len(note) > 0 and note.isspace() == False:
            new_note = NoteRecipe(recipe=recipe, author=user, text=note)
            new_note.save()
    return HttpResponse(note)

    
