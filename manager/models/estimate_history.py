"""Module for Estimate history models."""

from django.db import models
from django.utils import timezone
from .taskboard import Taskboard


class EstimateHistoryManager(models.Manager):
    """A custom Manager for EstimateHistory model."""

    def create(self, **kwargs):
        """Override the create method.

        Set initial time remaining to match the previous day, if exists.
        """
        taskboard = kwargs["taskboard"]
        eh_of_previous_day_of_this_tb = self.filter(taskboard=taskboard).last()

        if eh_of_previous_day_of_this_tb:
            kwargs["time_remaining"] = eh_of_previous_day_of_this_tb.time_remaining

        return super().create(**kwargs)

    def get(self, *args, **kwargs):
        """Override default get method.

        If the object does not exist, create a new one instead.
        """
        try:
            return super().get(*args, **kwargs)
        except EstimateHistory.DoesNotExist:
            new_obj = self.create(**kwargs)
            return new_obj


class EstimateHistory(models.Model):
    """A class containing time estimate history of each day of a specific taskboard."""

    taskboard = models.ForeignKey(Taskboard, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    time_remaining = models.IntegerField(default=0)
    objects = EstimateHistoryManager()
