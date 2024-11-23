"""A module for models relating to admission criteria."""

from django.core.validators import MaxValueValidator
from django.db import models
from .university import Major
from .exams import Exams


class Criterion(models.Model):
    """A passing criteria and the weight of each exam.

    Criterion is a singular form of criteria, according to Merriam-Webster dictionary.
    """

    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    min_score = models.FloatField(default=0)
    weight = models.FloatField(validators=[MaxValueValidator(100)])


class CriteriaSet(models.Model):
    """A set of criteria for a certain major.

    A major can have multiple criteria set such as this one:
    https://course.mytcas.com/programs/10010128901101A
    """

    name = models.CharField(max_length=200, default="Unnamed CriteriaSet")
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    criteria = models.ManyToManyField(Criterion)
