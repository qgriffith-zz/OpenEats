from django.contrib import admin
from models import Recipe, RecipeIngredient
from reversion.admin import VersionAdmin

class RecipeInline(admin.TabularInline):
    model = RecipeIngredient

class RecipeAdmin(VersionAdmin):
    prepopulated_fields = { 'slug' : ['title']}
    inlines = [RecipeInline,]
    class Media:
        js = ['/site_media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/site_media/js/tinymce_setup.js',]

admin.site.register(Recipe, RecipeAdmin)
