"""Test cases for CriteriaSet and Criterion models."""

from calculator.models import Criterion, Exams
from .calculator_base_test_case import CalculatorExtraTestCase


class AdmissionCriteriaTest(CalculatorExtraTestCase):
    """Test for admission criteria."""

    def test_major_can_have_multiple_criteria(self):
        """Test that multiple major can have multiple criteria."""
        self.assertEqual(self.cs1.major, self.cs2.major)

    def test_criteria_set_have_many_criterion(self):
        """Test that a criteria set has many criteria and can add criteria correctly."""
        self.assertEqual(self.cs1.criteria.count(), self.cs2.criteria.count(), 3)
        new_exam = Exams.objects.create(name="Physics")
        self.cs1.criteria.create(exam=new_exam, weight=0)
        self.assertEqual(self.cs1.criteria.count(), 4)
        self.assertEqual(self.cs1.criteria.get(exam__name="Physics").exam, new_exam)

    def test_deleting_criterion(self):
        """Deleting a criterion directly should delete it from all criteria set."""
        new_exam = Exams.objects.create(name="Physics")
        criterion = Criterion.objects.create(exam=new_exam, weight=0)
        self.cs1.criteria.add(criterion)
        self.cs2.criteria.add(criterion)
        self.assertEqual(self.cs1.criteria.count(), self.cs2.criteria.count(), 4)
        criterion.delete()
        self.assertEqual(self.cs1.criteria.count(), self.cs2.criteria.count(), 3)

    def test_removing_criterion(self):
        """Removing a criterion from one criteria set should not affect the other."""
        new_exam = Exams.objects.create(name="Physics")
        criterion = Criterion.objects.create(exam=new_exam, weight=0)
        self.cs1.criteria.add(criterion)
        self.cs2.criteria.add(criterion)
        self.assertEqual(self.cs1.criteria.count(), self.cs2.criteria.count(), 4)
        self.cs1.criteria.remove(criterion)
        self.assertEqual(self.cs1.criteria.count(), 3)
        self.assertEqual(self.cs2.criteria.count(), 4)
