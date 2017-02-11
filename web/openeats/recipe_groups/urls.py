from django.conf.urls import url

from openeats.recipe_groups.views import CourseList, CuisineList, CuisineCreate, CuisineUpdate, CourseCreate, CourseUpdate
from openeats.recipe_groups.models import Course, Cuisine
from openeats.recipe_groups import views


course_info = {
                "queryset":Course.objects.all(),
                "template_object_name":"course",
            }
cuisine_info = {
                "queryset":Cuisine.objects.all(),
                "template_object_name": "cuisine",
             }
urlpatterns = [
    url(r'^popadd/course/$', views.course_pop),
    url(r'^course/$', CourseList.as_view(), name="course_list"),
    url(r'^course/new/$', CourseCreate.as_view(), name='course_add'),
    url(r'^course/(?P<slug>[-\w]+)/$', views.course_recipes, name="course_recipes"),
    url(r'^popadd/cuisine/$', views.cuisine_pop),
    url(r'^cuisine/$', CuisineList.as_view()),
    url(r'^cuisine/new/$', CuisineCreate.as_view(), name="cuisine_add"),
    url(r'^cuisine/(?P<slug>[-\w]+)/$', views.cuisine_recipes, name="cuisine_recipes"),
]
