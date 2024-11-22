"""Module for Event models."""

from django.db import models
from django.utils import timezone
from django.db.models import F, Q
from django.contrib.auth.models import User
from .functions import today_midnight


class Event(models.Model):
    """
    A class representing events on the calendar.

    An event has a title, start date, end date and details.
    An event has 1 associated user. This is the user that created the event.
    """

    title = models.CharField(max_length=300)
    start_date = models.DateTimeField("Start date", default=timezone.now)
    end_date = models.DateTimeField("End date", default=today_midnight)
    details = models.TextField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Event."""

        constraints = [
            models.CheckConstraint(
                name="end_date must be greater than start_date",
                check=Q(end_date__gt=F("start_date")),
            )
        ]
