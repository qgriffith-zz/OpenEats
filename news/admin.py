from django.contrib import admin
from models import Entry
from django.conf import settings


class EntryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'frontpage', 'pub_date']

    class Media:
        js = [settings.STATIC_URL+'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', settings.STATIC_URL+'js/tinymce_setup.js', ]

admin.site.register(Entry, EntryAdmin)