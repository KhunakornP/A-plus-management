"""Top-level functions used in more than 1 test file."""
from manager.models import Task, Taskboard, EstimateHistory
from django.contrib.auth.models import User
from django.test import TestCase


class BaseTestCase(TestCase):
    """The base test suite for testcases."""

    def setUp(self):
        """Create and login user for tests."""
        super().setUp()
        self.username = "Tester"
        self.password = "Bestbytest!123"
        self.user1 = User.objects.create_user(
            username=self.username, email="testuser@nowhere.com"
        )
        self.user1.set_password(self.password)
        self.user1.save()
        self.client.login(username=self.username, password=self.password)
        # for the people who want to rework their tests to be faster
        # extend this clss


def create_taskboard(user: User, name: str = "Today") -> Taskboard:
    """
    Create a taskboard with the given name and user.

    :returns: A Taskboard object with the given name.
    """
    return Taskboard.objects.create(name=name, user=user)


def create_task(title: str, status: str, taskboard: Taskboard, end_date=None) -> Task:
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


def create_estimate_hisotry(tb: Taskboard, date, time_remaining: int):
    """Create a new Task bounded to a specific taskboard.

    :param title: Task's title
    :param tb: the Taskboard that this task would be bounded to
    :return: a Task object
    """
    return EstimateHistory.objects.create(
        taskboard=tb, date=date, time_remaining=time_remaining
    )
