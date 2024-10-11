"""Module for all view classes for pages in the manager app."""
import calendar
from django.views import generic
from .models import Taskboard, Task
from django.shortcuts import render
from datetime import date


class TaskboardView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard.html"
    model = Taskboard


def calendar_view(request, date=date.today()):
    """Display calendar."""
    current_year = date.year
    current_month = date.month
    start_day, n_days = calendar.monthrange(current_year, current_month)

    tasks = Task.objects.filter(end_date__year=current_year,
                                 end_date__month=current_month)
    task_data = [{'title': task.title, 'end_date': task.end_date} for task in tasks]

    return render(request, 'manager/calendar.html', {
        'current_month': current_month,
        'current_year': current_year,
        'start_day': start_day,
        'n_days': n_days,
        'tasks': task_data,
    })
