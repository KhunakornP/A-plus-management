"""Test updating student's A-level permission."""

from django.urls import reverse
from django.contrib.auth.models import Permission
from manager.models import User
from .templates_for_tests import ProfileTestCase


class UpdateALevelPermissionTest(ProfileTestCase):
    """Tests for update_a_level_permission function view."""

    def setUp(self) -> None:
        """Login as a student and store update_a_level_permission url."""
        super().setUp()
        self.client.login(username="student", password="student")
        self.url = reverse("manager:update_a_level")

    def test_accessing_update_a_level_permission_page(self):
        """Redirect user to profile page if a GET is recieved."""
        response = self.client.get(self.url)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )

    def test_add_a_level_permission(self):
        """Students can register themselves as A-level examinee."""
        form_data = {"choice": "Yes"}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.assertTrue(self.student.has_perm("manager.is_taking_A_levels"))
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("now access" in message.message)

    def test_remove_a_level_permission(self):
        """Student can remove thier status as a A-level examinee."""
        self.student.user_permissions.add(
            Permission.objects.get(codename="is_taking_A_levels")
        )
        self.assertTrue(self.student.has_perm("manager.is_taking_A_levels"))
        form_data = {"choice": "No"}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(
            response, self.profile, status_code=302, target_status_code=200
        )
        self.student = User.objects.get(pk=self.student.pk)
        self.assertFalse(self.student.has_perm("manager.is_taking_A_levels"))
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("removed" in message.message)
