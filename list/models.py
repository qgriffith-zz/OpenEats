from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField


class GroceryList(models.Model):
    title = models.CharField(_("grocery list"), max_length=250)
    slug = AutoSlugField(_('slug'), populate_from='title')
    author = models.ForeignKey(User, verbose_name=_('user'))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/grocery/%s/%s/" % (self.author, self.slug)

class GroceryAisle(models.Model):
    '''simple table to hold aisle names for the grocery list'''
    aisle = models.CharField(_('aisle'), max_length=100)

    class Meta:
        ordering = ['aisle']

    def __unicode__(self):
        return self.aisle

class GroceryItem(models.Model):
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'))
    item = models.CharField(_("item"), max_length=550)
    aisle = models.ForeignKey(GroceryAisle, blank = True, null = True, default=None)

    class Meta:
        ordering = ['aisle', 'item']

    def __unicode__(self):
        return self.item
    
