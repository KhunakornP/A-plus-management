"""Tests for ScoreHistory Viewset."""

from .calculator_base_test_case import CalculatorExtraTestCase
from calculator.models import ScoreHistory, Major
from rest_framework import status


class ScoreHistoryViewTest(CalculatorExtraTestCase):
    """Test ScoreHistoryViewSet."""

    def setUp(self):
        """Set Up some ScoreHistory objects for test."""
        super().setUp()
        self.sh1 = ScoreHistory.objects.create(
            major=Major.objects.get(pk=1),
            criteria_set=self.cs1,
            min_score=30,
            max_score=99,
            register=100,
            max_seat=30,
            admitted=25,
            year=2567,
        )

        self.sh2 = ScoreHistory.objects.create(
            major=Major.objects.get(pk=1),
            criteria_set=self.cs2,
            min_score=30,
            max_score=99,
            register=100,
            max_seat=30,
            admitted=25,
            year=2567,
        )

        self.sh3 = ScoreHistory.objects.create(
            major=Major.objects.get(pk=1),
            criteria_set=self.cs1,
            min_score=10.11,
            max_score=93.20,
            register=100,
            max_seat=30,
            admitted=25,
            year=2566,
        )

        self.sh4 = ScoreHistory.objects.create(
            major=Major.objects.get(pk=1),
            criteria_set=self.cs2,
            min_score=10,
            max_score=97.69,
            register=100,
            max_seat=30,
            admitted=25,
            year=2566,
        )

    def test_list_all_score_history(self):
        """Test listing all score history."""
        response = self.client.get("/api/score_history/")
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_score_history_based_on_criteria_set(self):
        """Test listing score history based on criteriaset."""
        response = self.client.get(f"/api/score_history/?criteria_set={self.cs1.id}")
        self.assertEqual(len(response.data), 2)
        response = self.client.get(f"/api/score_history/?criteria_set={self.cs1.id}")
        self.assertEqual(len(response.data), 2)
        self.assertTrue(
            all(filter(lambda r: r["criteria_set"] == self.cs1.id, response.data))
        )

        response_with_year = self.client.get(
            f"/api/score_history/?criteria_set={self.cs1.id}&year={2566}"
        )
        self.assertEqual(len(response_with_year.data), 1)
        self.assertTrue(response_with_year.data[0]["criteria_set"] == self.cs1.id)
        self.assertTrue(response_with_year.data[0]["year"] == 2566)

    def test_list_score_history_with_invalid_criteria_set(self):
        """Test listing score history with invalid CriteriaSet."""
        response = self.client.get(f"/api/score_history/?criteria_set={3000}")
        self.assertEqual(len(response.data), 0)

    def test_list_score_history_based_on_major(self):
        """Test listing score history based on major."""
        response = self.client.get(f"/api/score_history/?major={1}")
        self.assertEqual(len(response.data), 4)
        self.assertTrue(all(filter(lambda x: x["major"] == 1, response.data)))

        response_with_year = self.client.get(f"/api/score_history/?major={1}&year=2566")
        self.assertTrue(
            all(filter(lambda x: x["year"] == 2566, response_with_year.data))
        )
        self.assertTrue(all(filter(lambda x: x["major"] == 1, response_with_year.data)))
        self.assertEqual(len(response_with_year.data), 2)

    def test_list_score_history_with_invalid_year(self):
        """List score history with either criteria and exam but with invalid year."""
        response1 = self.client.get(
            f"/api/score_history/?criteria_set={self.cs1.id}&year={3000}"
        )
        self.assertEqual(len(response1.data), 0)
        response2 = self.client.get(f"/api/score_history/?major={1}&year=4000")
        self.assertEqual(len(response2.data), 0)
