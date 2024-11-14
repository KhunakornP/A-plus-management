"""Module for Taskboard models."""

from django.db import models
from django.contrib.auth.models import User


class Taskboard(models.Model):
    """
    A class representing a taskboard for holding tasks.

    A taskboard has a name and can have many tasks.
    But each task may only be associated with one task board.
    A taskboard has 1 associated user, which is the user
    the taskboard belongs to.
    """

    name: models.CharField = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
