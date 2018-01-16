import django
from django import template
from django.conf import settings

from generic_scaffold import get_url_names

register = template.Library()


if django.VERSION >= (1, 9, 0):
    decorator = register.simple_tag
else:
    decorator = register.assignment_tag


def set_urls_for_scaffold(app=None, model=None, prefix=None):
    url_names = get_url_names(app, model, prefix)
    return url_names

set_urls_for_scaffold = decorator(set_urls_for_scaffold)

