"""Test taskboard creation, deletion, modification and redirections."""

from django.contrib.auth.models import User
from django.urls import reverse
from manager.models import Taskboard
from typing import Any, Optional
from rest_framework import status
from .templates_for_tests import create_taskboard, BaseTestCase


def create_taskboard_json(
    user: int,
    name: str = "Today",
    id: Optional[int] = None,
) -> dict[str, Any]:
    """Create a dict with the given name.

    :returns: A Dictionary containing taskboard data.
    """
    data = {"name": name, "user": user}
    if id is not None:
        data["id"] = id
    return data


class TaskboardTests(BaseTestCase):
    """Test creating, deleting, getting and modifying taskboards."""

    def test_create_valid_taskboard(self):
        """Test creating valid taskboard."""
        tb = create_taskboard_json(self.user1.pk, "Hello")
        self.client.post("/api/taskboards/", tb, format="json")
        self.assertEqual(Taskboard.objects.count(), 1)
        self.assertEqual(Taskboard.objects.first().name, "Hello")

    def test_create_invalid_taskboard(self):
        """Test creating valid taskboard."""
        self.client.post("/api/taskboards/", {}, format="json")
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_delete_valid_taskboard(self):
        """Test deleting valid taskboard."""
        tb = create_taskboard(user=self.user1)
        self.assertEqual(Taskboard.objects.count(), 1)
        self.client.delete(f"/api/taskboards/{tb.id}/")
        self.assertEqual(Taskboard.objects.count(), 0)

    def test_delete_invalid_taskboard(self):
        """Test deleting invalid taskboard."""
        tb = create_taskboard(user=self.user1)
        self.client.delete(f"/api/taskboards/{tb.id * 727}/")
        self.assertEqual(Taskboard.objects.count(), 1)

    def test_updating_taskboard(self):
        """Test updating the taskboard's attributes."""
        tb = create_taskboard(self.user1, "goodbye")
        new_tb = create_taskboard_json(self.user1.pk, name="yahallo", id=tb.id)
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
        tb = create_taskboard(self.user1, "goodbye")
        new_tb = create_taskboard_json(self.user1.pk, "yahallo")
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
        tb = create_taskboard(self.user1, "goodbye")
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

    def test_get_user_taskboard(self):
        """Test getting the taskboard index of a different user."""
        user2 = User.objects.create_user(
            username="bogus man", email="testuser@nowhere.com"
        )
        user2.save()
        url = reverse("manager:user_tb_index", args=(user2.id,))
        response = self.client.get(url)
        self.assertEqual(response.context["viewed_user"].id, user2.id)
        url = reverse("manager:user_tb_index", args=(9999,))
        response = self.client.get(url)
        with self.assertRaises(TypeError):
            # should not be any context data
            self.assertEqual(response.context["viewed_user"], 0)

    def test_get_others_taskboard_detail(self):
        """Test viewing the taskboard of a different user."""
        user2 = User.objects.create_user(
            username="bogus man", email="testuser@nowhere.com"
        )
        user2.save()
        tb = create_taskboard(user2, "A-levels")
        url = reverse("manager:user_tb_details", args=(user2.id, tb.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
