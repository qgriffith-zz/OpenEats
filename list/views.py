from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from models import GroceryList

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
