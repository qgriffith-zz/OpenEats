from django.db import models
from django.contrib.auth.models import User

class UserProfiles(models.Model):
    '''UserProfile fields extends the user model by adding extra fields tied to a users profile'''
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.ForeignKey(User, unique=True)
    about = models.TextField('about',blank=True,default="Tell everyone something about yourself")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="What are ya?", null=True, default='None')
    url = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True, default='')
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    get_absolute_url = models.permalink(get_absolute_url)


