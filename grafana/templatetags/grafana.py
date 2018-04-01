import difflib
import json

from django import template

register = template.Library()


@register.filter(name='json')
def encode_json(data):
    return json.dumps(data, indent=2)


@register.simple_tag
def json_diff(a, b):
    return '\n'.join(
        difflib.unified_diff(
            json.dumps(a, indent=2).split('\n'),
            json.dumps(b, indent=2).split('\n')
        )
    )
