from django.db import models
from django.contrib.auth.models import User

class UserProfiles(models.Model):
    user = models.ForeignKey(User, unique=True)
    about = models.TextField(blank=True,default="Tell everyone something about yourself")
    url = models.URLField("Website", blank=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    get_absolute_url = models.permalink(get_absolute_url)


