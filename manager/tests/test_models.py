"""Test cases for models."""

from datetime import datetime, time, date
from django.utils import timezone
from django.test import TestCase
from manager.models import Taskboard, Task


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
