"""Test for StudentExamScoreViewSet."""

from collections.abc import Iterable
from typing import Any
from django.contrib.messages import get_messages
from rest_framework import status
from calculator.models import StudentExamScore, Exams
from manager.tests import BaseTestCase
from .calculator_base_test_case import CalculatorBaseTestCase


def create_exam_score_json(
    student: int, exam: int, score: float | int
) -> dict[str, float | int]:
    """Mock json of StudentExamScore that should be sent from frontend."""
    return {
        "student": student,
        "exam": exam,
        "score": score,
    }


def create_mock_criteria(criteria: Iterable[dict[str, int | float]]) -> dict[str, Any]:
    """Create a mock criteria Json for score calculation.

    You should,in theory, be able to pass the CriteriaSet Json that you fetched
    to the calculate_score function. Because this is literally that.
    Also please filter the event where any of the field is an empty string or
    invalid data types because serializer can't really detect those.
    """
    return {
        "criteria": list(criteria),
        "criteria_id": 0,
        "major_id": 1,
    }


class ExamScoreTest(BaseTestCase, CalculatorBaseTestCase):
    """Test API for saving and getting score of a certain user."""

    def setUp(self):
        """Set up some exams."""
        super().setUp()
        for i in range(1, 17):
            e = Exams.objects.create(name=f"Exam #{i}")
            if i <= 10:
                ses = StudentExamScore.objects.create(
                    student=self.user1, exam=e, score=69
                )
                ses.save()

    def test_list_all_scores(self):
        """List all scores of a user."""
        response = self.client.get("/api/exam_score/")
        self.assertEqual(len(response.data), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_existing_score(self):
        """Test updating scores of user."""
        for i in range(1, 5):
            data = create_exam_score_json(student=self.user1.id, exam=i, score=99)
            response = self.client.post("/api/exam_score/", data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StudentExamScore.objects.filter(score=99).count(), 4)
        self.assertEqual(StudentExamScore.objects.count(), 10)

    def test_retrieve_score_of_one_exam(self):
        """Retrieve a score of one exam."""
        response = self.client.get("/api/exam_score/3/")
        self.assertEqual(response.data["score"], 69)
        self.assertEqual(response.data["exam"], 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_exam_score(self):
        """Test creating a score of a new exam."""
        e = Exams.objects.create(name="Exam #1212312121")
        exam_score = create_exam_score_json(self.user1.id, exam=e.id, score=3000)
        response = self.client.post("/api/exam_score/", exam_score, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            StudentExamScore.objects.filter(exam__name="Exam #1212312121").count(), 1
        )
        self.assertEqual(StudentExamScore.objects.count(), 11)

    def test_calculating_score(self):
        """Test calculating the score."""
        data = create_mock_criteria(
            map(lambda x: {"exam": x, "weight": 25}, range(1, 5))
        )

        response = self.client.post(
            "/api/exam_score/calculate_score/", data, content_type="application/json"
        )
        session = self.client.session
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(session["score"], 69)

    def test_score_does_not_exist(self):
        """Test calculating score of exam that the user has not taken yet."""
        data = create_mock_criteria(
            map(
                lambda x: {"exam": x**2, "min_score": x * 10, "weight": 25}, range(1, 5)
            )
        )
        response = self.client.post(
            "/api/exam_score/calculate_score/", data, content_type="application/json"
        )
        messages = get_messages(response.wsgi_request)
        self.assertTrue(any("DOES NOT EXIST" in str(msg) for msg in messages))
        self.assertEqual(len(messages), 1)
