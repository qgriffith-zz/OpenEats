from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Entry


def entry(request, slug):
    """returns one news entry"""
    entry = get_object_or_404(Entry, slug=slug)
    return render_to_response('news/entry.html', {'entry': entry}, context_instance=RequestContext(request))


def list(request):
    """returns a list of news stories"""
    entry_list = Entry.objects.all().order_by('pub_date')
    return render_to_response('news/entry_list.html', {'entry_list': entry_list}, context_instance=RequestContext(request))