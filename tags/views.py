from taggit.models import Tag, TaggedItem
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def recipeTag(request,tag):
    '''displays a list of recipes with a giving tag'''
    pass
