"""Base test case for Calculator app models."""

from django.test import TestCase
from calculator.models import University, Faculty


class CalculatorBaseTestCase(TestCase):
    """Set up some University and Faculty."""

    def setUp(self):
        """Set up the tests."""
        faculty_name = "Engineering"
        self.university = University.objects.create(name="Kasetsart")
        self.faculty = Faculty.objects.create(
            name=faculty_name, university=self.university
        )
        self.university2 = University.objects.create(name="KMITL")
        self.faculty2 = Faculty.objects.create(
            name=faculty_name, university=self.university2
        )
