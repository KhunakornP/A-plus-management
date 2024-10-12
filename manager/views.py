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

def generate_calendar(start_day, n_days):
    """Return a nested list of days representing a calendar."""
    days = [''] * start_day + list(range(1, n_days + 1))
    rows = [days[i:i + 7] for i in range(0, len(days), 7)]
    
    # Ensure the last row has exactly 7 elements
    if len(rows[-1]) < 7:
        rows[-1].extend([''] * (7 - len(rows[-1])))
    
    return rows

def calendar_view(request):
    """Display calendar."""
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('date')

    if year is None or month is None:
        year = date.today().year
        month = date.today().month
        day = date.today().day
    else:
        year = int(year)
        month = int(month)
        day = date

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
        
    start_day, n_days = calendar.monthrange(year, month)

    tasks = Task.objects.filter(end_date__year=year,
                                end_date__month=month)
    task_data = [{'title': task.title, 'end_date': task.end_date} for task in tasks]

    return render(request, 'manager/calendar.html', {
        'current_day': day,
        'current_month': month,
        'current_year': year,
        'rows': generate_calendar(start_day+1, n_days),
        'tasks': task_data,
    })

if __name__ == 'main':
    print(generate_calendar(2, 31))