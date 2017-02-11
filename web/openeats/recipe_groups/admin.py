from django.contrib import admin

from openeats.recipe_groups.models import Course, Cuisine


class CourseAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title', 'author']
    list_filter = ['author']
    

class CuisineAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title', 'author']
    list_filter = ['author']


admin.site.register(Course, CourseAdmin)
admin.site.register(Cuisine, CuisineAdmin)