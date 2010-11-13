from django import template
from openeats.recipe_groups.models import Course,Cuisine
from itertools import chain
register = template.Library()

@register.inclusion_tag('sidebar/browse.html')
def browse_tag():
    course_list = Course.objects.all()
    cuisine_list = Cuisine.objects.all()
    return {'course_list':course_list, 'cuisine_list':cuisine_list}

