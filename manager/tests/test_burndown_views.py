"""Test Burndown chart views."""

from django.test import TestCase
from .templates_for_tests import create_taskboard, create_estimate_hisotry
from django.contrib.auth.models import User
from rest_framework import status
from datetime import date, timedelta


class EstimateHistoryViewTests(TestCase):
    """Tests for TaskViewSet."""

    def setUp(self):
        """Create EstimateHistory objects."""
        super().setUp()
        self.username = "Tester"
        self.password = "Bestbytest!123"
        self.user = User.objects.create_user(
            username=self.username, email="testuser@nowhere.com"
        )
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(username=self.username, password=self.password)

        self.tb = create_taskboard(self.user, "Test Taskboard")

        self.two_days_before = date.today() - timedelta(days=2)
        self.yesterday = date.today() - timedelta(days=1)
        self.today = date.today()

        self.eh1 = create_estimate_hisotry(self.tb, self.two_days_before, 70)
        self.eh2 = create_estimate_hisotry(self.tb, self.yesterday, 60)
        self.eh3 = create_estimate_hisotry(self.tb, self.today, 40)

    def test_get_eh_of_taskboard(self):
        """Test getting estimate_history in a specific taskboard."""
        response = self.client.get(f"/api/estimate_history/?taskboard={self.tb.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_invalid_taskboard(self):
        """Test getting a non-existent estimate history info."""
        response = self.client.get("/api/estimate_history/?taskboard=9999")
        self.assertEqual(response.data, [])

    def test_get_simple_velocity(self):
        """Test getting the velocity for data that is trending downward."""
        response = self.client.get(
            f"/api/velocity/?start={self.two_days_before.strftime('%Y-%m-%d')}&taskboard={self.tb.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["velocity"], 10.0)

    def test_get_average_velocity(self):
        """Test getting the velocity for data that contains recalculation."""
        create_estimate_hisotry(self.tb, self.today - timedelta(days=3), 80)
        start = self.today - timedelta(days=3)
        response = self.client.get(
            f"/api/velocity/?start={start.strftime('%Y-%m-%d')}&taskboard={self.tb.id}&mode=average"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["velocity"], 7.5)
