"""Test task creation, deletion, modification and redirections."""

from django.test import TestCase
from django.urls import reverse

from manager.models import Taskboard, Task


def create_taskboard(tb_name: str) -> Taskboard:
    """Create a new taskboard.

    :param tb_name: taskboard name
    :return: a Taskboard object
    """
    return Taskboard.objects.create(name=tb_name)


def create_task(title: str, tb: Taskboard) -> Task:
    """Create a new Task bounded to a specific taskboard.

    :param title: Task's title
    :param tb: the Taskboard that this task would be bounded to
    :return: a Task object
    """
    return Task.objects.create(title=title, taskboard=tb)


class TaskTests(TestCase):
    """Test task creation, modification and deletion."""

    def test_create_valid_task(self):
        """Test creating a Task."""
        tb = create_taskboard("Taskboard 1")
        url = reverse("manager:create_task", args=(tb.id,))
        task_title = "Task1"
        data = {"title": task_title, "taskboard": tb.id}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:taskboard", args=(tb.id,)))
        self.assertEqual(Task.objects.filter(title=task_title).count(), 1)
        self.assertEqual(Task.objects.filter(taskboard=tb).count(), 1)

    def test_create_invalid_task(self):
        """Test creating an invalid task."""
        tb = create_taskboard("Taskboard 1")
        url = reverse("manager:create_task", args=(tb.id,))
        data = {}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_valid_task(self):
        """Test deleting a valid task."""
        tb = create_taskboard("Taskboard 1")
        task = create_task("title", tb)
        self.assertEqual(Task.objects.count(), 1)
        url = reverse("manager:delete_task", args=(task.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse("manager:taskboard", args=(tb.id,)))
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_invalid_task(self):
        """Test deleting an invalid task."""
        url = reverse("manager:delete_task", args=(3000,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse("manager:taskboard_index"))

    def test_update_task(self):
        """Test updating attributes in a task."""
        tb = create_taskboard("Hello World")
        task = create_task("Das Kapital", tb)
        new_title = "Wealth of Nations"
        new_data = {"title": new_title, "taskboard": tb}
        url = reverse("manager:update_task", args=(task.id,))
        response = self.client.post(url, new_data)
        self.assertRedirects(response, reverse("manager:taskboard", args=(tb.id,)))
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.filter(title=new_title).count(), 1)
        self.assertEqual(
            task.taskboard, Task.objects.filter(title=new_title).first().taskboard
        )

    def test_update_non_existent_task(self):
        """Test updating attributes in a task."""
        tb = create_taskboard("Hello World")
        new_title = "Wealth of Nations"
        new_data = {"title": new_title, "taskboard": tb}
        url = reverse("manager:update_task", args=(3000,))
        response = self.client.post(url, new_data)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.assertEqual(Task.objects.count(), 0)

    def test_update_task_with_invalid_data(self):
        """Test updating a task with invalid attributes."""
        tb = create_taskboard("Hello World")
        old_title = "Das Kapital"
        task = create_task(old_title, tb)
        url = reverse("manager:update_task", args=(task.id,))
        response = self.client.post(url, {})
        self.assertRedirects(response, reverse("manager:taskboard", args=(tb.id,)))
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.filter(title=old_title).count(), 1)
