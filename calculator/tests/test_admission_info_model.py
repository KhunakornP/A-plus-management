"""Test cases for CriteriaSet, Criterion and StudentExamScore models."""

from django.contrib.auth.models import User
from calculator.models import CriteriaSet, Criterion, Major, Exams, StudentExamScore
from .calculator_base_test_case import CalculatorBaseTestCase


class AdmissionCriteriaTest(CalculatorBaseTestCase):
    """Test for admission criteria."""

    def setUp(self):
        """Set up majors and criteria."""
        super().setUp()
        major = Major.objects.create(
            faculty=self.faculty1, code="177013", name="Computer Engineering."
        )

        self.cs1 = CriteriaSet(major=major)
        self.cs2 = CriteriaSet(major=major)
        self.cs1.save()
        self.cs2.save()
        name = ["Maths", "Biology", "English"]
        w = [10, 50, 40, 30, 40, 20]
        for i in range(6):
            e = Exams.objects.create(name=name[i % 3])
            c = Criterion.objects.create(exam=e, min_score=20, weight=w[i])
            c.save()
            self.cs1.criteria.add(c) if i % 2 == 0 else self.cs2.criteria.add(c)

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


class StudentExamScoreTestCase(CalculatorBaseTestCase):
    """Test storing score of specific exam of each student."""

    def setUp(self):
        """Set up the user."""
        super().setUp()
        self.username1 = "yukinyon"
        self.password1 = "1234"
        self.user1 = User.objects.create_user(
            username=self.username1,
            password=self.password1,
            email="example@email.jp",
            first_name="Yukino",
        )
        self.user1.save()

        self.username2 = "yuiyui"
        self.password2 = "5678"
        self.user2 = User.objects.create(
            username=self.username2,
            password=self.password2,
            email="example2@email.jp",
            first_name="Yui",
        )

        self.user2.save()

        self.exam = Exams.objects.create(name="Biology")

    def test_two_students_can_have_same_exams(self):
        """Two students can store the score of the same exam."""
        StudentExamScore.objects.create(student=self.user1, exam=self.exam, score=100)
        StudentExamScore.objects.create(student=self.user2, exam=self.exam, score=90)
        self.assertEqual(StudentExamScore.objects.count(), 2)
        self.assertEqual(
            StudentExamScore.objects.filter(student=self.user1).count(),
            StudentExamScore.objects.filter(student=self.user2).count(),
            1,
        )
        self.assertEqual(StudentExamScore.objects.get(student=self.user1).score, 100)
        self.assertEqual(StudentExamScore.objects.get(student=self.user2).score, 90)

    def test_student_can_have_score_for_many_exams(self):
        """A student can have scores of many exams."""
        for i in range(5):
            exam = Exams.objects.create(name=f"Exam #{i}")
            StudentExamScore.objects.create(student=self.user1, exam=exam, score=i * 10)

        self.assertEqual(StudentExamScore.objects.filter(student=self.user1).count(), 5)
        self.assertEqual(StudentExamScore.objects.filter(student=self.user2).count(), 0)
