from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from recipe.models import Recipe
from models import GroceryList, GroceryItem
from forms import GroceryListForm, GroceryItemFormSet,GroceryUserList,GrocerySendMail
from datetime import date

@login_required
def index(request):
    '''returns a list of grocery list for a user'''
    glist = GroceryList.objects.filter(author=request.user)
    return render_to_response('list/grocery_index.html', {'glists' : glist}, context_instance=RequestContext(request))

@login_required
def groceryDelete(request, id):
    ''' takes the id of a list andremoves a users grocery list'''
    list = get_object_or_404(GroceryList, author=request.user, id=id)
    list.delete()
    messages.success(request, 'Your grocery list has been removed.')
    return HttpResponseRedirect(reverse('list.views.index'))

@login_required
def groceryAjaxDelete(request):

    if request.method == 'POST':
        if request.POST['id']:
            try:
                list = get_object_or_404(GroceryList, author=request.user, id=request.POST['id'])
            except GroceryList.DoesNotExist:
                raise Http404
            list.delete()
            return redirect("/list/grocery/grocery-ajax/")


@login_required
def groceryCreate(request, user=None, slug=None):
    '''used to create and edit grocery list'''
    ItemFormSet = inlineformset_factory(GroceryList, GroceryItem, extra=15, formset=GroceryItemFormSet, can_delete=True)
    if user and slug:
        cur_list = get_object_or_404(GroceryList, author=request.user, slug=slug)
        
    else:
        cur_list = GroceryList()

    if request.method=='POST':
      
        form = GroceryListForm(request.POST, instance=cur_list)
        formset = ItemFormSet(request.POST, instance=cur_list)
        if form.is_valid() and formset.is_valid():
            new_list = form.save()
            instances = formset.save(commit=False)#save the items seperatly
            for instance in instances:
               instance.list_id = new_list.id #set the grocery id foregin key to the this grocery id
               instance.save()
           
            return redirect('grocery_show', user=new_list.author, slug=new_list.slug)
    else:
        form = GroceryListForm(instance=cur_list)
        formset = ItemFormSet(instance=cur_list)

    return render_to_response('list/grocerylist_form.html', {'form': form, 'formset' : formset,}, context_instance=RequestContext(request))

@login_required
def groceryShow(request, slug, user, template_name='list/grocery_detail.html'):
    '''get the users grocery list and show it to them'''
    list = get_object_or_404(GroceryList, slug=slug, author=request.user) #this will make sure that the user owns the grocery list being requested
   
    return render_to_response(template_name, {'list': list}, context_instance=RequestContext(request))

@login_required
def groceryProfile(request):
    '''Returns a list of a users grocery list to be displayed on the users profile'''
    list = GroceryList.objects.filter(author=request.user)
    return render_to_response('list/grocery_ajax.html', {'lists' : list}, context_instance=RequestContext(request))

@login_required
def groceryAddRecipe(request, recipe_slug):
    '''Takes a recipe and adds all the ingredients from that recipe to a grocery list'''

    if request.method == 'POST':
        #not validating the form since the form is only a prepoulated drop box and can't really be validated
        if request.POST['lists'] == '0':  #must of selected to create a new list because no id can be set to zero otherwise
            list = GroceryList()
            list.title=date.today()
            list.author=request.user
            list.save()
        else:
            list = get_object_or_404(GroceryList, pk=request.POST['lists'], author=request.user)
        recipe = get_object_or_404(Recipe, pk=request.POST['recipe_id'])
        
        for ing in recipe.ingredient_set.all():
            new_item = GroceryItem()
            new_item.list_id = list.id
            new_item.item =  str(ing.quantity) + ' '  + str(ing.measurement) + ' ' + ing.title
            new_item.save()

        return redirect('grocery_edit', user=list.author, slug=list.slug)
    else:
        recipe = get_object_or_404(Recipe, slug=recipe_slug)
        form = GroceryUserList(user=request.user )
       # form.fields['lists'].initial=[0]
        return render_to_response('list/grocery_addrecipe.html', {'form': form, 'recipe' : recipe}, context_instance=RequestContext(request))

def groceryMail(request, gid):
    '''this view creates a form used to send a grocery list to someone via email'''
    if request.method == 'POST':
        form = GrocerySendMail(data=request.POST, request=request) #passing the request object so that in the form I can get the request post dict to save the form
        if form.is_valid():
            form.save(fail_silently=False)
            return HttpResponse("grocery list mail sent to " + request.POST['to_email'])
    else:
        form = GrocerySendMail(request=request)
    return render_to_response('list/grocery_email.html', {'form': form, 'gid': gid}, context_instance=RequestContext(request))




