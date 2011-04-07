from accounts.models import UserProfiles
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def createUserProfile(sender, instance, **kwargs):
    """Listens to the save signal of the User class then 
       create a UserProfile object each time a User is activated ; and link it.
    """
    UserProfiles.objects.get_or_create(user=instance)

post_save.connect(createUserProfile, sender=User)

