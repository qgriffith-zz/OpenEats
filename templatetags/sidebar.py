from django import template
from openeats.recipe_groups.models import Course,Cuisine
from itertools import chain
register = template.Library()

@register.inclusion_tag('sidebar/browse.html')
def browse_tag():
    browse_list = ()
    course_list = Course.objects.all()
    cuisine_list = Cuisine.objects.all()
    browse_list = list(chain(course_list, cuisine_list))
    sorted(browse_list)
    return {'browse_list':browse_list}

