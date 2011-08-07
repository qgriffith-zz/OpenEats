from django.contrib import admin
from models import GroceryList, GroceryItem, GroceryAisle, GroceryShared
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
    list_display = ['aisle', 'author']
    ordering = ['aisle', 'author__username']
    list_filter = ['author']
    search_fields = ['aurhtor__username', 'aisle']

class GrocerySharedAdmin(admin.ModelAdmin):
    list_display = ['list', 'shared_by']
    list_filter = ['shared_by', 'shared_to']
    search_fields = ['shared_by__username', 'shared_to__username']
    exclude = ['shared_by']
    ordering = ['list']

admin.site.register(GroceryList, GroceryListAdmin)
admin.site.register(GroceryShared, GrocerySharedAdmin)
admin.site.register(GroceryItem, GroceryItemAdmin)
admin.site.register(GroceryAisle, GroceryAisleAdmin)
