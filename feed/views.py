from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext as _
from recipe.models import Recipe

class RecentRecipesFeed(Feed):
    title = settings.OETITLE + _(" Recent Recipes")
    link = "/recipe/recent"
    description=_("Updates added on new recipes added to ") + settings.OETITLE

    def items(self):
        return Recipe.objects.filter(shared=Recipe.SHARE_SHARED).order_by('-pub_date', 'title')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.info
