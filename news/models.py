from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField( upload_to='uploads/news/', blank=True)
    pub_date =  models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/news/%s/" %self.slug
