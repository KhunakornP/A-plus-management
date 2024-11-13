"""Test cases for University, Faculty and Major models."""

from django.db.utils import IntegrityError
from calculator.models import Major, Faculty
from .calculator_base_test_case import CalculatorBaseTestCase


class UniversityTest(CalculatorBaseTestCase):
    """Test for university, faculty and major."""

    def test_faculty_in_different_university_can_have_same_name(self):
        """Different university may have same faculty name."""
        self.assertEqual(self.faculty2.name, self.faculty1.name)
        self.assertNotEqual(self.faculty2, self.faculty1)

    def test_one_faculty_per_university(self):
        """No two faculties of the same name belonging to the same university."""
        with self.assertRaises(IntegrityError):
            name = "Agro-Industry"
            Faculty.objects.create(university=self.university1, name=name)
            Faculty.objects.create(university=self.university1, name=name)

    def test_many_faculty_per_university(self):
        """One university can have many faculties."""
        for i in range(6):
            m = Faculty.objects.create(
                name=f"Faculty #{i}", university=self.university1
            )
            m.save()
        self.assertEqual(Faculty.objects.filter(university=self.university1).count(), 7)

    def test_many_major_per_faculty(self):
        """One faculty can have many majors."""
        for i in range(6):
            m = Major.objects.create(
                name=f"Major #{i}", code=f"{i}", faculty=self.faculty1
            )
            m.save()
        self.assertEqual(Major.objects.filter(faculty=self.faculty1).count(), 6)

    def test_major_cannot_have_same_code(self):
        """Different major must have unique code."""
        with self.assertRaises(IntegrityError):
            code = "KFC-1150"
            Major.objects.create(
                name="Gender Studies", code=code, faculty=self.faculty1
            )
            Major.objects.create(
                name="Gender Studies", code=code, faculty=self.faculty2
            )
            Major.objects.create(
                name="Gender Studies", code=code, faculty=self.faculty1
            )
            Major.objects.create(
                name="Mechanical Engineering", code=code, faculty=self.faculty1
            )

    def test_major_can_have_same_name(self):
        """Majors can have same name."""
        m1 = Major.objects.create(
            code="The-Pizza-1112", name="Electrical Engineering", faculty=self.faculty1
        )
        m2 = Major.objects.create(
            code="Pizza-Hut-1150", name="Electrical Engineering", faculty=self.faculty2
        )
        self.assertEqual(m1.name, m2.name)
        self.assertNotEqual(m1, m2)
