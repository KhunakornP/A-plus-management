"""Test adding parent to student information."""

from django.contrib.auth.models import Permission
from django.urls import reverse
from manager.models import User
from .templates_for_tests import ProfileTestCase


class AddParentTest(ProfileTestCase):
    """Tests for add_parent function view."""

    def setUp(self) -> None:
        """Login as a student and store add_parent url."""
        super().setUp()
        self.client.login(username="student", password="student")
        self.url = reverse("manager:add_parent")

    def test_accessing_add_parent_page(self):
        """Redirect user to profile page if a GET is recieved."""
        response = self.client.get(self.url)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )

    def test_adding_valid_parent(self):
        """Student can add parent to their parent list using the parent's email."""
        parent = User.objects.create_user(
            username="parent2", password="parent2", email="parent2@parent.com"
        )
        parent.user_permissions.add(Permission.objects.get(codename="is_parent"))
        parent.refresh_from_db()
        form_data = {"email": parent.email}
        response = self.client.post(self.url, form_data)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.student_info.refresh_from_db()
        self.assertEqual(self.student_info.parent.last(), parent)

    def test_adding_none_as_parent(self):
        """Adding non-existent user as parent redirect to profile page with error."""
        fake_email = "unreal@forreal.com"
        form_data = {"email": fake_email}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(f"with email: {fake_email}" in message.message)

    def test_adding_student_as_parent(self):
        """Adding student user as parent redirect to profile page with error."""
        student = User.objects.create_user(
            username="student2", password="student2", email="student2@parent.com"
        )
        form_data = {"email": student.email}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(f"{student.email} is not a parent" in message.message)

    def test_adding_already_in_list(self):
        """Adding existing parent in the list redirect to profile page with warning."""
        form_data = {"email": self.parent.email}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "warning")
        self.assertTrue(f"{self.parent.email} is already" in message.message)
