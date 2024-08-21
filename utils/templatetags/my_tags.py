from django import template
from django.urls import reverse


register = template.Library()

# Base code from : https://stackoverflow.com/questions/10263482/compare-request-path-with-a-reversed-url-in-django-template
@register.simple_tag(takes_context=True)
def url_active(context, viewname):
    request = context['request']
    if request.path == reverse(viewname):
        return 'active-loader'
    else:
        return ''