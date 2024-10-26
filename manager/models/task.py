"""Module for Task models."""

from django.db import models
from django.utils import timezone
from .functions import today_midnight
from .taskboard import Taskboard
from .estimate_history import EstimateHistory
from django.contrib.auth.models import User


class Task(models.Model):
    """
    A class representing tasks to be done.

    A task has a title, status, end date and details.
    Each task belongs to only one taskboard but each taskboard
    can have multiple tasks.
    A task at any given moment belongs to exactly one user.
    """

    title: models.CharField = models.CharField(max_length=300)
    status: models.CharField = models.CharField(max_length=20, default="TODO")
    end_date: models.DateTimeField = models.DateTimeField(
        "End date", default=today_midnight
    )
    details: models.TextField = models.TextField(default=None, null=True, blank=True)
    taskboard: models.ForeignKey = models.ForeignKey(
        Taskboard, on_delete=models.CASCADE
    )
    time_estimate = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __compute_time_diff(self, new_time: int) -> int:
        """Compute the difference between old and new time estimate."""
        try:
            old_time = Task.objects.get(pk=self.pk).time_estimate
            return new_time - old_time
        except Task.DoesNotExist:
            return new_time

    def save(self, *args, **kwargs):
        """Override default save method.

        Namely,
        - Set end_date to today midnight if end_date is NULL.
        - Update the time remaining of the related estimate history object.
        """
        if self.end_date is None:
            self.end_date = today_midnight()
        eh = EstimateHistory.objects.get(
            date=timezone.localdate(), taskboard=self.taskboard
        )
        eh.time_remaining += self.__compute_time_diff(self.time_estimate)
        eh.save()

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Override default delete method.

        Also subtracts the time remaining in the related EstimateHistory object.
        """
        est = self.time_estimate
        eh = EstimateHistory.objects.get(
            date=timezone.localdate(), taskboard=self.taskboard
        )
        eh.time_remaining -= est
        eh.save()

        super().delete(using, keep_parents)
