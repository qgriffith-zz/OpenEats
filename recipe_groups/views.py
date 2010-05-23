from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from models import Course, Cuisine

def course_recipes(request, slug):
    '''Rectrives the recipe objects in a list that belong to the course passed to the method'''
    #recipe_list = Recipe.objects.filter(course__title__exact=course)
    course_object = get_object_or_404(Course, slug=slug)
    recipe_list = course_object.recipe_set.all();
    return render_to_response('recipe_groups/recipe_list.html', {'recipe_list':recipe_list} )

def cuisine_recipes(request, slug):
    '''Retrives the recipe objects in a list that belong to the cuisnie passed to the method'''
    cuisine_object = get_object_or_404(Cuisine, slug=slug)
    recipe_list = cuisine_object.recipe_set.all();
    return render_to_response('recipe_groups/recipe_list.html', {'recipe_list':recipe_list})