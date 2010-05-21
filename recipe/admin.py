from django.contrib import admin
from models import Recipe
from reversion.admin import VersionAdmin

class RecipeAdmin(VersionAdmin):
    prepopulated_fields = { 'slug' : ['title']}

admin.site.register(Recipe, RecipeAdmin)
