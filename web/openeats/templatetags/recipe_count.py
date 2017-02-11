from django import template
from django.contrib.auth.models import User
register = template.Library()

@register.filter(name='recipeCount')
def recipeCount(value, arg):
    """takes the value, which is the users name and counts the number of private or shared recipes"""
    user = User.objects.get(username=value)
    if arg == 'shared':
        return user.recipe_set.filter(shared=0).count()
    else:
        return user.recipe_set.filter(shared=1).count()

    
