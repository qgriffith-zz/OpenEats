from django.contrib import admin
from models import Recipe, StoredRecipe, NoteRecipe
from ingredient.models import Ingredient
from reversion.admin import VersionAdmin
from forms import IngItemFormSet

class RecipeInline(admin.TabularInline):
    model = Ingredient
    formset=IngItemFormSet

class RecipeAdmin(VersionAdmin):
    prepopulated_fields = { 'slug' : ['title']}
    inlines = [RecipeInline,]
    list_display = ['title','admin_thumbnail_view', 'author', 'pub_date', 'shared']
    list_filter = ['shared', 'author', 'course', 'cuisine']
    search_fields = ['author__username', 'title',]
    radio_fields = {"shared": admin.HORIZONTAL}
    class Media:
        js = ['/site_media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/site_media/js/tinymce_setup.js',]

class StoredRecipeAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    search_fields = ['user__username', 'recipe__title']
    list_filter = ['user',]

class NoteRecipeAdmin(admin.ModelAdmin):
    list_filter = ('recipe', 'author')
    list_display = ('recipe', 'author')
    search_fields = ['author__username', 'recipe']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(StoredRecipe, StoredRecipeAdmin)
admin.site.register(NoteRecipe, NoteRecipeAdmin)