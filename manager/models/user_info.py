"""Module for related user information models."""

from django.db import models
from django.contrib.auth.models import User


class UserPermissions(models.Model):
    """
    A class that stores custom permissions for use in the template.

    This class has no related fields or table in the database.
    It only stores permissions for the django Groups model.
    """

    class Meta:
        """The Meta class for UserPermissions."""

        managed = False

        permissions = [
            ("is_taking_A_levels", "User who has access to the calculator"),
            ("is_parent", "User who has access to the parent dashboard"),
        ]


class ParentInfo(models.Model):
    """
    A class which stores parent data.

    Each Parent object can only be associated with only one User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayed_name = models.CharField(max_length=50)


class StudentInfo(models.Model):
    """
    A class which stores student data.

    Each StudentInfo object can only be associated with only one User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayed_name = models.CharField(max_length=50)
    parent = models.ManyToManyField(
        User,
        related_name="student_set",
    )
