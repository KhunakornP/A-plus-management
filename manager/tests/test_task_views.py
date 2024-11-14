"""Test task creation, deletion, modification and redirections."""

from datetime import datetime
from rest_framework import status
from django.utils import timezone
from django.test import TestCase
from manager.models import Taskboard, Task
from typing import Any, Optional
from .templates_for_tests import create_taskboard, create_task
from django.contrib.auth.models import User


def create_task_json(
    title: str,
    task_status: str,
    taskboard: Taskboard,
    end_date: Optional[datetime] = None,
    id: Optional[int] = None,
) -> dict[str, Any]:
    """
    Create a task as a Dict with the given title and end date.

    :param title: The name of the task.
    :param end_date: The due date of the task.
    :return: Dictionary containing task data.
    """
    if not task_status:
        task_status = "TODO"
    if not end_date:
        end_date = timezone.now()

    data = {}
    if id is not None:
        data["id"] = str(id)

    data.update(
        {
            "title": title,
            "status": task_status.upper(),
            "start": end_date,
            "taskboard": taskboard.id,
        }
    )

    return data


class TaskViewTests(TestCase):
    """Tests for TaskViewSet."""

    def setUp(self):
        """Create Taskboards with some tasks."""
        super().setUp()
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

    def test_get_all_tasks(self):
        """Test getting all tasks info."""
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_one_task(self):
        """Test getting a specific task info."""
        response = self.client.get(f"/api/tasks/{self.task_2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task_2.title)
        self.assertEqual(response.data["status"], self.task_2.status)

    def test_get_invalid_task(self):
        """Test getting a non-existent task info."""
        response = self.client.get("/api/tasks/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_status_not_done(self):
        """Test getting tasks with status not equal to DONE."""
        create_task("Done Task", "DONE", self.taskboard_1)
        response = self.client.get("/api/tasks/?exclude=DONE")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_all_status_not_in_progress(self):
        """Test getting tasks with status not equal to INPROGRESS."""
        response = self.client.get("/api/tasks/?exclude=INPROGRESS")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_all_status_not_todo(self):
        """Test getting tasks with status not equal to TODO."""
        response = self.client.get("/api/tasks/?exclude=TODO")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_tasks_in_one_taskboard(self):
        """Test getting tasks in a specific taskboard."""
        response = self.client.get(
            f"/api/tasks/?taskboard={self.taskboard_1.id}&exclude=TODO"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_tasks_in_one_taskboard_exclude_status(self):
        """Test getting tasks except those with the given status in a taskboard."""
        response = self.client.get(f"/api/tasks/?taskboard={self.taskboard_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_valid_task(self):
        """Test creating a Task."""
        task = create_task_json("Hello", "DONE", self.taskboard_2)
        response = self.client.post("/api/tasks/", task, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.last().title, "Hello")

    def test_create_invalid_task(self):
        """
        Test creating an invalid task.

        If a required form field is empty, no task should be created.
        """
        response = self.client.post("/api/tasks/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 3)

    def test_delete_valid_task(self):
        """Test deleting a valid task."""
        response_1 = self.client.delete(f"/api/tasks/{self.task_2.id}/")
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)
        response_2 = self.client.delete(f"/api/tasks/{self.task_3.id}/")
        self.assertEqual(response_2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_invalid_task(self):
        """Test deleting an invalid task."""
        response = self.client.delete("/api/tasks/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.count(), 3)

    def test_update_valid_task(self):
        """Test updating a task with valid information."""
        task = create_task_json("Task 1 Edited", "DONE", self.taskboard_1)
        response = self.client.put(
            f"/api/tasks/{self.task_1.id}/",
            task,
            format="json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.title, "Task 1 Edited")
        self.assertEqual(self.task_1.status, "DONE")

    def test_update_task_with_invalid_data(self):
        """Updating a task with invalid data should raise HTTP 400."""
        task = {"title": "", "taskboard": ""}
        response = self.client.put(
            f"/api/tasks/{self.task_1.id}/",
            task,
            format="json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.title, "Task 1")
        self.assertEqual(self.task_1.status, "TODO")

    def test_update_non_existent_task(self):
        """Updating a task that does not exist should raise HTTP 404."""
        task = create_task_json("Task 1 Edited", "DONE", self.taskboard_1)
        response = self.client.put(
            "/api/tasks/9999/",
            task,
            format="json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.title, "Task 1")
        self.assertEqual(self.task_1.status, "TODO")
