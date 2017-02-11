from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext as _

from openeats.recipe.models import Recipe


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