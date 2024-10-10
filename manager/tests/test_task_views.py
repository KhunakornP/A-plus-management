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


class TaskTests(TestCase):
    """Test task creation, modification and deletion."""
    
    def test_create_valid_task(self):
        """Test creating a Task."""
        tb = create_taskboard("Taskboard 1")
        url = reverse("manager:create_task", args=(tb.id,))
        task_title = "Task1"
        data = {"title" : task_title, "taskboard": tb.id}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:taskboard", args=(tb.id,)))
        self.assertEqual(Task.objects.filter(title=task_title).count(), 1)
        self.assertEqual(Task.objects.filter(taskboard=tb).count(), 1)