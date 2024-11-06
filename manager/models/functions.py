"""Module for functions used by models."""

from django.utils import timezone


def today_midnight():
    """
    Return the time for midnight of the current day.

    :returns: A datetime object for midnight of the current day.
    """
    midnight = timezone.now().replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    return midnight
