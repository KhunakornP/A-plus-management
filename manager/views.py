"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Event
from django.forms import ModelForm


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
