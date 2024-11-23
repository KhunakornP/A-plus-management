"""Test Burndown chart views."""

from django.test import TestCase
from django.utils import timezone
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

        self.two_days_before = timezone.now() - timedelta(days=2)
        self.yesterday = timezone.now() - timedelta(days=1)
        self.today = timezone.now()

        self.eh1 = create_estimate_hisotry(self.tb, self.two_days_before, 70)
        self.eh2 = create_estimate_hisotry(self.tb, self.yesterday, 60)
        self.eh3 = create_estimate_hisotry(self.tb, self.today, 40)

    def test_get_simple_velocity(self):
        """Test getting the velocity for data that is trending downward."""
        response = self.client.get(
            f"/api/velocity/?start={self.two_days_before.strftime('%Y-%m-%d')}&taskboard={self.tb.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["velocity"], 15.0)
        # remaining 40hr/15 vel per day = 3 days till completion
        end = self.today + timedelta(days=3)
        self.assertEqual(response.data["x"], end.strftime("%Y-%m-%d"))

    def test_get_average_velocity(self):
        """Test getting the velocity for data that contains recalculation."""
        self.eh1.time_remaining = 80
        self.eh2.time_remaining = 56
        self.eh3.time_remaining = 60  # some tasks got re estimated today
        self.eh1.save()
        self.eh2.save()
        self.eh3.save()
        response = self.client.get(
            f"/api/velocity/?start={self.two_days_before.strftime('%Y-%m-%d')}&taskboard={self.tb.id}&mode=average"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["velocity"], 12.0)
        # with a velocity of 12.0 it takes 60/12 = 5
        # aka finish before 8 days after today
        end = self.today + timedelta(days=5)
        self.assertEqual(response.data["x"], end.strftime("%Y-%m-%d"))

    def test_get_monthly_average_velocity(self):
        """Test getting the average velocity for monthly data."""
        # get the last month without hard coding the date
        last_month = self.today.replace(day=1) - timedelta(days=1)
        start = last_month.replace(day=1)
        # create history for the first and last day of last month
        create_estimate_hisotry(self.tb, start, 100)
        create_estimate_hisotry(self.tb, last_month, 20)
        response = self.client.get(
            f"/api/velocity/?start={start.strftime('%Y-%m-%d')}&taskboard={self.tb.id}&mode=average&interval=month"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["velocity"], 40.0)
        # 40 hr left this month should finish by next month
        next_month = self.today.replace(month=max(self.today.month % 12 + 1, 1))
        self.assertEqual(response.data["x"], next_month.strftime("%Y-%m-%d"))
