from django.http import HttpResponse
from django.utils import simplejson
from models import Ingredient


def autocomplete_ing(request):
    q = request.GET.get('term', '')
    ing_list = Ingredient.objects.filter(title__istartswith=q).values_list('title').distinct().order_by('title')[:10]
    results = []
    for ing_item in ing_list:
        results.append(" ".join(ing_item))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype="application/json")

