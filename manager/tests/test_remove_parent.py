"""Test removing parent from student information."""

from django.urls import reverse
from .templates_for_tests import ProfileTestCase


class RemoveParentTest(ProfileTestCase):
    """Tests for remove_parent function view."""

    def setUp(self) -> None:
        """Login as a student and store remove_parent url."""
        super().setUp()
        self.client.login(username="student", password="student")
        self.url = reverse("manager:remove_parent")

    def test_accessing_remove_parent_page(self):
        """Redirect user to profile page if a GET is recieved."""
        response = self.client.get(self.url)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )

    def test_remove_valid_parent(self):
        """Student can remove parent from thier parent list."""
        form_data = {"email": self.parent.email}
        response = self.client.post(self.url, form_data)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.student_info.refresh_from_db()
        self.assertEqual(self.student_info.parent.count(), 0)

    def test_remove_non_existent_parent(self):
        """Removing non-existent parent redirect to profile page with error."""
        fake_email = "4^0/\/j^^oh|_|$69420@yahoo.com"
        form_data = {"email": fake_email}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(f"no user with email: {fake_email}" in message.message)
