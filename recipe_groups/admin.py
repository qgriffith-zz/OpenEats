from django.contrib import admin
from models import Course, Cuisine

class CourseAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title', 'author']
    list_filter = ['author',]
    prepopulated_fields = { 'slug' : ['title']}

class CuisineAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title', 'author']
    list_filter = ['author',]
    prepopulated_fields = { 'slug' : ['title']}

admin.site.register(Course, CourseAdmin)
admin.site.register(Cuisine, CuisineAdmin)