from django.contrib import admin
from models import Entry
from reversion.admin import VersionAdmin

class EntryAdmin(VersionAdmin):
     search_fields = ['title',]
     class Media:
        js = ['/site-media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/site-media/js/tinymce_setup.js',]

admin.site.register(Entry, EntryAdmin)