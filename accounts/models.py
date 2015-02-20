from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserProfiles(models.Model):
    """UserProfile fields extends the user model by adding extra fields tied to a users profile"""
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    user = models.ForeignKey(User, verbose_name=_('user'), unique=True)
    about = models.TextField(_('about'), blank=True,default="Tell everyone something about yourself")
    gender = models.CharField(_('gender'), max_length=5, choices=GENDER_CHOICES, help_text="What are ya?", null=True, default='None')
    url = models.URLField(_('url'), blank=True)
    location = models.CharField(_('location'), max_length=150, blank=True, default='')
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _('User profiles')
        
    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})

    get_absolute_url = models.permalink(get_absolute_url)