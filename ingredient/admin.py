from django.contrib import admin
from ingredient.models import Ingredient

class IngredientAdmin(admin.ModelAdmin):
    ordering = ['title']

admin.site.register(Ingredient, IngredientAdmin)

