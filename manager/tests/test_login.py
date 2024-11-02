"""Test the context data for the login page."""

from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class LoginViewTestCase(TestCase):
    """Test cases for the login view."""

    def test_get_context_data_for_login(self):
        """Test if the url and client id is correctly passed to the login views."""
        response = self.client.get(reverse("manager:main_login"))
        self.assertQuerySetEqual(
            response.context["callback_uri"], settings.GOOGLE_CALLBACK_URI
        )
        self.assertQuerySetEqual(
            response.context["client_id"], settings.GOOGLE_CLIENT_ID
        )

    def test_is_valid_callback_uri(self):
        """
        Test if the callback uri is valid.

        The uri must follow either the Https or Http schemes.
        """
        response = self.client.get(reverse("manager:main_login"))
        scheme = response.context["callback_uri"].split("/")[0]
        self.assertIn(scheme, ["https:", "http:"])
