from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import Course, Cuisine
from django.contrib.auth.decorators import login_required
from forms import CoursePopForm
from helpers.form_helper import handlePopAdd
from django.views.decorators.csrf import csrf_exempt

def course_recipes(request, slug):
    '''Rectrives the recipe objects in a list that belong to the course passed to the method'''
    #recipe_list = Recipe.objects.filter(course__title__exact=course)
    course_object = get_object_or_404(Course, slug=slug)
    recipe_list = course_object.recipe_set.all();
    return render_to_response('recipe_groups/recipe_list.html', {'recipe_list':recipe_list},context_instance=RequestContext(request) )

def cuisine_recipes(request, slug):
    '''Retrives the recipe objects in a list that belong to the cuisnie passed to the method'''
    cuisine_object = get_object_or_404(Cuisine, slug=slug)
    recipe_list = cuisine_object.recipe_set.all();
    return render_to_response('recipe_groups/recipe_list.html', {'recipe_list':recipe_list},context_instance=RequestContext(request))

@login_required
@csrf_exempt
def course_pop(request):
    '''Is called via js from the recipe form to allow users to add a new course with out leaving the recipe form'''
    return handlePopAdd(request, CoursePopForm, 'course')