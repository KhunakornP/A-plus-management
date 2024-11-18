"""A module of ScoreHistory object."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .university import Major
from .criteria import CriteriaSet


class ScoreHistory(models.Model):
    """A Model to store the score of a certain major of previous year."""

    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    criteria_set = models.ForeignKey(CriteriaSet, on_delete=models.CASCADE)
    min_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    register = models.IntegerField(default=0)
    max_seat = models.IntegerField(default=0)
    admitted = models.IntegerField(default=0)
    year = models.IntegerField(
        default=2567, validators=[MaxValueValidator(9999), MinValueValidator(1899)]
    )

    def __str__(self):
        """Return a string Representation of the ScoreHistory Model."""
        return f"{self.major.name} score of year"
