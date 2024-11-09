"""Test cases for CriteriaSet and Criterion models."""

from django.test import TestCase
from calculator.models import CriteriaSet, Criterion, Major, Exams
from .tempalte_for_tests import CalculatorBaseTestCase


class AdmissionCriteriaTest(CalculatorBaseTestCase):
    """Test for admission criteria."""

    def setUp(self):
        """Set up majors and criteria."""
        super().setUp()
        major = Major.objects.create(
            faculty=self.faculty, code="177013", name="Computer Engineering."
        )

        self.cs1 = CriteriaSet(major=major)
        self.cs2 = CriteriaSet(major=major)
        self.cs1.save()
        self.cs2.save()
        name = ["Maths", "Biology", "English"]
        w = [10, 50, 40, 30, 40, 20]
        for i in range(6):
            e = Exams.objects.create(name=name[i % 3])
            c = Criterion.objects.create(exam=e, min_score=10, weight=w[i])
            c.save()
            self.cs1.criteria.add(c) if i % 2 == 0 else self.cs2.criteria.add(c)

    def test_major_can_have_multiple_criteria(self):
        """Test that multiple major can have multiple criteria."""
        self.assertEqual(self.cs1.major, self.cs2.major)
