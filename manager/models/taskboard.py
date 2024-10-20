from django.db import models


class Taskboard(models.Model):
    """
    A class representing a taskboard for holding tasks.

    A taskboard has a name and can have many tasks.
    But each task may only be associated with one task board.
    """

    name: models.CharField = models.CharField(max_length=200, null=False)