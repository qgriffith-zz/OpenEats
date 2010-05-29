from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import Recipe

'''def index(request):
    recipes = get_list_or_404(Recipe.objects.order_by('pub_date', 'title')[:10])
    return render_to_response('recipe/index.html', {'recipes':recipes},context_instance=RequestContext(request))'''

