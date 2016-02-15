from django import template
from django.conf import settings

from generic_scaffold import get_url_names

register = template.Library()

@register.simple_tag
def get_url_for_action(prefix, action):
    url = get_url_names(prefix)[action]
    return url

@register.assignment_tag
def set_url_for_action(prefix, action):
    url = get_url_names(prefix)[action]
    return url
