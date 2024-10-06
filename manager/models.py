"""Models for the manager application."""

from django.db import models
from django.utils import timezone


def today_midnight():
    """
    Return the time for midnight of the current day.

    :returns: A datetime object for midnight of the current day.
    """
    midnight = timezone.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timezone.timedelta(days=1)
    return midnight


class Taskboard(models.Model):
    """
    A class representing a taskboard for holding tasks.

    A taskboard has a name and can have many tasks.
    But each task may only be associated with one task board.
    """

    name = models.CharField(max_length=200, null=False)


class Task(models.Model):
    """
    A class representing tasks to be done.

    A task has a title, status, end date and details.
    Each task belongs to only one taskboard but each taskboard
    can have multiple tasks.
    """

    title = models.CharField(max_length=300)
    status = models.CharField(max_length=20, default="TODO")
    end_date = models.DateTimeField("End date", default=today_midnight)
    details = models.TextField(default=None, null=True, blank=True)
    taskboard = models.ForeignKey(Taskboard, on_delete=models.CASCADE)
