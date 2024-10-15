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


class Event(models.Model):
    """
    A class representing events on the calendar.

    An event has a title, start date, end date and details.
    """

    title = models.CharField(max_length=300)
    start_date = models.DateTimeField("Start date", default=timezone.now)
    end_date = models.DateTimeField("End date", default=timezone.now)
    details = models.TextField(default=None, null=True, blank=True)
