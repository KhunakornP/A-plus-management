"""Test taskboard creation, deletion, modification and redirections."""

from django.test import TestCase
from manager.models import Taskboard
from typing import Any, Optional
from rest_framework import status


def create_taskboard(name: str = "Today") -> Taskboard:
    """Create a taskboard with the given name.

    :returns: A Taskboard object with the given name.
    """
    return Taskboard.objects.create(name=name)


def create_taskboard_json(
    name: str = "Today", id: Optional[int] = None
) -> dict[str, Any]:
    """Create a dict with the given name.

    :returns: A Dictionary containing taskboard data.
    """
    data = {"name": name}
    if id is not None:
        data["id"] = id
    return data


class TaskboardTests(TestCase):
    """Test creating, deleting and modifying taskboards."""

    def test_create_valid_taskboard(self):
        """Test creating valid taskboard."""
        tb = create_taskboard_json("Hello")
        self.client.post("/api/taskboards/", tb, format="json")
        self.assertEqual(Taskboard.objects.count(), 1)
        self.assertEqual(Taskboard.objects.first().name, "Hello")

    def test_create_invalid_taskboard(self):
        """Test creating valid taskboard."""
        self.client.post("/api/taskboards/", {}, format="json")
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_delete_valid_taskboard(self):
        """Test deleting valid taskboard."""
        tb = create_taskboard()
        self.assertEqual(Taskboard.objects.count(), 1)
        self.client.delete(f"/api/taskboards/{tb.id}/")
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_delete_invalid_taskboard(self):
        """Test deleting invalid taskboard."""
        tb = create_taskboard()
        self.client.delete(f"/api/taskboards/{tb.id * 727}/")
        self.assertEqual(Taskboard.objects.count(), 1)

    def test_updating_taskboard(self):
        """Test updating the taskboard's attributes."""
        tb = create_taskboard("goodbye")
        new_tb = create_taskboard_json(name="yahallo", id=tb.id)
        response = self.client.put(
            f"/api/taskboards/{tb.id}/",
            new_tb,
            format="json",
            content_type="application/json",
        )
        tb.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Taskboard.objects.count(), 1)
        self.assertEqual(tb.name, "yahallo")

    def test_updating_non_existent_taskboard(self):
        """Test updating non-existent taskboard with valid attributes."""
        tb = create_taskboard("goodbye")
        new_tb = create_taskboard_json("yahallo")
        response = self.client.put(
            f"/api/taskboards/{tb.id * 420 // 69}/",
            new_tb,
            format="json",
            content_type="application/json",
        )
        tb.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Taskboard.objects.count(), 1)
        self.assertEqual(tb.name, "goodbye")

    def test_updating_taskboard_with_invalid_data(self):
        """Test updating a taskboard with invalid data."""
        tb = create_taskboard("goodbye")
        new_tb = {"skibidi": "toilet", "id": tb.id}
        self.client.put(
            f"/api/taskboards/{tb.id}/",
            new_tb,
            format="json",
            content_type="application/json",
        )
        tb.refresh_from_db()
        self.assertEqual(Taskboard.objects.count(), 1)
        self.assertEqual(tb.name, "goodbye")
