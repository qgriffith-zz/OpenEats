from django import template
from django.utils.translation import ugettext_lazy as _

from openeats.news.models import Entry


register = template.Library()

@register.inclusion_tag('news/front_page.html')
def frontpage_news():
    """a tag that returns the news story for the front page"""
    if Entry.objects.filter(frontpage=True):
        news = Entry.objects.filter(frontpage=True).order_by('-pub_date')[0]  #always will return the most recent story marked with frontpage
        return {'news': news}
    else:
        news = Entry()
        news.title=_("No Front page News")
        news.content=_("Currently not any front page news on this site")
        return {'news': news}
