from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from recipe_groups.models import Course, Cuisine

class Recipe(models.Model):
    SHARE_SHARED = 0
    PRIVATE_SHARED = 1
    SHARED_CHOCIES = (
    (SHARE_SHARED, 'Share'),
    (PRIVATE_SHARED, 'Private'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    cuisine = models.ForeignKey(Cuisine)
    detail = models.TextField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    directions = models.TextField()
    shared = models.IntegerField(choices=SHARED_CHOCIES, default=SHARE_SHARED)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pub_date', 'title']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/recipe/%s" %self.slug





