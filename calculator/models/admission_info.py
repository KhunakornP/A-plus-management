"""A module for models relating to admission information such as criteria and score."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
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

    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    criteria = models.ManyToManyField(Criterion)


class StudentExamScore(models.Model):
    """A model to store each student's score of each exam."""

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0)])
