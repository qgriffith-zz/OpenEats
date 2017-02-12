from django.views.generic import ListView

from openeats.recipe.models import Recipe


class RecentRecipeView(ListView):
    context_object_name = "recipe_list"
    queryset=Recipe.objects.filter(shared=Recipe.SHARE_SHARED).order_by('-pub_date', 'title')[:20]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RecentRecipeView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Recent Recipes'
        context['feed'] = "/feed/recent/"
        return context

class TopRecipeView(ListView):
    context_object_name = "recipe_list"
    rating_qs = Recipe.objects.extra(select={'rate': '((100/%s*rating_score/(rating_votes+%s+1))+100)/2' % (Recipe.rating.range, Recipe.rating.weight)})
    queryset=rating_qs.filter(shared=Recipe.SHARE_SHARED).order_by('-rate')[:20]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TopRecipeView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['feed'] = "/feed/top/"
        context['title'] = 'Top Recipes'
        return context