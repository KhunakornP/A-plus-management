"""Test Burndown chart views."""

from django.test import TestCase
from django.urls import reverse

from manager.models import Taskboard


def create_taskboard(name: str = "Today") -> Taskboard:
    """
    Create a taskboard with the given name.

    :returns: A Taskboard object with the given name.
    """
    return Taskboard.objects.create(name=name)


class TestBurndownChartView(TestCase):
    """Test the burndown chat view."""

    def test_get_request(self):
        """Test sending get request."""
        tb = create_taskboard()
        url = reverse("manager:burndown_chart", args=(tb.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        """Test sending post request.

        The BurndownChartView should get the events data.
        """
        tb = create_taskboard()
        url = reverse("manager:burndown_chart", args=(tb.id,))
        data = {"events": ["a", "b", "v"]}
        response = self.client.post(url, data)
        self.assertEqual(response.context["events"], data["events"])
        self.assertEqual(response.status_code, 200)
