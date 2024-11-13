"""Views for handling task creation, deletion and updates."""

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from manager.models import Task
from rest_framework import status, viewsets
from rest_framework.response import Response
from manager.serializers import TaskSerializer
from django.utils import timezone


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


class TaskViewSet(viewsets.ViewSet):
    """ViewSet fot handling Task-related operations."""

    def list(self, request):
        """
        List all Task objects.

        :param request: The HTTP request.
        :return: Response with tasks.
        """
        queryset = Task.objects.all().order_by("end_date")
        taskboard_id = request.query_params.get("taskboard")
        ignore_status = request.query_params.get("exclude")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            queryset = self.get_tasks_in_range(start_date, end_date, taskboard_id)
        # get all non-finished tasks from the taskboard.
        elif ignore_status and taskboard_id:
            queryset = Task.objects.filter(
                ~Q(status=ignore_status), taskboard=taskboard_id
            )
        # get tasks in a taskboard.
        elif taskboard_id:
            queryset = Task.objects.filter(taskboard=taskboard_id)
        # get non-finished tasks for the calendar.
        elif ignore_status:
            queryset = Task.objects.filter(
                ~Q(status=ignore_status), taskboard__user=request.user
            )
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_tasks_in_range(
        self,
        start_date: str = FETCH_LOWER_LIMIT,
        end_date: str = FETCH_UPPER_LIMIT,
        taskboard_id: int = None,
    ):
        """
        Return a queryset of tasks that are between the start and end dates.

        :param start_date: The start date in ISO format.
        :param end_date: The end date in ISO format.
        :param taskboard_id: The id of the taskboard to get tasks from.
            If None gets the data from all available tasks instead.
        :return: A queryset with all tasks within range.
        """
        # get the dates from the str
        start_day = timezone.make_aware(datetime.fromisoformat(start_date))
        end_day = timezone.make_aware(datetime.fromisoformat(end_date))
        if taskboard_id:
            queryset = Task.objects.filter(
                end_date__gte=start_day,
                end_date__lte=end_day,
                taskboard__id=taskboard_id,
            )
            return queryset
        queryset = Task.objects.filter(end_date__gte=start_day, end_date__lte=end_day)
        return queryset

    def create(self, request):
        """
        Create a new Task object.

        :param request: The HTTP request with event data.
        :return: Response with created event.
        """
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        """
        Retrieve a Task object data bt ID.

        :param request: The HTTP request.
        """
        try:
            event = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """
        Update an existing Task object by ID.

        :param request: The HTTP request with updated data.
        :param pk: Primary key of the Task to update.
        :return: Response with updated event.
        """
        try:
            event = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """
        Delete a Task by ID.

        :param request: The HTTP request.
        :param pk: Primary key of the Task to delete
        :return: Response indicating deletion status.
        """
        try:
            event = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
