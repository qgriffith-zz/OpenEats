from django.contrib import admin
from models import Recipe, RecipeIngredient
from reversion.admin import VersionAdmin

class RecipeInline(admin.TabularInline):
    model = RecipeIngredient

class RecipeAdmin(VersionAdmin):
    prepopulated_fields = { 'slug' : ['title']}
    inlines = [RecipeInline,]

admin.site.register(Recipe, RecipeAdmin)
