"""Test for StudentExamScoreViewSet."""
from calculator.models import StudentExamScore, Exams
from manager.tests import BaseTestCase


def create_examscore_json(
    student: int, exam: int, score: float | int, id: int | None = None
):
    """Mock json of StudentExamScore that should be sent from frontend."""
    data = {}
    if id is not None:
        data["id"] = str(id)

    data.update(
        {
            "student": student,
            "exam": exam,
            "score": score,
        }
    )

    return data


class ExamScoreTest(BaseTestCase):
    """Test API for saving and getting score of a certain user."""

    def setUp(self):
        """Set up some exams."""
        super().setUp()
        for i in range(1, 10):
            e = Exams.objects.create(name=f"Exam #{i}")
            ses = StudentExamScore.objects.create(
                student=self.user1, exam=e, score=12.99
            )
            ses.save()

    def test_list_all_scores(self):
        """List all scores of a user."""
        response = self.client.get("/api/exam_score/")
        self.assertEqual(len(response.data), 9)

    def test_updating_existing_score(self):
        """Test updating scores of user."""
        for i in range(1, 5):
            data = create_examscore_json(student=1, exam=i, score=99)
            self.client.post("/api/exam_score/", data, format="json")
        self.assertEqual(StudentExamScore.objects.filter(score=99).count(), 4)
