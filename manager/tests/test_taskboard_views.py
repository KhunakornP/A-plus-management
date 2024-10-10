"""Test taskboard creation, deletion, modification and redirections."""

from django.test import TestCase
from django.urls import reverse

from manager.models import Taskboard


def create_taskboard(tb_name: str) -> Taskboard:
    """Create a new taskboard.

    :param tb_name: taskboard name
    :return: a Taskboard object.
    """
    return Taskboard.objects.create(name=tb_name)


class TaskboardTests(TestCase):
    """Test creating, deleting and modifying taskboards."""

    def test_create_valid_taskboard(self):
        """Test creating valid taskboard."""
        url = reverse("manager:create_taskboard")
        tb_name = "Test Taskboard"
        tb_data = {"name": tb_name}
        response = self.client.post(url, tb_data)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        taskboard = Taskboard.objects.filter(name=tb_name)
        self.assertEqual(taskboard.count(), 1)

    def test_create_invalid_taskboard(self):
        """Test creating valid taskboard."""
        url = reverse("manager:create_taskboard")
        taskboard_data = {}
        response = self.client.post(url, taskboard_data)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_delete_valid_taskboard(self):
        """Test deleting valid taskboard."""
        tb_name = "Taskboard1"
        tb = create_taskboard(tb_name)
        self.assertEqual(Taskboard.objects.count(), 1)
        url = reverse("manager:delete_taskboard", args=(tb.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse("manager:taskboard_index"))
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_delete_invalid_taskboard(self):
        """Test deleting invalid taskboard."""
        self.assertEqual(Taskboard.objects.count(), 0)
        url = reverse("manager:delete_taskboard", args=(400,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_modifying_taskboard(self):
        """Test modifying the taskboard."""
        tb = create_taskboard("Taskboard 1")
        new_name = "Event Generator 3000"
        new_data = {"name": new_name}
        url = reverse("manager:update_taskboard", args=(tb.id,))
        response = self.client.post(url, new_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Taskboard.objects.filter(name=new_name).count(), 1)
