"""Test Burndown chart views."""

from django.test import TestCase
# from django.urls import reverse
# from .templates_for_tests import create_taskboard, create_estimate_hisotry
# from datetime import date, timedelta
# from manager.models import Taskboard, EstimateHistory


class EstimateHistoryViewTests(TestCase):
    """Tests for TaskViewSet."""

    def setUp(self):
        """Create EstimateHistory objects."""
        pass

    def test_get_all_estimate_history(self):
        """Test getting all estimate history info."""
        pass

    def test_get_eh_of_taskboard(self):
        """Test getting estimate_history in a specific taskboard."""
        pass

    def test_get_invalid_estimate_history(self):
        """Test getting a non-existent estimate history info."""
        pass


# class EstimateHistoryJsonTests(TestCase):
#     """Test the json response for EstimateHistory objects."""

#     def test_estimate_histories_json(self):
#         """Test json response."""
#         tb = create_taskboard("Taskboard 1")

#         create_estimate_hisotry(
#             tb, date=date.today() - timedelta(days=3), time_remaining=50
#         )
#         create_estimate_hisotry(
#             tb, date=date.today() - timedelta(days=2), time_remaining=40
#         )
#         create_estimate_hisotry(
#             tb, date=date.today() - timedelta(days=1), time_remaining=20
#         )

#         url = reverse(
#             "/api/estimate_history/",
#             kwargs={"taskboard_id": tb.id},
#         )
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)


# class TestBurndownChartView(TestCase):
#     """Test the burndown chat view."""

#     def test_get_request(self):
#         """Test sending get request."""
#         tb = create_taskboard()
#         url = reverse("manager:burndown_chart", args=(tb.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_post_request(self):
#         """Test sending post request.

#         The BurndownChartView should get the events data.
#         """
#         tb = create_taskboard()
#         url = reverse("manager:burndown_chart", args=(tb.id,))
#         data = {"events": ["a", "b", "v"]}
#         response = self.client.post(url, data)
#         self.assertEqual(response.context["events"], data["events"])
#         self.assertEqual(response.status_code, 200)
