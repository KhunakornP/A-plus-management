"""Test cases for the EstimateHistory model."""

from datetime import date
from freezegun import freeze_time
from manager.models import Task, EstimateHistory
from .templates_for_tests import create_taskboard, BaseTestCase


class EstimateHistoryTest(BaseTestCase):
    """Test Estimate History Class."""

    def test_adding_same_day_tasks(self):
        """Test adding multiple tasks within the same day."""
        tb = create_taskboard(self.user1, "test")
        Task.objects.create(title="something", taskboard=tb, time_estimate=3)
        Task.objects.create(title="something3", taskboard=tb, time_estimate=5)
        Task.objects.create(title="something2", taskboard=tb, time_estimate=7)
        self.assertEqual(EstimateHistory.objects.count(), 1)
        eh = EstimateHistory.objects.first()
        self.assertEqual(eh.time_remaining, 3 + 5 + 7)

    def test_changing_time_estimate(self):
        """Test changing time estimate of a task."""
        tb = create_taskboard(self.user1, "test")
        t = Task.objects.create(title="something2", taskboard=tb, time_estimate=7)
        t.time_estimate = 6
        t.save()
        eh = EstimateHistory.objects.first()
        self.assertEqual(eh.time_remaining, 6)

    def test_adding_different_day_tasks(self):
        """Test creating multiple Tasks with different date.

        There should be multiple EstimateHistory objects.
        """
        tb = create_taskboard(self.user1, "test")
        day1 = date(2010, 10, 10)
        day2 = date(2011, 11, 11)
        with freeze_time(day1):
            obj1 = Task.objects.create(title="title", taskboard=tb, time_estimate=3)
        with freeze_time(day2):
            obj2 = Task.objects.create(title="title2", taskboard=tb, time_estimate=5)

        self.assertEqual(EstimateHistory.objects.count(), 2)
        self.assertEqual(
            EstimateHistory.objects.get(date=day1).time_remaining, obj1.time_estimate
        )
        self.assertEqual(
            EstimateHistory.objects.get(date=day2).time_remaining,
            obj2.time_estimate + obj1.time_estimate,
        )

    def test_deleting_task_also_subtract_estimate_time(self):
        """If a task got deleted, the time estimate should go down as well."""
        tb = create_taskboard(self.user1, "test")
        t = Task.objects.create(title="something2", taskboard=tb, time_estimate=7)
        eh = EstimateHistory.objects.first()
        self.assertEqual(eh.time_remaining, 7)
        t.delete()
        eh.refresh_from_db()
        self.assertEqual(eh.time_remaining, 0)

    def test_changing_status(self):
        """Test changing between different task status.

        Changing task status to DONE should subtracts the task's time remaining
        from the time estimate. Changing it back to DONE should add it back up.
        """
        tb = create_taskboard(self.user1, "test")
        t = Task.objects.create(title="something1", taskboard=tb, time_estimate=7)
        t2 = Task.objects.create(title="something2", taskboard=tb, time_estimate=3)
        t.save()
        t2.save()
        eh = EstimateHistory.objects.first()
        self.assertEqual(eh.time_remaining, 7 + 3)
        for _ in range(2):
            t.status = "DONE"
            t.save()
            eh.refresh_from_db()
            self.assertEqual(eh.time_remaining, 0 + 3)
        t.status = "IN PROGRESS"
        t.save()
        eh.refresh_from_db()
        self.assertEqual(eh.time_remaining, 7 + 3)
        t.status = "TODO"
        t.save()
        eh.refresh_from_db()
        self.assertEqual(eh.time_remaining, 7 + 3)

    def test_creating_task_with_status_done(self):
        """Create a task where the status is set to DONE.

        It should not add the time estimate.
        """
        tb = create_taskboard(self.user1)
        t2 = Task.objects.create(
            title="something2", taskboard=tb, time_estimate=3, status="DONE"
        )
        t2.save()
        eh = EstimateHistory.objects.first()
        self.assertEqual(eh.time_remaining, 0)
