import json
from django import template
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()

@register.filter
def jsonify(value):
    """Converts Python objects to JSON string with proper JavaScript boolean handling"""
    return json.dumps(value, cls=DjangoJSONEncoder)