from urllib.parse import urlencode
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, next_page):
    query = context['request'].GET.copy().urlencode()
    
    if '&page=' in query:
        url = query.rpartition('&page=')[0]
    else:
        url = query
    return f'{url}&page={next_page}'