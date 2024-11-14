"""Module for Event models."""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Event(models.Model):
    """
    A class representing events on the calendar.

    An event has a title, start date, end date and details.
    An event has 1 associated user. This is the user that created the event.
    """

    title = models.CharField(max_length=300)
    start_date = models.DateTimeField("Start date", default=timezone.now)
    end_date = models.DateTimeField("End date", default=timezone.now)
    details = models.TextField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
