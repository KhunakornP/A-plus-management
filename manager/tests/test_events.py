"""Test cases for models."""

from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from manager.models import Event
from django.urls import reverse


def create_event(
    title: str, start_date: datetime = None, end_date: datetime = None
) -> Event:
    """
    Create an event with the given title, start date, and end date.

    :param title: The name of the event.
    :param start_date: The start date of the event.
    :param end_date: The end date of the event.
    :return: An Event object.
    """
    if not start_date:
        start_date = timezone.now()
    if not end_date:
        end_date = timezone.now()
    return Event.objects.create(title=title, start_date=start_date, end_date=end_date)


# to the group who's working on the taskboard could you please
# refactor this to your test suit. While we're here shall we also do codecov?
class EventViewTests(TestCase):
    """Tests for the front end views for creating and deleting tasks."""

    def test_create_valid_event(self):
        """Test creating an event."""
        url = reverse("manager:create_event")
        data = {
            "title": "New festival",
            "start_date": datetime.now(),
            "end_date": datetime.now(),
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:calendar"))
        self.assertEqual(Event.objects.filter(title="New festival").count(), 1)
        data = {
            "title": "Midterms",
            "start_date": datetime.now(),
            "end_date": datetime.now(),
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:calendar"))
        self.assertEqual(Event.objects.filter(title="Midterms").count(), 1)
        self.assertEqual(Event.objects.count(), 2)

    def test_create_invalid_event(self):
        """
        Test creating an invalid event.

        If a required form field is empty, no event should be created.
        """
        url = reverse("manager:create_event")
        data = {}  # ohno no field data provided!
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:calendar"))
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_valid_event(self):
        """Test deleting a valid event."""
        event = Event.objects.create(title="Bug bounty ISP")
        self.assertEqual(Event.objects.count(), 1)
        url = reverse("manager:delete_event", args=(event.id,))
        response = self.client.post(url)
        self.assertEqual(Event.objects.count(), 0)
        self.assertRedirects(response, reverse("manager:calendar"))

    def test_delete_invalid_event(self):
        """
        Test deleting an event that does not exist.

        The user should be redirected back to the calendar page even if an
        event could not be deleted.
        """
        # delete an event that does not exist (yet)
        url = reverse("manager:delete_event", args=(9999,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse("manager:calendar"))

    def test_update_valid_event(self):
        """Test updating an event with valid information."""
        event = Event.objects.create(title="Bug bounty ISP")
        data = {
            "title": "Team Bug bounty ISP 2024",
            "start_date": datetime.now(),
            "end_date": datetime.now(),
        }
        url = reverse("manager:update_event", args=(event.id,))
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:calendar"))
        updated_event = Event.objects.get(pk=event.id)
        self.assertEqual(
            Event.objects.filter(title="Team Bug bounty ISP 2024").count(), 1
        )
        self.assertEqual(Event.objects.filter(title="Bug bounty ISP").count(), 0)
        self.assertEqual(event, updated_event)

    def test_update_invalid_event(self):
        """Updating an event that does not exist does not create a new event."""
        data = {
            "title": "My first date",
            "start_date": datetime.now(),
            "end_date": datetime.now(),
        }
        url = reverse("manager:update_event", args=(9999,))
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:calendar"))
        self.assertEqual(Event.objects.count(), 0)
