from datetime import date

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _

from openeats.recipe.models import Recipe
from openeats.list.models import GroceryList, GroceryItem, GroceryShared, GroceryAisle, GroceryRecipe
from openeats.list.forms import GroceryListForm, GroceryItemFormSet, GroceryUserList, GrocerySendMail, GroceryShareTo, GroceryAisleForm


@login_required
def index(request):
    """returns a list of grocery list for a user"""
    glist = GroceryList.objects.filter(author=request.user).order_by('-pub_date')
    gshared = GroceryShared.objects.filter(shared_to=request.user).order_by('-list__pub_date')
    return render(request, 'list/grocery_index.html', {'glists': glist, 'gshared': gshared})


@login_required
def groceryDelete(request, id):
    """ takes the id of a list andremoves a users grocery list"""
    list = get_object_or_404(GroceryList, author=request.user, id=id)
    list.delete()
    output = _('Your grocery list has been removed.')
    messages.success(request, output)
    return HttpResponseRedirect(reverse('grocery_list'))

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
    """used to create and edit grocery list"""
    if user:
        owner = User.objects.get(username=user)  # setting the owner of the list instead of using request.user because if a list is shared request.user won't be the owner
    else:
        owner = request.user  # must be coming in to create a new list and not edit another one this is the only way user wouldn't be passed

    ItemFormSet = inlineformset_factory(GroceryList, GroceryItem, fields='__all__', extra=1, formset=GroceryItemFormSet, can_delete=True)
    if user and slug:  # must be editing a list that is already created
        cur_list = get_object_or_404(GroceryList, author=owner, slug=slug)

        if owner.id != request.user.id:  # if the person is the the owner check if the list is shared to the user
            shared = GroceryShared.objects.filter(list=cur_list)  # check to see if this list is shared
            if shared:
                if shared[0].shared_to_id != request.user.id:
                    output = _('You do not have permissions to edit this list ')
                    messages.error(request, output)
                    return redirect('grocery_list')
            else:
                output = _('You do not have permissions to edit this list ')
                messages.error(request, output)
                return redirect('grocery_list')

    else:
        cur_list = GroceryList()

    if request.method == 'POST':

        form = GroceryListForm(request.POST, instance=cur_list)
        formset = ItemFormSet(request.POST, instance=cur_list, user=owner)
        if form.is_valid() and formset.is_valid():
            new_list = form.save()
            instances = formset.save(commit=False)  # save the items separately
            for instance in instances:
                instance.list_id = new_list.id  # set the grocery id foreign key to the this grocery id
                instance.save()

            return redirect('grocery_show', user=new_list.author, slug=new_list.slug)
    else:
        form = GroceryListForm(instance=cur_list)
        formset = ItemFormSet(instance=cur_list, user=owner)

    return render(request, 'list/grocerylist_form.html', {'form': form, 'formset': formset, 'user': owner})


@login_required
def groceryShow(request, slug, user, template_name='list/grocery_detail.html'):
    """get the users grocery list and show it to them"""
    owner = User.objects.get(username=user)
    list = get_object_or_404(GroceryList, slug=slug, author=owner)
    if owner.id != request.user.id:  # if the person is the the owner check if the list is shared to the user
        shared = GroceryShared.objects.filter(list=list)  # check to see if this list is shared
        if shared:
            if shared[0].shared_to_id != request.user.id:
                output = _('You do not have permissions to view this list ')
                messages.error(request, output)
                return redirect('grocery_list')
        else:
            output = _('You do not have permissions to view this list ')
            messages.error(request, output)
            return redirect('grocery_list')

    return render(request, template_name, {'list': list})


@login_required
def groceryProfile(request):
    """Returns a list of a users grocery list to be displayed on the users profile"""
    list = GroceryList.objects.filter(author=request.user)
    return render(request, 'list/grocery_ajax.html', {'lists': list})


