from django.contrib import admin
from models import UserProfiles

class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfiles, ProfileAdmin)
