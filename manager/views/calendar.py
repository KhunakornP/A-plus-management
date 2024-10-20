"""A class-based view for the calendar page."""

from django.views import generic
from typing import Any
from django.urls import reverse
from manager.models import Event, Task


class CalendarView(generic.TemplateView):
    """A view that display the calendar that show events and tasks."""

    template_name = "manager/calendar.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Create context dictionary used to render the template.

        :return: A dictionary containing a list of dicts about events
                 information to be converted into array.
        """
        all_events = Event.objects.all()
        all_tasks = Task.objects.all()
        events_list = []
        tasks_list = []
        for event in all_events:
            event_info = {
                "type": "event",
                "title": event.title,
                "start": event.start_date.isoformat(),
                "end": event.end_date.isoformat(),
                "color": "#6767fe",
                "editable": True,
                "details": event.details,
                "update": reverse("manager:update_event", args=(event.id,)),
            }
            events_list.append(event_info)
        for task in all_tasks:
            tasks_info = {
                "type": "task",
                "title": task.title,
                "start": task.end_date.isoformat(),
                "color": "#FF00FF",
                "editable": False,
                "details": task.details,
            }
            tasks_list.append(tasks_info)
        context = {"events": events_list, "tasks": tasks_list}
        return context
