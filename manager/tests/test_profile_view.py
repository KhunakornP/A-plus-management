"""Test the context data of the profile page."""

from .templates_for_tests import ProfileTestCase


class ProfileViewTest(ProfileTestCase):
    """Tests for the ProfileView page."""

    def test_parent_profile(self):
        """Parent can see thier displayed name and their children's email."""
        self.client.login(username="parent", password="parent")
        response = self.client.get(self.profile)
        self.assertContains(response, self.parent_info.displayed_name)
        self.assertContains(response, self.student.email)

    def test_student_profile(self):
        """Students can see thier displayed name and their parent's email."""
        self.client.login(username="student", password="student")
        response = self.client.get(self.profile)
        self.assertContains(response, self.student_info.displayed_name)
        self.assertContains(response, self.parent.email)
