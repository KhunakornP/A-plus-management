"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Task
from django.shortcuts import get_object_or_404, redirect
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

    tempalte = "manager/taskboard.html"
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
    except (KeyError, Taskboard.DoesNotExist):
        return None


def create_task(request, taskboard_id: int) -> redirect:
    """(UNTESTED) Create a new task bounded to a specific taskboard from POST request.

    :param request: django request object
    :param taskboard_id: id of the taskboard we're going to bound the task to
    cannot be tested until the taskboard.html page is finished.
    """
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        request.POST["taskboard"] = taskboard
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Successfully created task {request.POST["title"]}'
            )
        else:
            messages.error(request, "Invalid data.")
        # to be changed to the taskboard page that the task belongs to.
        return redirect(reverse("manager:taskboard_index"))
    messages.error(request, "Taskboard does not exists.")
    return redirect(reverse("manager:taskboard_index"))


def create_taskboard(request) -> redirect:
    """Create a taskboard from POST request.

    :param request: django's request object
    :return: redirect to taskboard index page
    """
    try:
        taskboard_name = request.POST["name"]
    except KeyError:
        messages.error("Please enter taskboard name.")
        return redirect(reverse("manager:taskboard_index"))

    new_taskboard = Taskboard.objects.create(name=taskboard_name)
    new_taskboard.save()
    return redirect(reverse("manager:taskboard_index"))


def delete_taskboard(request, taskboard_id: int) -> redirect:
    """Delete a specific taskboard from the database.

    :param request: Django's request object
    :param taskboard_id: the ID of the taskboard which is to be deleted
    :return: redirect to the taskboard index page
    """
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        messages.success(request, "Deleted Taskboard f{taskboard.name}")
        taskboard.delete()
    else:
        messages.error(request, "Taskboard does not exists.")
    return redirect(reverse("manager:taskboard_index"))


def modify_taskbaord(request, taskboard_id: int) -> redirect:
    """(UNTESTED) Modify the taskboard form POST request.

    :param request: _description_
    :param taskboard_id: the ID of the taskboard which is to be deleted
    :return: redirect to the taskboard index page
    """
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        form = TaskboardForm(request.POST, instance=taskboard)
        if form.is_valid():
            messages.success(request, "Taskboard updated")
            form.save()
        else:
            messages.error("Cannot update taskboard")
    return redirect(reverse("manager:taskboard_index"))
