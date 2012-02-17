from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from models import Entry

def entry(request, slug):
    entry = get_object_or_404(Entry, slug=slug)
    return render_to_response('news/entry.html', {'entry':entry}, context_instance=RequestContext(request))


