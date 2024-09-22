from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def slugify_text(value):
    """
    A tag for slugifying text.
    """
    return slugify(value)
