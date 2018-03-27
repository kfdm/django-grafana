import json

from django import template

register = template.Library()


@register.filter(name='json')
def decode_json(value):
    return json.loads(value)
