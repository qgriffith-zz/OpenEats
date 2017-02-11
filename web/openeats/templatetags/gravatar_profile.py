from django import template

import urllib, hashlib

register = template.Library()

def gravatar(user, size=80):
    """A template tag that returns a users gravatar picture if they are registerd if not it returns the default picture"""
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id':hashlib.md5(user.email).hexdigest(),
        'size':str(size),
        'd':'mm'})
    return """<img src="%s" alt="gravatar for %s" />""" % (gravatar_url, user.username)

register.simple_tag(gravatar)