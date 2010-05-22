from django.contrib import admin
from ingredient.models import Ingredient

class IngredientAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug' : ['title']}

admin.site.register(Ingredient, IngredientAdmin)

