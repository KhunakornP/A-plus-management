"""Views for handling event creation/deletion and update."""

from django.core.exceptions import ObjectDoesNotExist
from manager.models import Event
from rest_framework import status, viewsets
from rest_framework.response import Response
from manager.serializers import EventSerializer


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
