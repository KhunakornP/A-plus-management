"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard


class TaskboardIndexView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"
    model = Taskboard

class TaskboardView(generic.DetailView):
    """A view that display a specific taskboard"""
    
    tempalte = "manager/taskboard.html"
    model = Taskboard

class CalendarView(generic.ListView):
    """A view that displays the calendar."""

    # to be implemented
    template_name = "manager/calendar.html"

def create_task(request):
    pass