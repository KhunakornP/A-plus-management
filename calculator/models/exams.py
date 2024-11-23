"""Model for storing exam data."""

from django.db import models


class Exams(models.Model):
    """
    A class representing A-level tests.

    Each Exam has a name and max possible score.
    The core field indicates if the Exam was created by CUPT or if it
    is issued by an outside authority, True if created by CUPT, False otherwise.
    """

    name = models.CharField(max_length=200)
    max_score = models.FloatField(default=100.00)
    core = models.BooleanField(default=False)
