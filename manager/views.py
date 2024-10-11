"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard
from django.shortcuts import render
from datetime import datetime


class TaskboardView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard.html"
    model = Taskboard


def calendar_view(request):
    """Display calendar."""
    today = datetime.today()
    return render(request, 'manager/calendar.html', {
        'current_month': today.month,
        'current_year': today.year,
    })
