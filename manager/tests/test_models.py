"""Test cases for models."""

from datetime import datetime, time, date
from django.utils import timezone
from manager.models import Task
from .templates_for_tests import create_task, create_taskboard, BaseTestCase


class TaskboardModelTestcase(BaseTestCase):
    """Test cases for the Taskboard class."""

    def test_create_taskboard(self):
        """
        Test the creation of task boards.

        A task board should always have a name and task boards with the
        same name are different objects.
        """
        t1 = create_taskboard(self.user1)
        t2 = create_taskboard(self.user1, "Study plans")
        t3 = create_taskboard(self.user1)
        self.assertTrue(t1.name, "Today")
        self.assertTrue(t2.name, "Study plans")
        self.assertNotEqual(t1, t3)


class TaskModelTestcase(BaseTestCase):
    """Testcase for the Task class."""

    def test_taskboard_has_tasks(self):
        """
        A task board has associated tasks.

        Tasks are only associated with one taskboard and each taskboard
        should display all tasks.
        """
        taskboard = create_taskboard(self.user1)
        t1 = create_task("Study math", "TODO", taskboard)
        t2 = create_task("Do biology homework", "TODO", taskboard)
        t3 = create_task("Clean the house", "Finished", taskboard)
        self.assertEqual([t1, t2, t3], list(taskboard.task_set.all()))

    def test_task_default_end_date(self):
        """The default end date of a task is midnight of the date of its creation."""
        taskboard = create_taskboard(self.user1)
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
        taskboard1 = create_taskboard(self.user1)
        taskboard2 = create_taskboard(self.user1, "project delta")
        task1 = create_task("Study math", "TODO", taskboard1)
        task2 = create_task("Study chemistry", "TODO", taskboard1)
        task3 = create_task("Study math", "TODO", taskboard2)
        task4 = create_task("Study chemistry", "TODO", taskboard2)
        self.assertEqual([task1, task2], list(taskboard1.task_set.all()))
        self.assertEqual([task3, task4], list(taskboard2.task_set.all()))

    def test_task_default_time_estimate(self):
        """The default time estimate of a task is 0 hours."""
        taskboard = create_taskboard(self.user1)
        task = create_task("Do homework", "TODO", taskboard)
        self.assertEqual(task.time_estimate, 0)

    def test_task_default_status(self):
        """The default status of tasks is TO-DO."""
        taskboard = create_taskboard(self.user1)
        task = Task.objects.create(title="Do homework", taskboard=taskboard)
        self.assertEqual(task.status, "TODO")
