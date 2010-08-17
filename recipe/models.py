from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tagging.fields import TagField, Tag
from recipe_groups.models import Course, Cuisine
from imagekit.models import ImageModel
from djangoratings.fields import RatingField

class Recipe(ImageModel):
    SHARE_SHARED = 0
    PRIVATE_SHARED = 1
    SHARED_CHOCIES = (
    (SHARE_SHARED, 'Share'),
    (PRIVATE_SHARED, 'Private'),
    )

    title = models.CharField("Recipe Title", max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User)
    photo = models.ImageField(blank=True, upload_to="upload/recipe_photos")
    course = models.ForeignKey(Course)
    cuisine = models.ForeignKey(Cuisine)
    info = models.TextField(help_text="enter information about the recipe")
    cook_time = models.IntegerField(help_text="enter time in miuntes")
    servings = models.IntegerField(help_text="enter total number of servings")
    directions = models.TextField()
    shared = models.IntegerField(choices=SHARED_CHOCIES, default=SHARE_SHARED, help_text="share the recipe with the community or mark it private")
    tags = TagField(help_text="separate with commas")
    rating = RatingField(range=5)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class IKOptions:
        '''image kit options'''
        spec_module = 'recipe.ikspec'
        cache_dir = 'upload/recipe_photos/cache'
        image_field = 'photo'


    class Meta:
        ordering = ['pub_date', 'title']

    def __unicode__(self):
        return self.title

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def save(self, *args, **kwargs):
        if (not self.id) and (not self.slug):
            self.slug=slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/recipe/%s/" %self.slug

