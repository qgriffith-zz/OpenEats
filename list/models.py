from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class GroceryList(models.Model):
    title = models.CharField(_("grocery list"), max_length=250)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_('user'))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(GroceryList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/grocery/%s/%s/" % (self.author, self.slug)

class GroceryItem(models.Model):
    title = models.CharField(_("item"), max_length=250)
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'))
    qty =  models.CharField(_("quantity"), max_length=100)
    aisle = models.CharField(_('aisle'), max_length=100)

    class Meta:
        ordering = ['aisle', 'title']

    def __unicode__(self):
        return self.title
    
