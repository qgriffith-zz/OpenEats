import html5lib
from html5lib import treebuilders, treewalkers, serializer, sanitizer

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@stringfilter
@register.filter(name='sanitize_html')
def sanitize_html(value):
    """A custom filter that sanitzes html output to make sure there is no bad stuff in it"""
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer, tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = p.parseFragment(value)

    walker = treewalkers.getTreeWalker("dom")

    stream = walker(dom_tree)

    s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
    return "".join(s.serialize(stream))
