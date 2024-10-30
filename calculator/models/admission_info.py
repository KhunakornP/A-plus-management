"""A module to store University data."""

from django.db import models


# Create your models here.
class University(models.Model):
    """Name of different universities."""

    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    """Name of different faculties of a university."""

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.name} {self.university}"


class Major(models.Model):
    """Name of different majors of a faculty."""

    code = models.CharField(max_length=200, null=False, unique=True)
    name = models.CharField(max_length=200, null=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.faculty.name} {self.faculty.university.name}"


class Criteria(models.Model):
    """Criteria of a major."""

    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    def __str__(self):
        return f"Criteria of {self.major.name} {self.major.faculty.name} {self.major.faculty.university.name}"
