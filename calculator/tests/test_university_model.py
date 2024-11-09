"""Test cases for University, Faculty and Major models."""

from django.test import TestCase
from django.db.utils import IntegrityError
from calculator.models import University, Major, Faculty
from .tempalte_for_tests import CalculatorBaseTestCase


class UniversityTest(CalculatorBaseTestCase):
    """Test for university, faculty and major."""

    def test_faculty_in_different_university_can_have_same_name(self):
        """Different university may have same faculty name."""
        self.assertEqual(self.faculty2.name, self.faculty.name)
        self.assertNotEqual(self.faculty2, self.faculty)

    def test_one_faculty_per_university(self):
        """No two faculties of the same name belonging to the same university."""
        with self.assertRaises(IntegrityError):
            name = "Agro-Industry"
            Faculty.objects.create(university=self.university, name=name)
            Faculty.objects.create(university=self.university, name=name)

    def test_major_cannot_have_same_code(self):
        """Different major must have unique code."""
        with self.assertRaises(IntegrityError):
            code = "KFC-1150"
            Major.objects.create(name="Gender Studies", code=code, faculty=self.faculty)
            Major.objects.create(
                name="Gender Studies", code=code, faculty=self.faculty2
            )
            Major.objects.create(name="Gender Studies", code=code, faculty=self.faculty)
            Major.objects.create(
                name="Mechanical Engineering", code=code, faculty=self.faculty
            )

    def test_major__can_have_same_name(self):
        """Majors can have same name."""
        m1 = Major.objects.create(
            code="The-Pizza-1112", name="Electrical Engineering", faculty=self.faculty
        )
        m2 = Major.objects.create(
            code="Pizza-Hut-1150", name="Electrical Engineering", faculty=self.faculty2
        )
        self.assertEqual(m1.name, m2.name)
        self.assertNotEqual(m1, m2)
