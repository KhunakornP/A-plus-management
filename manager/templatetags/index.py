"""Adds a filter for indexing objects in the django html template."""

from django import template
from collections.abc import Sequence
from typing import Any

register = template.Library()


@register.filter
def index(dataclass: Sequence, i: int) -> Any:
    """Index a given object with the current index."""
    return dataclass[i]
