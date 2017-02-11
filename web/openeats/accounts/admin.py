from django.contrib import admin

from openeats.accounts.models import UserProfiles


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'location']
    list_display = ['user', 'pub_date', 'location']

admin.site.register(UserProfiles, ProfileAdmin)
