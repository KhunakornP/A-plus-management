"""Views for handling event creation/deletion and update."""

import json
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect
from manager.models import Event
from django.contrib import messages
from django.forms import ModelForm
from rest_framework import status, viewsets
from rest_framework.response import Response
from manager.serializers import EventSerializer


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


class EventViewSet(viewsets.ViewSet):
    """ViewSet fot handling Event-related operations."""

    def list(self, request):
        """
        List all Event objects.

        :param request: The HTTP request.
        :return: Response with events.
        """
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new Event object.

        :param request: The HTTP request with event data.
        :return: Response with created event.
        """
        data = request.data
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        """
        Retrieve an Event object data bt ID.

        :param request: The HTTP request.
        """
        try:
            event = Event.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """
        Update an existing Event object by ID.

        :param request: The HTTP request with updated data.
        :param pk: Primary key of the Event to update.
        :return: Response with updated event.
        """
        try:
            event = Event.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """
        Delete an Event by ID.

        :param request: The HTTP request.
        :param pk: Primary key of the Event to delete
        :return: Response indicating deletion status.
        """
        try:
            event = Event.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
