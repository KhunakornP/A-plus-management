"""Test cases for the display_burndown_chart view."""

import matplotlib.pyplot as plt
from django.test import TestCase
from manager.models import Taskboard, Task
from manager.views import get_estimate_history_data, create_figure

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
    return Task.objects.create(title=title, taskboard=tb)


class BurndownChartTests(TestCase):
    """Test the figure creation of burndown chart."""

    def test_create_figure(self):
        """Test create_figure."""
        tb = create_taskboard("Taskboard 1")
        create_task('task1', tb)

        est_hist = get_estimate_history_data()
        fig = create_figure(est_hist)

        plt.show()