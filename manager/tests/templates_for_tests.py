"""Top-level functions used in more than 1 test file."""

from manager.models import Task, Taskboard, EstimateHistory


def create_taskboard(name: str = "Today") -> Taskboard:
    """
    Create a taskboard with the given name.

    :returns: A Taskboard object with the given name.
    """
    return Taskboard.objects.create(name=name)


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
