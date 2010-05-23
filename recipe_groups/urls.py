from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import Course, Cuisine

course_info={
                "queryset":Course.objects.all(),
                "template_object_name":"course",
            }
cuisine_info={
                "queryset":Cuisine.objects.all(),
                "template_object_name": "cuisine",
             }
urlpatterns = patterns('',
    (r'^course/$', list_detail.object_list, course_info ),
    url(r'^course/(?P<slug>[-\w]+)/$', 'openeats.recipe_groups.views.course_recipes', name="course_recipes"),
    (r'^cuisine/$', list_detail.object_list, cuisine_info),
    url(r'^cuisine/(?P<slug>[-\w]+)/$', 'openeats.recipe_groups.views.cuisine_recipes', name="cuisine_recipes"),

)