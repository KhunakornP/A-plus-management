"""Adds a filter for indexing objects in the django html template."""
from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]

