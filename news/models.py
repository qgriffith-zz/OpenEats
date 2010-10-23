from django.db import models
from django.utils.translation import ugettext_lazy as _

class Entry(models.Model):
    title = models.CharField(_('title') ,max_length=255, blank=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    content = models.TextField(_('content'), blank=True)
    image = models.ImageField(_('image'), upload_to='uploads/news/', blank=True)
    pub_date =  models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/news/%s/" %self.slug
