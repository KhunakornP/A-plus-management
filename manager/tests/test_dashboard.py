"""Test the context data in the parent dashboard."""

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone

from manager.models import StudentInfo, UserPermissions
from django.shortcuts import reverse
from manager.tests.templates_for_tests import create_taskboard, create_task


class DashboardViewTestCase(TestCase):
    """Test cases for the dashboard."""

    def setUp(self):
        """Set up parent users and some child users."""
        super().setUp()
        self.username = "DekD"
        self.password = "Tcaslover123"
        self.user1 = User.objects.create_user(
            username="DekD",
            password="Tcaslover123",
            email="notavalidemail@gmail.com",
        )
        self.user1.first_name = "Tester"
        self.user2 = User.objects.create_user(
            username="myTcasser",
            password="myTcasdabest123",
            email="notavalidemail2@gmail.com",
        )
        self.user2.save()
        self.user3 = User.objects.create_user(
            username="John", password="Bestdad1941", email="notavalidemail2@gmail.com"
        )
        self.user3.save()
        self.client.login(username="John", password="Bestdad1941")
        # get the related StudentInfo objects
        si1 = StudentInfo.objects.get(user=self.user1)
        si2 = StudentInfo.objects.get(user=self.user2)
        # update parent in the database
        si1.parent.add(self.user3)
        si2.parent.add(self.user3)
        si1.save()
        si2.save()
        # give the user parent permissions
        content_type = ContentType.objects.get_for_model(UserPermissions)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user3.user_permissions.add(permission)

    def test_access_by_unauthenticated_user(self):
        """Unauthenticated users should be redirected back to the login page."""
        self.client.logout()
        url = reverse("manager:dashboard")
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:main_login"))

    def test_access_by_student(self):
        """Only parents can access the parent dashboard."""
        self.client.login(username="myTcasser", password="myTcasdabest123")
        url = reverse("manager:dashboard")
        response = self.client.get(url)
        # should be redirected to the index page
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("manager:taskboard_index"))

    def test_get_children_info(self):
        """The dashboard page displays all children related to the parent."""
        response = self.client.get(reverse("manager:dashboard"))
        self.assertEqual(200, response.status_code)
        students = StudentInfo.objects.filter(parent=self.user3)
        self.assertQuerySetEqual(
            students, response.context["child_list"], ordered=False
        )

    def test_no_children(self):
        """The dashboard page displays help text if user has no children."""
        # create a fresh student
        self.user4 = User.objects.create_user(
            username="Dio", password="Worstdad1941", email="notavalidemail2@gmail.com"
        )
        self.user4.save()
        self.client.login(username="Dio", password="Worstdad1941")
        # give the user parent permissions
        content_type = ContentType.objects.get_for_model(UserPermissions)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user4.user_permissions.add(permission)
        # go to the dashboard
        response = self.client.get(reverse("manager:dashboard"))
        self.assertEqual(200, response.status_code)
        students = StudentInfo.objects.none()
        self.assertQuerySetEqual(
            students, response.context["child_list"], ordered=False
        )
        self.assertContains(
            response, "You currently do not have any children associated!"
        )

    def test_get_children_statistics(self):
        """Test is the statistics for each child is correct."""
        tb = create_taskboard(self.user1, "studies")
        past_deadline = timezone.now() + timezone.timedelta(days=-1)
        create_task("late1", "TODO", tb, past_deadline)
        create_task("late2", "TODO", tb, past_deadline)
        create_task("done", "DONE", tb, past_deadline)
        create_task("today", "IN_PROGRESS", tb)
        response = self.client.get(reverse("manager:dashboard"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context["today"][0])
        self.assertEqual(1, response.context["fin"][0])
        self.assertEqual(2, response.context["late"][0])
