"""Test cases for the display_burndown_chart view."""

import matplotlib.pyplot as plt
import matplotcheck.base as mpc
from datetime import date, timedelta
from manager.models import Taskboard, EstimateHistory
from manager.views import get_estimate_history_data, create_figure
from django.test import TestCase
from django.urls import reverse


def create_taskboard(tb_name: str) -> Taskboard:
    """Create a new taskboard.

    :param tb_name: taskboard name
    :return: a Taskboard object
    """
    return Taskboard.objects.create(name=tb_name)


def create_estimate_hisotry(tb: Taskboard, date: date, time_remaining: int):
    """Create a new Task bounded to a specific taskboard.

    :param title: Task's title
    :param tb: the Taskboard that this task would be bounded to
    :return: a Task object
    """
    return EstimateHistory.objects.create(
        taskboard=tb, date=date, time_remaining=time_remaining
    )


class BurndownChartTests(TestCase):
    """Test the figure creation of burndown chart."""

    def test_create_figure(self):
        """Test create_figure."""
        tb = create_taskboard("Taskboard 1")

        create_estimate_hisotry(
            tb, date=date.today() - timedelta(days=3), time_remaining=50
        )
        create_estimate_hisotry(
            tb, date=date.today() - timedelta(days=2), time_remaining=40
        )
        create_estimate_hisotry(
            tb, date=date.today() - timedelta(days=1), time_remaining=20
        )

        est_hist = get_estimate_history_data(tb.id)

        fig, ax = create_figure(est_hist)
        plt.show()

        # Create a Matplotcheck PlotTester object
        plot_tester_1 = mpc.PlotTester(ax)

        # Test that the histogram plot has 5 bins
        plot_tester_1.assert_num_bins(3)

        # Test that the histogram bin values (the height of each bin) is as expected
        expected_bin_values = [50, 40, 20]
        plot_tester_1.assert_bin_values(expected_bin_values)


class EstimateHistoryJsonTests(TestCase):
    """Test the json response for EstimateHistory objects."""

    def test_estimate_histories_json(self):
        """Test json response."""
        tb = create_taskboard("Taskboard 1")

        create_estimate_hisotry(
            tb, date=date.today() - timedelta(days=3), time_remaining=50
        )
        create_estimate_hisotry(
            tb, date=date.today() - timedelta(days=2), time_remaining=40
        )
        create_estimate_hisotry(
            tb, date=date.today() - timedelta(days=1), time_remaining=20
        )

        url = reverse(
            "taskboard/<int:taskboard_id>/burndown/response",
            kwargs={"taskboard_id": tb.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
