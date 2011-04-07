from django.contrib import admin
from models import GroceryList, GroceryItem, GroceryAisle
from forms import GroceryItemFormSet

class GroceryListInline(admin.TabularInline):
    model = GroceryItem
    formset = GroceryItemFormSet
    

class GroceryListAdmin(admin.ModelAdmin):
    inlines = [GroceryListInline,]
    list_display = ['title', 'author']
    list_filter = ['author']
    search_fields = ['author__username', 'title']
    ordering = ['author__username', 'title']

class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ['list', 'item']
    list_filter = ['list']
    ordering = ['list', 'item']
    search_fields = ['list']

class GroceryAisleAdmin(admin.ModelAdmin):
    ordering = ['aisle']

admin.site.register(GroceryList, GroceryListAdmin)
admin.site.register(GroceryItem, GroceryItemAdmin)
admin.site.register(GroceryAisle, GroceryAisleAdmin)
