from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from openeats.news.models import Entry


def entry(request, slug):
    """returns one news entry"""
    entry = get_object_or_404(Entry, slug=slug)
    return render(request, 'news/entry.html', {'entry': entry})


def list(request):
    """returns a list of news stories"""
    entry_list = Entry.objects.all().order_by('pub_date')
    return render(request, 'news/entry_list.html', {'entry_list': entry_list})