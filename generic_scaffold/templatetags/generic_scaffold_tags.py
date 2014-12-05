from django import template
from django.conf import settings
from django.db.models.loading import get_model

from generic_scaffold import get_url_names

register = template.Library()

@register.simple_tag
def get_url_for_action(app, model, action):
    model_class = get_model(app, model)
    url = get_url_names(model_class)[action]
    return url

@register.assignment_tag
def set_url_for_action(app, model, action):
    model_class = get_model(app, model)
    url = get_url_names(model_class)[action]
    return url
