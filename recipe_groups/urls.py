from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import Course, Cuisine
from django.conf import settings

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
    (r'^cuisine/$', list_detail.object_list, cuisine_info),

)