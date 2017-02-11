from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import mail_admins

from openeats.accounts.models import UserProfiles
from openeats.recipe.models import ReportedRecipe


def createUserProfile(sender, instance, **kwargs):
    """Listens to the save signal of the User class then 
       create a UserProfile object each time a User is activated ; and link it.
    """
    UserProfiles.objects.get_or_create(user=instance)

post_save.connect(createUserProfile, sender=User)


def notifyAdminReportedRecipe(sender, instance, created, **kwargs):
    """Listens to the save signal for the report recipe class and
        sends an email to the admins
    """
    if created:
        subject = "A recipe has been reported"
        message = "Recipe %s was reported as being inappropriate" % instance.recipe
        mail_admins(subject, message)

post_save.connect(notifyAdminReportedRecipe, sender=ReportedRecipe)