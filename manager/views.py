"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Event
from django.forms import ModelForm
from django.shortcuts import redirect
from django.contrib import messages


class TaskboardView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard.html"
    model = Taskboard


class CalendarView(generic.ListView):
    """A view that displays the calendar."""

    # to be implemented
    template_name = "manager/calendar.html"


class EventForm(ModelForm):
    """A class for creating an event object from the given POST request"""

    class Meta:
        """Metaclass for the form"""
        model = Event
        fields = ["title", "start_date", "end_date", "details"]

    def __init__(self, *args, **kwargs):
        """Modify the init method to specify which fields are optional"""
        super().__init__(*args, **kwargs)
        # Note while event does have defaults for dates please enter
        # the date that the user clicked on the calendar for the default.
        self.fields["details"].required = False


def create_event(request) -> redirect:
    """Create an event object from the POST request

    :param request: A django HttpRequest object.
    :return: A redirect to the Calendar page.
    """
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Event: {request.POST['title']} added!")
            return redirect("manager:calendar")
    # if method is not POST or form is not valid
    messages.error(request, f"Event data is invalid.")
    return redirect("manager:calendar")
