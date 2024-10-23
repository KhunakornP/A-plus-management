"""Test cases for models."""

from datetime import datetime
from rest_framework import status
from django.utils import timezone
from django.test import TestCase
from manager.models import Event
from typing import Any, Optional


def create_event(
    title: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Event:
    """
    Create an event in Django models with the given title, start date, and end date.

    :param title: The name of the event.
    :param start_date: The start date of the event.
    :param end_date: The end date of the event.
    :return: An Event object.
    """
    if not start_date:
        start_date = timezone.now()
    if not end_date:
        end_date = timezone.now()
    return Event.objects.create(
        title=title, start_date=start_date, end_date=end_date, details="something"
    )


def create_event_json(
    title: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    id: Optional[int] = None,
) -> dict[str, Any]:
    """
    Create an event as a Dict with the given title, start date, and end date.

    :param title: The name of the event.
    :param start_date: The start date of the event.
    :param end_date: The end date of the event.
    :return: Dictionary containing event data.
    """
    if not start_date:
        start_date = timezone.now()
    if not end_date:
        end_date = timezone.now()

    data = {"details": "something"}
    if id is not None:
        data["id"] = str(id)

    data.update({"title": title, "start_date": start_date, "end_date": end_date})

    return data


# to the group who's working on the taskboard could you please
# refactor this to your test suit. While we're here shall we also do codecov?
class EventViewSetTests(TestCase):
    """Tests for the Event API viewset."""

    def test_create_valid_event(self):
        """Test creating an event."""
        event = create_event_json("Hello")
        self.client.post("/api/events/", event, format="json")
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().title, "Hello")

    def test_create_invalid_event(self):
        """
        Test creating an invalid event.

        If a required form field is empty, no event should be created.
        """
        self.client.post("/api/events/", {}, format="json")
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_valid_event(self):
        """Test deleting a valid event."""
        event = create_event("hello")
        self.assertEqual(Event.objects.count(), 1)
        self.client.delete(f"/api/events/{event.id}/")
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_invalid_event(self):
        """
        Test deleting an event that does not exist.

        The user should be redirected back to the calendar page even if an
        event could not be deleted.
        """
        event = create_event("hello")
        self.client.delete(f"/api/events/{event.id * 420 // 69}/")
        self.assertEqual(Event.objects.count(), 1)

    def test_update_valid_event(self):
        """Test updating an event with valid information."""
        event = create_event("goodbye")
        new_event = create_event_json(title="yahallo", id=event.id)
        response = self.client.put(
            f"/api/events/{event.id}/",
            new_event,
            format="json",
            content_type="application/json",
        )
        event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.title, "yahallo")

    def test_update_non_existent_event(self):
        """Updating an event that does not exist does not create a new event."""
        event = create_event("goodbye")
        new_event = create_event_json("yahallo")
        response = self.client.put(
            f"/api/events/{event.id * 420 // 69}/",
            new_event,
            format="json",
            content_type="application/json",
        )
        event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.title, "goodbye")

    def test_update_event_with_invalid_data(self):
        """Updating an event with invalid data should raise HTTP 400."""
        event = create_event("goodbye")
        new_event = {"name": 1234, "id": event.id}
        self.client.put(
            f"/api/events/{event.id}/",
            new_event,
            format="json",
            content_type="application/json",
        )
        event.refresh_from_db()
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.title, "goodbye")

    def test_get_one_event(self):
        """Test getting a specifc event instance."""
        time1 = timezone.make_aware(datetime(2020, 3, 9, 12, 00, 00))
        time2 = timezone.make_aware(datetime(2020, 10, 9, 12, 00, 00))
        create_event("ni hao")
        create_event("ni hao 2")
        event = create_event("zaijian", time1, time2)
        event_json = create_event_json(event.title, time1, time2, event.id)
        request = self.client.get(f"/api/events/{event.id}/")
        self.assertEqual(request.data["title"], event_json["title"])
        self.assertEqual(
            datetime.fromisoformat(request.data["start_date"]), event_json["start_date"]
        )
        self.assertEqual(
            datetime.fromisoformat(request.data["end_date"]), event_json["end_date"]
        )
        self.assertEqual(request.data["details"], event_json["details"])

    def test_get_all_events(self):
        """Test getting all events."""
        create_event("ni hao")
        create_event("ni hao 2")
        create_event("zaijian")
        request = self.client.get("/api/events/")
        self.assertEqual(len(request.data), 3)
