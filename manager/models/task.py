"""Module for Task models."""

from django.db import models
from django.utils import timezone
from .functions import today_midnight
from .taskboard import Taskboard
from .estimate_history import EstimateHistory


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

    def __compute_time_diff(self) -> int:
        """Compute the difference between old and new time estimate."""
        try:
            old_time = Task.objects.get(pk=self.pk).time_estimate
            return self.time_estimate - old_time
        except Task.DoesNotExist:
            return self.time_estimate

    def __status_changed_to_done(self) -> bool:
        """Check whether status of tasks are changed to DONE.

        :return: True if the task's status changed from something else to DONE.
        Or the task is created with status=DONE.
        Otherwise, return false.
        """
        try:
            old_status = Task.objects.get(pk=self.pk).status
            if self.status == old_status:
                return False
            return self.status == "DONE"
        except Task.DoesNotExist:
            return self.status == "DONE"

    def __status_changed_from_done(self) -> bool:
        """Check whether status of tasks are changed from DONE.

        :return: True if the task's status changed from DONE to something else.
        Otherwise, return false.
        """
        try:
            old_status = Task.objects.get(pk=self.pk).status
            if self.status == old_status:
                return False
            return old_status == "DONE"
        except Task.DoesNotExist:
            return False

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
        eh.time_remaining += self.__compute_time_diff()
        if self.__status_changed_to_done():
            eh.time_remaining -= self.time_estimate
        elif self.__status_changed_from_done():
            eh.time_remaining += self.time_estimate
        eh.save()

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Override default delete method.

        Also subtracts the time remaining in the related EstimateHistory object.
        """
        eh = EstimateHistory.objects.get(
            date=timezone.localdate(), taskboard=self.taskboard
        )
        eh.time_remaining -= self.time_estimate
        eh.save()

        super().delete(using, keep_parents)
