from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from djangoratings.fields import RatingField
from taggit.managers import TaggableManager

from openeats.recipe_groups.models import Course, Cuisine


class Recipe(models.Model):
    SHARE_SHARED = 0
    PRIVATE_SHARED = 1
    SHARED_CHOCIES = (
        (SHARE_SHARED, _('Share')),
        (PRIVATE_SHARED, _('Private')),
    )

    title = models.CharField(_("Recipe Title"), max_length=250)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    author = models.ForeignKey(User, verbose_name=_('user'))
    photo = models.ImageField(_('photo'), blank=True, upload_to="upload/recipe_photos")
    course = models.ForeignKey(Course, verbose_name=_('course'))
    cuisine = models.ForeignKey(Cuisine, verbose_name=_('cuisine'))
    info = models.TextField(_('info'), help_text="enter information about the recipe")
    cook_time = models.IntegerField(_('cook time'), help_text="enter time in minutes")
    servings = models.IntegerField(_('servings'), help_text="enter total number of servings")
    directions = models.TextField(_('directions'))
    shared = models.IntegerField(_('shared'), choices=SHARED_CHOCIES, default=SHARE_SHARED, help_text="share the recipe with the community or mark it private")
    tags = TaggableManager(_('tags'), help_text="separate with commas", blank=True)
    rating = RatingField(range=5)
    related = models.OneToOneField('Recipe', verbose_name=_('related'), related_name='RecipeRelated', blank=True, null=True, help_text="relate another recipe")
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pub_date', 'title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/recipe/%s/" % self.slug

    def get_reported(self):
        if ReportedRecipe.objects.filter(recipe=self):
            return True


class StoredRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name=_('recipe'))
    user = models.ForeignKey(User, verbose_name=_('user'))

    def __unicode__(self):
        return self.recipe.title


class NoteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name=_('recipe'))
    author = models.ForeignKey(User, verbose_name=_('author'))
    text = models.TextField(_('note'))

    class meta:
        verbose_name_plural = "Recipe Notes"

    def __unicode__(self):
        return "%s note for %s" % (self.author, self.recipe)


class ReportedRecipe(models.Model):
    recipe = models.OneToOneField(Recipe, verbose_name=_('recipe'))
    reported_by = models.ForeignKey(User, verbose_name=_('author'))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date', 'recipe']

    def __unicode__(self):
        return self.recipe.title