from django.contrib import admin
from models import GroceryList, GroceryItem, GroceryAisle
from forms import GroceryItemFormSet

class GroceryListInline(admin.TabularInline):
    model = GroceryItem
    formset = GroceryItemFormSet
    

class GroceryListAdmin(admin.ModelAdmin):
    #prepopulated_fields = { 'slug' : ['title']}
    inlines = [GroceryListInline,]
    list_display = ['title', 'author']
    list_filter = ['author']

class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'list']
    list_filter = ['list']

class GroceryAisleAdmin(admin.ModelAdmin):
    pass

admin.site.register(GroceryList, GroceryListAdmin)
admin.site.register(GroceryItem, GroceryItemAdmin)
admin.site.register(GroceryAisle, GroceryAisleAdmin)
