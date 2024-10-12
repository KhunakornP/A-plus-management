"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Event
from django.forms import ModelForm
from django.shortcuts import redirect, reverse
from django.contrib import messages


class TaskboardView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard.html"
    model = Taskboard


class CalendarView(generic.ListView):
    """A view that displays the calendar."""

    # to be implemented
    template_name = "manager/calendar.html"
    model = Event


class EventForm(ModelForm):
    """A class for creating an event object from the given POST request."""

    class Meta:
        """Metaclass for the form."""

        model = Event
        fields = ["title", "start_date", "end_date", "details"]

    def __init__(self, *args, **kwargs):
        """Modify the init method to specify which fields are optional."""
        super().__init__(*args, **kwargs)
        # Note while event does have defaults for dates please enter
        # the date that the user clicked on the calendar for the default.
        self.fields["details"].required = False


def create_event(request) -> redirect:
    """
    Create an event object from the POST request.

    :param request: A django HttpRequest object.
    :return: A redirect to the Calendar page.
    """
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Event: {request.POST['title']} added!")
            return redirect(reverse("manager:calendar"))
    # if method is not POST or form is not valid
    messages.error(request, "Event data is invalid.")
    return redirect(reverse("manager:calendar"))


def delete_event(request, event_id: int) -> redirect:
    """
    Delete the given event from the database.

    :param request: A django HttpRequest object.
    :param event_id: The Primary Key (id) of the event.
    :return: A redirect to the calendar page.
    """
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event does not exist")
        return redirect(reverse("manager:calendar"))
    event_title = event.title
    event.delete()
    messages.info(request, f"Event: {event_title}, has been deleted.")
    return redirect(reverse("manager:calendar"))


def update_event(request, event_id: int) -> redirect:
    """
    Update an event attributes with the given data.

    This function takes a POST request and updates the event with the given
    event_id. It updates all attributes specified in the POST request for the
    event object.

    :param request: A django HttpRequest object.
    :param event_id: The Primary Key (id) of the event.
    :return: A redirect to the calendar page.
    """
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event does not exist")
        return redirect(reverse("manager:calendar"))
    if request.method == "POST:":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.info(request, f"Event: {request.POST['title']} updated.")
            return redirect(reverse("manager:calendar"))
    # if the request was not POST or form is not valid
    messages.error(request, "Event data provided is invalid.")
    return redirect(reverse("manager:calendar"))

