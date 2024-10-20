"""Views for handling event creation/deletion and update."""

import json
from django.urls import reverse
from django.shortcuts import redirect
from manager.models import Event
from django.contrib import messages
from django.forms import ModelForm


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
    if request.method == "POST":
        data = json.loads(request.body)
        form = EventForm(data, instance=event)
        if form.is_valid():
            form.save()
            messages.info(request, f"Event: {data['title']} updated.")
            return redirect(reverse("manager:calendar"))
    messages.error(request, "Event data provided is invalid.")
    return redirect(reverse("manager:calendar"))
