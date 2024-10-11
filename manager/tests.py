"""Test cases for models."""

from datetime import datetime, time, date
from django.utils import timezone
from django.test import TestCase
from .models import Taskboard, Task, Event
from django.urls import reverse


def create_taskboard(name: str = "Today"):
    """
    Create a taskboard with the given name.

    :returns: A Taskboard object with the given name.
    """
    return Taskboard.objects.create(name=name)


def create_task(title: str, status: str, taskboard: Taskboard, end_date=None):
    """
    Create a task with the given parameters.

    :param title: The task's title
    :param status: The task's current status
    :param taskboard: The taskboard the task belongs to
    :param end_date: Optional, The deadline for the task
    :returns: A Task object with the given parameters
    """
    if not end_date:
        return Task.objects.create(title=title, status=status, taskboard=taskboard)
    # else create a task with an end date
    return Task.objects.create(
        title=title, status=status, end_date=end_date, taskboard=taskboard
    )


class TaskboardModelTestcase(TestCase):
    """Test cases for the Taskboard class."""

    def test_create_taskboard(self):
        """
        Test the creation of task boards.

        A task board should always have a name and task boards with the
        same name are different objects.
        """
        t1 = create_taskboard()
        t2 = create_taskboard("Study plans")
        t3 = create_taskboard()
        self.assertTrue(t1.name, "Today")
        self.assertTrue(t2.name, "Study plans")
        self.assertNotEqual(t1, t3)


class TaskModelTestcase(TestCase):
    """Testcase for the Task class."""

    def test_taskboard_has_tasks(self):
        """
        A task board has associated tasks.

        Tasks are only associated with one taskboard and each taskboard
        should display all tasks.
        """
        taskboard = create_taskboard()
        t1 = create_task("Study math", "TODO", taskboard)
        t2 = create_task("Do biology homework", "TODO", taskboard)
        t3 = create_task("Clean the house", "Finished", taskboard)
        self.assertEqual([t1, t2, t3], list(taskboard.task_set.all()))

    def test_task_default_end_date(self):
        """The default end date of a task is midnight of the date of its creation."""
        taskboard = create_taskboard()
        task = create_task("Do homework", "TODO", taskboard)
        midnight = datetime.combine(date.today(), time.min)
        # midnight is actually modelled as 0:00 of the next day
        self.assertTrue(task.end_date, midnight + timezone.timedelta(days=+1))

    def test_task_have_same_name(self):
        """
        Tasks can have the same name.

        Multiple tasks can have the same name but are associated with
        different questions.
        """
        taskboard1 = create_taskboard()
        taskboard2 = create_taskboard("project delta")
        task1 = create_task("Study math", "TODO", taskboard1)
        task2 = create_task("Study chemistry", "TODO", taskboard1)
        task3 = create_task("Pick a color palette", "TODO", taskboard2)
        task4 = create_task("Sketch the subject", "TODO", taskboard2)
        self.assertEqual([task1, task2], list(taskboard1.task_set.all()))
        self.assertEqual([task3, task4], list(taskboard2.task_set.all()))


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

    def test_create_invalid_task(self):
        """
        Test creating an invalid event.

        If a required form field is empty, no event should be created.
        """
        url = reverse("manager:create_event")
        data = {}  # ohno no field data provided!
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("manager:calendar"))
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_valid_task(self):
        """Test deleting a valid event."""
        event = Event.objects.create(title="Bug bounty ISP")
        self.assertEqual(Event.objects.count(), 1)
        url = reverse("manager:delete_event", args=(event.id,))
        response = self.client.post(url)
        self.assertEqual(Event.objects.count(), 0)
        self.assertRedirects(response, reverse("manager:calendar"))

    def test_delete_invalid_task(self):
        """
        Test deleting an event that does not exist.

        The user should be redirected back to the calendar page even if an
        event could not be deleted.
        """
        # delete an event that does not exist (yet)
        url = reverse("manager:delete_event", args=(9999,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse("manager:calendar"))
