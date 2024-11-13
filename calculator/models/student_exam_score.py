"""A module for StudentExamScore class."""

from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from .exams import Exams

class StudentExamScore(models.Model):
    """A model to store each student's score of each exam."""

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0)])
