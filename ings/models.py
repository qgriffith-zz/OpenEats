from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Ingredient(models.Model):
     title = models.CharField(max_length=250)
     slug = models.SlugField(unique=True, blank=True)
     author = models.ForeignKey(User)

     class Meta:
         ordering = ['title']

     def __unicode__(self):
        return self.title
    

