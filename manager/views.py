"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Task
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.forms import ModelForm
from django.urls import reverse
from typing import Union


class TaskboardIndexView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"
    context_object_name = "taskboard_list"
    model = Taskboard


class TaskboardView(generic.DetailView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"
    model = Taskboard


class CalendarView(generic.ListView):
    """A view that displays the calendar."""

    # to be implemented
    template_name = "manager/calendar.html"


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


class TaskboardForm(ModelForm):
    """Create a Taskboard object from POST request."""

    class Meta:
        """The Meta class."""

        model = Taskboard
        fields = ["name"]


def get_taskboard(taskboard_id: int) -> Union[Taskboard, None]:
    """Return a Taskboard which has a specific taskboard id.

    :param taskboard_id: the ID of the taskboard
    :return: a Taskboard object, return None if it does not exists
    """
    try:
        return get_object_or_404(Taskboard, pk=taskboard_id)
    except Http404:
        return None


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
    # TODO test this method once the frontend is done
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


def create_taskboard(request) -> HttpResponse:
    """Create a taskboard from POST request.

    :param request: django's request object
    :return: redirect to taskboard index page
    """
    # TODO test this method once the frontend is done
    try:
        taskboard_name = request.POST["name"]
        new_taskboard = Taskboard.objects.create(name=taskboard_name)
        new_taskboard.save()
    except KeyError:
        messages.error(request, "Please enter taskboard name.")

    return redirect(reverse("manager:taskboard_index"))


def delete_taskboard(request, taskboard_id: int) -> HttpResponse:
    """Delete a specific taskboard from the database.

    :param request: Django's request object
    :param taskboard_id: the ID of the taskboard which is to be deleted
    :return: redirect to the taskboard index page
    """
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        messages.success(request, f"Deleted Taskboard {taskboard.name}")
        taskboard.delete()
    else:
        messages.error(request, "Taskboard does not exists.")
    return redirect(reverse("manager:taskboard_index"))


def update_taskboard(request, taskboard_id: int) -> HttpResponse:
    """Modify the taskboard form POST request.

    :param request: Django's request object
    :param taskboard_id: the ID of the taskboard which is to be deleted
    :return: redirect to the taskboard index page
    """
    # TODO test this method once the frontend is done
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        form = TaskboardForm(request.POST, instance=taskboard)
        if form.is_valid():
            messages.success(request, "Taskboard updated")
            form.save()
        else:
            messages.error(request, "Cannot update taskboard")
    return redirect(reverse("manager:taskboard_index"))
