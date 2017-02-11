from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from relationships.decorators import require_user
from django.contrib.auth.models import User
from relationships.models import RelationshipStatus

@require_user
@login_required
def follow_list(request, username):
    """takes a user name and gets all the followers, friends and people the user is following"""
    user = get_object_or_404(User, username=username)

    def get_status(status_slug):
        """get the relationship status object we're talking about"""
        try:
            status = RelationshipStatus.objects.by_slug(status_slug)
        except RelationshipStatus.DoesNotExist:
            raise Http404
        return status

    following_status = get_status('following')
    follower_status = get_status('followers')
    following_list = user.relationships.get_relationships(status=following_status)
    followers_list = user.relationships.get_related_to(status=follower_status)
    blocking_list = user.relationships.blocking()

    return render(request, 'friends/list.html', {'following_list': following_list, 'followers_list': followers_list, 'blocking_list': blocking_list, 'username':  user.username})


@login_required
def feed(request, username):
    """inds the followers of a user' and passes it to a template that uses template tags to pull the feeds"""

    user = get_object_or_404(User, username=username)
    following = user.relationships.following()

    return render(request, 'friends/feed.html', {'following_list': following})
