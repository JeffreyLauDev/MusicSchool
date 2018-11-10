import datetime

from django import template
from django.utils.dateformat import format

register = template.Library()

@register.filter
def template(var):
    pass