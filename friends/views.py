from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from relationships.decorators import require_user
from django.contrib.auth.models import User
from relationships.models import Relationship, RelationshipStatus

@require_user
@login_required
def follow_list(request, username):
    '''takes a user name and gets all the followers, friends and people the user is following'''
    user = get_object_or_404(User, username=username)


    def get_status(status_slug):
        '''get the relationship status object we're talking about'''
        try:
            status = RelationshipStatus.objects.by_slug(status_slug)
        except RelationshipStatus.DoesNotExist:
            raise Http404
        return status

    following_status = get_status('following')
    follower_status = get_status('followers')
    friend_status = get_status('friends')

    following_list = user.relationships.get_relationships(status=following_status)
    followers_list = user.relationships.get_related_to(status=follower_status)
    friend_list = user.relationships.get_symmetrical(status=friend_status)
    blocking_list = user.relationships.blocking()

    return render_to_response('friends/list.html', {'following_list': following_list, 'followers_list': followers_list, 'blocking_list': blocking_list, 'friend_list': friend_list, 'user':  user.username}, context_instance=RequestContext(request))


