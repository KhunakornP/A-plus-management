"""Test cases for StudentExamScore model."""

from django.contrib.auth.models import User
from calculator.models import StudentExamScore, Exams
from .calculator_base_test_case import CalculatorBaseTestCase


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
