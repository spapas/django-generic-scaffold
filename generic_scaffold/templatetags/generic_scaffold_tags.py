from django import template
from django.conf import settings

from generic_scaffold import get_url_names

register = template.Library()

@register.assignment_tag
def set_urls_for_scaffold(app=None, model=None, prefix=None):
    url_names = get_url_names(app, model, prefix)
    return url_names

    
