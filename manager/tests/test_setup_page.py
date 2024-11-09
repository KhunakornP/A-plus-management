"""Test UserInfo creation and update."""

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from manager.models import UserPermissions
from django.test import TestCase


class SetUpPageTest(TestCase):
    """Test cases for the setup page."""

    def setUp(self):
        """Create a new user."""
        super().setUp()
        self.user1 = User.objects.create_user(
            username="myTcasser",
            password="myTcasdabest123",
            email="notavalidemail2@gmail.com",
        )
        self.user1.save()

    def test_user_is_already_verified(self):
        """A verified user cannot access the setup page."""
        content_type = ContentType.objects.get_for_model(UserPermissions)
        verified, created = Permission.objects.get_or_create(
            codename="is_verified", content_type=content_type
        )
        self.user1.user_permissions.add(verified)
        self.user = User.objects.get(pk=self.user1.pk)
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:user_setup")
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:taskboard_index"))

    def test_unauthenticated_access(self):
        """An unauthenticated user is redirected to the login page first."""
        url = reverse("manager:user_setup")
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:main_login"))

    def test_get_regular_student_perms(self):
        """Test getting permissions as a regular student."""
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:user_setup")
        response = self.client.post(url, data={"type": "student", "exam": "false"})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.user = User.objects.get(pk=self.user1.pk)
        self.assertTrue(self.user1.has_perm("manager.is_verified"))
        self.assertFalse(self.user1.has_perm("manager.is_parent"))
        self.assertFalse(self.user1.has_perm("manager.is_taking_A_levels"))

    def test_get_A_level_student_perms(self):
        """Test getting permissions as an A-level student."""
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:user_setup")
        response = self.client.post(url, data={"type": "student", "exam": "true"})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.user = User.objects.get(pk=self.user1.pk)
        self.assertTrue(self.user1.has_perm("manager.is_verified"))
        self.assertFalse(self.user1.has_perm("manager.is_parent"))
        self.assertTrue(self.user1.has_perm("manager.is_taking_A_levels"))

    def test_get_parent_perms(self):
        """Test getting permissions as a parent."""
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:user_setup")
        response = self.client.post(url, data={"type": "parent", "exam": "false"})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.assertTrue(self.user1.has_perm("manager.is_verified"))
        self.assertTrue(self.user1.has_perm("manager.is_parent"))
        self.assertTrue(self.user1.has_perm("manager.is_taking_A_levels"))
