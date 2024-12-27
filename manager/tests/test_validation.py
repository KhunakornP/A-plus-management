"""Test user checking for CRUD operations."""

from datetime import datetime
from rest_framework import status
from django.utils import timezone
from django.test import TestCase
from .templates_for_tests import create_taskboard, create_task
from django.contrib.auth.models import User, Permission


class TaskViewTests(TestCase):
    """Tests for TaskViewSet."""

    def setUp(self):
        """Create Taskboards with some tasks."""
        super().setUp()
        # add the base user
        self.username = "Tester"
        self.password = "Bestbytest!123"
        self.user1 = User.objects.create_user(
            username=self.username, email="testuser@nowhere.com"
        )
        self.user1.set_password(self.password)
        self.user1.save()
        self.client.login(username=self.username, password=self.password)
        due_date = timezone.make_aware(datetime(2030, 10, 2, 10))
        self.taskboard_1 = create_taskboard(self.user1, "Today")
        self.taskboard_2 = create_taskboard(self.user1, "Today but number 2")
        self.task_1 = create_task("Task 1", "TODO", self.taskboard_1, due_date)
        self.task_2 = create_task("Task 2", "INPROGRESS", self.taskboard_1)
        self.task_3 = create_task("Task 3", "TODO", self.taskboard_2, due_date)
        # add the student
        self.user2 = User.objects.create_user(
            username="Conway", email="testuser2@nowhere.com"
        )
        self.user2.set_password("Sonata")
        self.user2.save()
        self.user2.studentinfo.parent.add(self.user1)
        # A random bad guy who wants to leak data
        self.user3 = User.objects.create_user(
            username="JohnBadguy", email="Hacker@anywhere.com"
        )
        self.user3.set_password("l33tcrew420")
        self.user3.save()

    def test_get_other_users_tasks(self):
        """Only the parent of a user or the user can view the user's tasks."""
        tb = create_taskboard(self.user2, "Shopping list")
        create_task("Buy milk", "TODO", tb)
        create_task("Buy cool toy", "INPROGRESS", tb)
        self.user1.user_permissions.add(Permission.objects.get(codename="is_parent"))
        self.assertTrue(self.user1.has_perm("manager.is_parent"))
        response = self.client.get(f"/api/tasks/?user={self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.client.login(username="JohnBadguy", password="l33tcrew420")
        response = self.client.get(f"/api/tasks/?user={self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_users_taskboard(self):
        """Only the parent of a user or the user can view the user's taskboards."""
        tb = create_taskboard(self.user2, "Shopping list")
        create_task("Buy milk", "TODO", tb)
        self.user1.user_permissions.add(Permission.objects.get(codename="is_parent"))
        self.assertTrue(self.user1.has_perm("manager.is_parent"))
        response = self.client.get(f"/api/tasks/?taskboard={tb.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.client.login(username="JohnBadguy", password="l33tcrew420")
        response = self.client.get(f"/api/tasks/?taskboard={tb.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
