"""Test Burndown chart views."""

from django.urls import reverse

from .templates_for_tests import create_taskboard, BaseTestCase


class TestBurndownChartView(BaseTestCase):
    """Test the burndown chat view."""

    def test_get_request(self):
        """Test sending get request."""
        tb = create_taskboard(self.user1)
        url = reverse("manager:burndown_chart", args=(tb.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        """Test sending post request.

        The BurndownChartView should get the events data.
        """
        tb = create_taskboard(self.user1)
        url = reverse("manager:burndown_chart", args=(tb.id,))
        data = {"events": ["a", "b", "v"]}
        response = self.client.post(url, data)
        self.assertEqual(response.context["events"], data["events"])
        self.assertEqual(response.status_code, 200)
