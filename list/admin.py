from django.contrib import admin
from models import GroceryList, GroceryItem

class GroceryListInline(admin.TabularInline):
    model = GroceryItem

class GroceryListAdmin(admin.ModelAdmin):
    inlines = [GroceryListInline,]
    list_display = ['title', 'author']
    list_filter = ['author']

class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'list']
    list_filter = ['list']

admin.site.register(GroceryList, GroceryListAdmin)
admin.site.register(GroceryItem, GroceryItemAdmin)
