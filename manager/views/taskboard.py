"""Views for handling taskboard creation, deletion, update and render."""

from manager.models import Taskboard
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse, Http404
from django.views import generic
from typing import Union

from rest_framework import viewsets
from manager.serializers import TaskboardSerializer


class TaskboardViewSet(viewsets.ModelViewSet):
    """A viewset to handle create/update/delete operations for Taskboard."""

    queryset = Taskboard.objects.all()
    serializer_class = TaskboardSerializer


class TaskboardIndexView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"
    context_object_name = "taskboard_list"
    model = Taskboard


class TaskboardView(generic.DetailView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"
    model = Taskboard


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


def create_taskboard(request) -> HttpResponse:
    """Create a taskboard from POST request.

    :param request: django's request object
    :return: redirect to taskboard index page
    """
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
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        form = TaskboardForm(request.POST, instance=taskboard)
        if form.is_valid():
            messages.success(request, "Taskboard updated")
            form.save()
        else:
            messages.error(request, "Cannot update taskboard")
    return redirect(reverse("manager:taskboard_index"))
