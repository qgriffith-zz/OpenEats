from django import template

from openeats.recipe_groups.models import Course, Cuisine


register = template.Library()

@register.inclusion_tag('sidebar/browse.html', takes_context=True)  # get the request context so the sidebar templates have access to the session data
def browse_tag(context):
    courses = Course.objects.all()
    cuisines = Cuisine.objects.all()
    course_list = []
    cuisine_list = []

    for course in courses:
        if course.recipe_count() > 0:  # check to see there is at least one recipe
            course_list.append(course)
    for cuisine in cuisines:
        if cuisine.recipe_count() > 0:
            cuisine_list.append(cuisine)
    return {'course_list': course_list, 'cuisine_list': cuisine_list, "request": context['request']}

