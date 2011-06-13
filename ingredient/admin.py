from django.contrib import admin
from ingredient.models import Ingredient
from reversion.admin import VersionAdmin

class IngredientAdmin(VersionAdmin):
    ordering = ['title', 'recipe']
    list_display = ['title', 'recipe',]
    search_fields = ['title', 'recipe__title',]

admin.site.register(Ingredient, IngredientAdmin)

