"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Task
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.forms import ModelForm
from django.urls import reverse


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
    """Create a task object from form post request.

    :param ModelForm: Inherits ModelForm, more info at
    https://docs.djangoproject.com/en/5.1/topics/forms/modelforms
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


def create_task(request, taskboard_id):
    """Create a new task bounded to a specific taskboard.

    :param request: django request object
    :param taskboard_id: id of the taskboard we're going to bounded to
    """
    try:
        taskboard = get_object_or_404(Taskboard, pk=taskboard_id)
    except (KeyError, Taskboard.DoesNotExist):
        messages.error(request, "Cannot find taskboard")
        redirect(reverse("manager:taskboard_index"))
    request.POST["taskboard"] = taskboard
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(f'Successfully created task {request.POST["title"]}')
        return redirect(reverse("manager:taskboard_index"))
    else:
        messages.errir("Invalid data")
        return redirect(reverse("manager:taskboard_index"))
