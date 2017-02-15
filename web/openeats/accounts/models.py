from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfiles(models.Model):
    """UserProfile fields extends the user model by adding extra fields tied to a users profile"""
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    user = models.OneToOneField(User,related_name='profile', verbose_name=_('user'))
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfiles.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
