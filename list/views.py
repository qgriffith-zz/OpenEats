from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from models import GroceryList

@login_required
def index(request):
    '''returns a list of grocery list for a user'''
    glist = GroceryList.objects.filter(author=request.user)
    return render_to_response('list/grocery_index.html', {'glists' : glist}, context_instance=RequestContext(request))
