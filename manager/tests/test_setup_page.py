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
        redirect_with_next = f"{reverse('manager:main_login')}?next={url}"
        self.assertRedirects(response, redirect_with_next)

    def test_get_setup_page(self):
        """As a non-verified and authenticated user I can access the setup page."""
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:user_setup")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_validated_user_post(self):
        """A verified user cannot POST to the setup page."""
        content_type = ContentType.objects.get_for_model(UserPermissions)
        verified, created = Permission.objects.get_or_create(
            codename="is_verified", content_type=content_type
        )
        self.user1.user_permissions.add(verified)
        self.user = User.objects.get(pk=self.user1.pk)
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:user_setup")
        response = self.client.post(url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:taskboard_index"))

    def test_unauthenticated_post(self):
        """An unauthenticated user cannot set up their account."""
        url = reverse("manager:user_setup")
        response = self.client.post(url)
        self.assertEqual(302, response.status_code)
        redirect_with_next = f"{reverse('manager:main_login')}?next={url}"
        self.assertRedirects(response, redirect_with_next)

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

    def test_get_a_level_student_perms(self):
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
