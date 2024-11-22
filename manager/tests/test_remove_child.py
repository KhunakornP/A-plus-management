"""Test removing child from parent information."""

from django.urls import reverse
from .templates_for_tests import ProfileTestCase


class RemoveChildTest(ProfileTestCase):
    """Tests for remove_child function view."""

    def setUp(self) -> None:
        """Login as a parent and store remove_child url."""
        super().setUp()
        self.client.login(username="parent", password="parent")
        self.url = reverse("manager:remove_child")

    def test_accessing_remove_child_page(self):
        """Redirect user to profile page if a GET is recieved."""
        response = self.client.get(self.url)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )

    def test_remove_valid_child(self):
        """Parent can remove child from thier children list."""
        form_data = {"email": self.student.email}
        response = self.client.post(self.url, form_data)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.student_set.count(), 0)

    def test_remove_non_existent_child(self):
        """Removing non-existent child redirect to profile page with error."""
        fake_email = "4^0/\/j^^oh|_|$69420@yahoo.com"
        form_data = {"email": fake_email}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(f"no user with email: {fake_email}" in message.message)
