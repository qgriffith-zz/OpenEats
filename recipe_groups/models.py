from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def save(self,  *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "course/self.slug"

    def recipe_count(self):
        return self.recipe_set.filter(shared=0).count()

class Cuisine(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def save(self,  *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(Cuisine, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "cuisine/self.slug"

    def recipe_count(self):
        return self.recipe_set.filter(shared=0).count()


