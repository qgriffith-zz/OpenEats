from django.contrib import admin
from models import Entry
from reversion.admin import VersionAdmin

class EntryAdmin(VersionAdmin):
     prepopulated_fields = { 'slug' : ['title']}
     search_fields = ['title',]
     class Media:
        js = ['/site_media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/site_media/js/tinymce_setup.js',]

admin.site.register(Entry, EntryAdmin)