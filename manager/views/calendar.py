"""A class-based view for the calendar page."""

from django.views import generic


class CalendarView(generic.TemplateView):
    """A view that display the calendar that show events and tasks."""

    template_name = "manager/calendar.html"
