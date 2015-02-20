from django import template
register = template.Library()

@register.inclusion_tag('list/_items.html')
def item_tag(items):
    """a tag that gets passed grocery items and then arranges the items by the aisle they are found in"""
    aisle_list=[]
    for item in items:
        if item.aisle not in aisle_list: #go thorugh and add each aisle to a list and only add each one once
            aisle_list.append(item.aisle)
    
    aisle_list.sort()
    return {'aisle_list':aisle_list, 'items':items, 'dict': dict }