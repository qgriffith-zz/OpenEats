from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Ingredient(models.Model):
     title = models.CharField(max_length=250)
     slug = models.SlugField(unique=True, blank=True)
     author = models.ForeignKey(User, blank=True, null=True)
 
     class Meta:
         ordering = ['title']

     def __unicode__(self):
        return self.title
 
     def save(self, *args, **kwargs):
         if(not self.id) and (not self.slug):
             self.slug = slugify(self.title)
         super(Ingredient, self).save(*args, **kwargs)
         
     def get_absolute_url(self):
         return "/ingredient/%s" %self.slug



