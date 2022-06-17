import difflib
import json
import datetime
from django import template

register = template.Library()


@register.filter(name="json")
def encode_json(data):
    return json.dumps(data, indent=2)


@register.simple_tag
def json_diff(a, b):
    return "\n".join(
        difflib.unified_diff(
            json.dumps(a, indent=2).split("\n"), json.dumps(b, indent=2).split("\n")
        )
    )


@register.filter
def from_epoch(epoch):
    ts = datetime.datetime.fromtimestamp(epoch / 1000)
    return ts


@register.filter
def role_class(role):
    if role == "Admin":
        return "danger"
    if role == "Editor":
        return "warning"
    if role == "Viewer":
        return "info"
    return "secondary"
