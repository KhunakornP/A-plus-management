"""Base test case for Calculator app models."""

from django.test import TestCase
from calculator.models import University, Faculty, Major


class CalculatorBaseTestCase(TestCase):
    """Set up some University and Faculty."""

    def setUp(self):
        """Set up the tests."""
        faculty_name = "Engineering"
        self.university1 = University.objects.create(name="Kasetsart")
        self.faculty1 = Faculty.objects.create(
            name=faculty_name, university=self.university1
        )
        self.university2 = University.objects.create(name="KMITL")
        self.faculty2 = Faculty.objects.create(
            name=faculty_name, university=self.university2
        )
        Faculty.objects.create(university=self.university1, name="Humanity")
        for i in range(7):
            m = Major.objects.create(
                name=f"Major #{i}",
                code=f"{i}",
                faculty=self.faculty1 if i % 2 == 0 else self.faculty2,
            )
            m.save()
