from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext as _
from recipe.models import Recipe
from taggit.models import Tag, TaggedItem


class RecentRecipesFeed(Feed):
    title = settings.OETITLE + _(" Recent Recipes")
    link = "/recipe/recent/"
    description = _("Updates added on new recipes added to ") + settings.OETITLE

    def items(self):
        return Recipe.objects.filter(shared=Recipe.SHARE_SHARED).order_by('-pub_date', 'title')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.info


class TopRecipesFeed(Feed):
    title = settings.OETITLE + _(" Top Recipes")
    link = "/recipe/top/"
    description =_("Top recipes on ") + settings.OETITLE

    def items(self):
        rating_qs = Recipe.objects.extra(select={'rate': '((100/%s*rating_score/(rating_votes+%s))+100)/2' % (Recipe.rating.range, Recipe.rating.weight)})
        return rating_qs.filter(shared=Recipe.SHARE_SHARED).order_by('-rate')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.info

class TaggedRecipesFeed(Feed):

    def get_object(self, request, tag):
        return tag

    def title(self, tag):
        return settings.OETITLE + _(" Recipes tagged %s") % tag

    def link(self, tag):
        return "/tags/recipe/" + tag + "/"

    def description(self, tag):
        return _("New recipes tagged %s added to %s") % (tag, settings.OETITLE)

    def items(self, tag):
        try:
            recipe_tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            return []
        recipes_tagged = TaggedItem.objects.filter(tag=recipe_tag).order_by('-id')[:10]
        return [recipe.content_object for recipe in recipes_tagged]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.info
