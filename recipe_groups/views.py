from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import Course, Cuisine
from recipe.models import Recipe
from django.contrib.auth.decorators import login_required
from forms import CoursePopForm, CuisinePopForm
from helpers.form_helper import handlePopAdd


def course_recipes(request, slug):
    '''Rectrives the recipe objects in a list that belong to the course passed to the method'''
    course_object = get_object_or_404(Course, slug=slug)
    recipe_list = course_object.recipe_set.filter(shared=Recipe.SHARE_SHARED)
    
    return render_to_response('recipe_groups/recipe_list.html', {'recipe_list':recipe_list, 'catagory': course_object.title},context_instance=RequestContext(request) )

def cuisine_recipes(request, slug):
    '''Retrives the recipe objects in a list that belong to the cuisnie passed to the method'''
    cuisine_object = get_object_or_404(Cuisine, slug=slug)
    recipe_list = cuisine_object.recipe_set.filter(shared=Recipe.SHARE_SHARED)
       
    return render_to_response('recipe_groups/recipe_list.html', {'recipe_list':recipe_list, 'catagory': cuisine_object.title},context_instance=RequestContext(request))

@login_required
def course_pop(request):
    '''Is called via js from the recipe form to allow users to add a new course with out leaving the recipe form'''
    return handlePopAdd(request, CoursePopForm, 'course')

@login_required
def cuisine_pop(request):
    '''Is called via js from the recipe form to allow users to add a new cuisine with out leaving the recipe form'''
    return handlePopAdd(request, CuisinePopForm, 'cuisine')