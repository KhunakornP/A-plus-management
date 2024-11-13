"""Views for handling event creation/deletion and update."""

from django.core.exceptions import ObjectDoesNotExist
from manager.models import Event
from rest_framework import status, viewsets
from rest_framework.response import Response
from manager.serializers import EventSerializer
from django.utils import timezone
from datetime import datetime


ONE_HUNDRED_YEARS = 36500
# default upper limit for task range
FETCH_UPPER_LIMIT = (
    timezone.now().replace(hour=0, minute=0, second=0)
    + timezone.timedelta(days=ONE_HUNDRED_YEARS)
).isoformat()
# default lower limit for task range
FETCH_LOWER_LIMIT = (
    timezone.now().replace(hour=0, minute=0, second=0)
    - timezone.timedelta(days=ONE_HUNDRED_YEARS)
).isoformat()


class EventViewSet(viewsets.ViewSet):
    """ViewSet fot handling Event-related operations."""

    def list(self, request):
        """
        List all Event objects.

        :param request: The HTTP request.
        :return: Response with events.
        """
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            queryset = self.get_events_in_range(request.user.id, start_date, end_date)
        else:
            queryset = Event.objects.filter(user=request.user)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_events_in_range(
        self,
        user_id: int,
        start_date: str = FETCH_LOWER_LIMIT,
        end_date: str = FETCH_UPPER_LIMIT,
    ):
        """
        Return a queryset of events that are between the start and end dates.

        This method returns events that start within the given date ranges.
        This method return events associated with the given user id.
        :param user_id: The id of the user who created the events.
        :param start_date: The start date in ISO format.
        :param end_date: The end date in ISO format.
        :return: A queryset with all events that have a start date within range.
        """
        # get the dates from the str
        start_day = timezone.make_aware(datetime.fromisoformat(start_date))
        end_day = timezone.make_aware(datetime.fromisoformat(end_date))
        queryset = Event.objects.filter(
            start_date__gte=start_day, start_date__lte=end_day, user__id=user_id
        )
        return queryset

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