@login_required
def groceryAddRecipe(request, recipe_slug):
    """Takes a recipe and adds all the ingredients from that recipe to a grocery list"""
    if request.method == 'POST':
        # not validating the form since the form is only a prepopulated drop box and can't really be validated
        if request.POST['lists'] == '0':  # must of selected to create a new list because no id can be set to zero otherwise
            list = GroceryList()
            list.title = date.today()
            list.author = request.user
            list.save()
        else:
            list = get_object_or_404(GroceryList, pk=request.POST['lists'], author=request.user)
        recipe = get_object_or_404(Recipe, pk=request.POST['recipe_id'])

        new_groceryRecipe = GroceryRecipe()  # save the recipe added to the grocery list
        new_groceryRecipe.recipe_id = recipe.id
        new_groceryRecipe.list_id = list.id
        new_groceryRecipe.save()

        for ing in recipe.ingredients.all():
            new_item = GroceryItem()
            new_item.list_id = list.id
            new_item.item = str(ing.quantity) + ' ' + str(ing.measurement) + ' ' + ing.title
            new_item.save()

        if recipe.related:
            new_groceryRecipe = GroceryRecipe()
            new_groceryRecipe.recipe_id = recipe.related.id
            new_groceryRecipe.list_id = list.id
            new_groceryRecipe.save()
            for ing in recipe.related.ingredients.all():
                new_item = GroceryItem()
                new_item.list_id = list.id
                new_item.item = str(ing.quantity) + ' ' + str(ing.measurement) + ' ' + ing.title
                new_item.save()

        return redirect('grocery_edit', user=list.author, slug=list.slug)
    else:
        recipe = get_object_or_404(Recipe, slug=recipe_slug)
        form = GroceryUserList(user=request.user)

        return render(request, 'list/grocery_addrecipe.html', {'form': form, 'recipe': recipe})


@login_required
def groceryShareList(request, user, slug):
    list = get_object_or_404(GroceryList, slug=slug, author=request.user)
    if request.method == 'POST':
        shared_list = GroceryShared(list=list)
        form = GroceryShareTo(request.POST, instance=shared_list)
        if form.is_valid():
            form.save()
            output = _('Your grocery list has been shared.')
            messages.success(request, output)
            return redirect('grocery_show', user=request.user, slug=slug)
    else:
        form = GroceryShareTo()
        form.fields['shared_to'].queryset = request.user.relationships.followers()  # only allow people who are following a user to be allowed to have list shared to them
    return render(request, 'list/grocery_share.html', {'form': form, 'list': list})


@login_required
def groceryUnShareList(request, user, slug):
    list = GroceryList.objects.get(slug=slug)
    shared_list = get_object_or_404(GroceryShared, list=list)
    if shared_list.shared_to == request.user or shared_list.shared_by == request.user:
        shared_list.delete()
        output = _("Grocery List has been un-shared")
        messages.success(request, output)
    return redirect('grocery_list')


def groceryMail(request, gid):
    """this view creates a form used to send a grocery list to someone via email"""
    if request.method == 'POST':
        form = GrocerySendMail(data=request.POST, request=request)  # passing the request object so that in the form I can get the request post dict to save the form
        if form.is_valid():
            form.save(fail_silently=False)
            return HttpResponse("grocery list mail sent to " + request.POST['to_email'])
    else:
        form = GrocerySendMail(request=request)
    return render(request, 'list/grocery_email.html', {'form': form, 'gid': gid})


@login_required
def groceryAisle(request):
    """used by users to manage their grocery aisles """
    aisles = GroceryAisle.objects.filter(author=request.user)
    grocery_aisle = GroceryAisle()
    grocery_aisle.author = request.user
    if request.method == "POST":
        form = GroceryAisleForm(request.POST, instance=grocery_aisle)

        if form.is_valid():
            form.save()
            output = _("New Aisle added")
            messages.success(request, output)
            return redirect('grocery_aisle')
    else:
        form = GroceryAisleForm(instance=grocery_aisle)

    return render(request, 'list/groceryaisle_form.html', {'form': form, 'aisles': aisles})


@login_required
def groceryAisleAjaxDelete(request):
    aisles = GroceryAisle.objects.filter(author=request.user)
    if request.method == 'POST':
        if request.POST['id']:
            try:
                aisle = get_object_or_404(GroceryAisle, author=request.user, id=request.POST['id'])
            except GroceryList.DoesNotExist:
                raise Http404
            aisle.delete()
    return render(request, "list/_aisles.html", {'aisles': aisles})