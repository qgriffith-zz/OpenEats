from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from openeats.recipe.models import Recipe


class GroceryList(models.Model):
    title = models.CharField(_("grocery list title"), max_length=250)
    slug = AutoSlugField(_('slug'), populate_from='title')
    author = models.ForeignKey(User, verbose_name=_('user'))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return self.title

    def get_shared(self):
        """check if the list is shared"""
        if GroceryShared.objects.filter(list=self):
            return True

    def get_shared_to(self):
        """if the list is shared get who it is shared to"""
        if self.get_shared:
            shared = GroceryShared.objects.get(list=self)
            return shared.shared_to

    def get_absolute_url(self):
        return "/grocery/%s/%s/" % (self.author, self.slug)


class GroceryAisle(models.Model):
    """simple table to hold aisle names for the grocery list"""
    aisle = models.CharField(_('aisle'), max_length=100)
    author = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True)

    class Meta:
        ordering = ['aisle']

    def __unicode__(self):
        return self.aisle


class GroceryItem(models.Model):
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'), related_name='items')
    item = models.CharField(_("item"), max_length=550)
    aisle = models.ForeignKey(GroceryAisle, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['aisle', 'item']

    def __unicode__(self):
        return self.item


class GroceryShared(models.Model):
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'))
    shared_by = models.ForeignKey(User, verbose_name=_('shared by'), related_name="shared_by")
    shared_to = models.ForeignKey(User, verbose_name=_('shared to'), related_name="shared_to")

    class Meta:
        verbose_name_plural = "shared lists"

    def save(self, *args, **kwargs):
        """make sure the shared_by field is always set the to the owner of the list"""
        if not self.id:
            self.shared_by = self.list.author
        super(GroceryShared, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.list.title


class GroceryRecipe(models.Model):
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'))
    recipe = models.ForeignKey(Recipe, verbose_name=_('recipe'))

    def __unicode__(self):
        return self.recipe.title