"""Views for handling task creation, deletion and updates."""

from django.urls import reverse
from django.shortcuts import redirect
from manager.models import Task
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse


class TaskForm(ModelForm):
    """Create a task object from POST request.

    More info at https://docs.djangoproject.com/en/5.1/topics/forms/modelforms
    """

    class Meta:
        """The Meta class."""

        model = Task
        fields = ["title", "status", "end_date", "details", "taskboard"]

    def __init__(self, *args, **kwargs):
        """Mark optional fields as not required."""
        super().__init__(*args, **kwargs)
        self.fields["status"].required = False
        self.fields["end_date"].required = False
        self.fields["details"].required = False


def create_task(request, taskboard_id: int) -> HttpResponse:
    """Create a new task bounded to a specific taskboard from POST request.

    :param request: django request object
    :param taskboard_id: id of the taskboard we're going to bound the task to
    cannot be tested until the taskboard.html page is finished.
    """
    post_data = request.POST.copy()
    post_data["taskboard"] = taskboard_id
    form = TaskForm(post_data)
    if form.is_valid():
        form.save()
        messages.success(request, f'Successfully created task {request.POST["title"]}')
        return redirect(reverse("manager:taskboard", args=(taskboard_id,)))
    else:
        messages.error(request, "Invalid data.")
        return redirect(reverse("manager:taskboard_index"))


def delete_task(request, task_id: int) -> HttpResponse:
    """Delete a specific task from the database.

    :param request: Django's request object
    :param task_id: the ID of the task which is to be deleted
    :return: redirects to the Taskboard page that this task belongs
    """
    try:
        task = Task.objects.get(pk=task_id)
        tb_id = task.taskboard.id
        task.delete()
        return redirect(reverse("manager:taskboard", args=(tb_id,)))
    except (KeyError, Task.DoesNotExist):
        messages.error(request, "This task does not exist")
        return redirect(reverse("manager:taskboard_index"))


def update_task(request, task_id: int) -> HttpResponse:
    """Update task attributes from POST request.

    This method will OVERRIDE the task with everything that's put in the
    POST request if the post request contains all non-optional attributes of
    a task, namely the title and the taskboard. it will DO NOTHING if the either
    the title, or the taskboard, or both, are not specified.

    :param request: Django's request object
    :param task_id: the ID of the task that is to be updated
    :return: redirects to the Taskboard page that this task belongs
    """
    try:
        task = Task.objects.get(pk=task_id)
    except (KeyError, Task.DoesNotExist):
        messages.error(request, "This task does not exist")
        return redirect(reverse("manager:taskboard_index"))
    post_data = request.POST.copy()
    assert task.taskboard is not None
    post_data["taskboard"] = task.taskboard.id
    form = TaskForm(post_data, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "The task has been updated")
    else:
        messages.error(request, "Task does not exist")
    return redirect(reverse("manager:taskboard", args=(task_id,)))
