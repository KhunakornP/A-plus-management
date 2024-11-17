"""Test displayed name update."""

from django.urls import reverse
from .templates_for_tests import ProfileTestCase


class UpdateDisplayedNameTest(ProfileTestCase):
    """Tests for update_displayed_name function view."""

    def setUp(self) -> None:
        """Store update_displayed_name url."""
        super().setUp()
        self.url = reverse("manager:update_displayed_name")

    def test_accessing_update_name_page(self):
        """Redirect user to profile page if a GET is recieved."""
        self.client.login(username="parent", password="parent")
        response = self.client.get(self.url)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.client.logout()
        self.client.login(username="student", password="student")
        response2 = self.client.get(self.url)
        self.assertRedirects(
            response2, self.profile, status_code=302, target_status_code=200
        )

    def test_update_parent_name(self):
        """Parent can update their displayed name."""
        self.client.login(username="parent", password="parent")
        new_name = "parent tzu"
        form_data = {"name": new_name}
        response = self.client.post(self.url, form_data)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.parent_info.refresh_from_db()
        self.assertEqual(self.parent_info.displayed_name, new_name)

    def test_update_student_name(self):
        """Student can update their displayed name."""
        self.client.login(username="student", password="student")
        new_name = "student DOS"
        form_data = {"name": new_name}
        response = self.client.post(self.url, form_data)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.student_info.refresh_from_db()
        self.assertEqual(self.student_info.displayed_name, new_name)
