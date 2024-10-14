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

    name: models.CharField = models.CharField(max_length=200, null=False)


class EstimateHistory(models.Model):
    """A class containing time estimate history of each day of a specific taskboard."""

    taskboard = models.ForeignKey(Taskboard, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    time_remaining = models.IntegerField(default=0)
    # TODO modify the creation method to get the time remaining of previous day
    # as initial value


class Task(models.Model):
    """
    A class representing tasks to be done.

    A task has a title, status, end date and details.
    Each task belongs to only one taskboard but each taskboard
    can have multiple tasks.
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

        try:
            estimate_history_obj = EstimateHistory.objects.get(
                date=timezone.localdate(), taskboard=self.taskboard
            )
        except EstimateHistory.DoesNotExist:
            estimate_history_obj = EstimateHistory.objects.create(
                taskboard=self.taskboard
            )
            estimate_history_obj.save()

        estimate_history_obj.time_remaining += self.__compute_time_diff(
            self.time_estimate
        )
        estimate_history_obj.save()

        super().save(*args, **kwargs)


class Event(models.Model):
    """
    A class representing events on the calendar.

    An event has a title, start date, end date and details.
    """

    title = models.CharField(max_length=300)
    start_date = models.DateTimeField("Start date", default=timezone.now)
    end_date = models.DateTimeField("End date", default=timezone.now)
    details = models.TextField(default=None, null=True, blank=True)
