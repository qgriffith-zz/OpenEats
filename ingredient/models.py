from django.db import models
from recipe.models import Recipe


class Ingredient(models.Model):
     title = models.CharField(max_length=250)
     quantity =  models.IntegerField()
     measurement = models.CharField(max_length=200)
     preparation = models.CharField(max_length=100, blank=True, null=True)
     recipe    = models.ForeignKey(Recipe)
 
     class Meta:
         ordering = ['title']

     def __unicode__(self):
        return self.title
