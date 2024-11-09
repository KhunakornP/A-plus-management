"""A module to store admission criteria of each major."""

from django.db import models
from .university import Major
from .exams import Exams
from django.core.validators import MaxValueValidator


class Criteria(models.Model):
    """A passing criteria and the weight of each exam."""

    exam = models.ForeignKey(Exams)
    min_score = models.FloatField()
    weight = models.FloatField(validators=[MaxValueValidator(100)])


class CriteriaSet(models.Model):
    """A set of criteria for a certain major.

    A major can have multiple criteria set such as this one:
    https://course.mytcas.com/programs/10010128901101A
    """

    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    criteria_set = models.ManyToManyField(Criteria)
