"""Views for handling task creation, deletion and updates."""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from manager.models import Task, StudentInfo, Taskboard
from rest_framework import status, viewsets
from rest_framework.response import Response
from manager.serializers import TaskSerializer


def is_user_authorized(requesting_user: User, user_id:int) -> bool:
    """Check if the current user has access to another user's content."""
    if not requesting_user.has_perm("manager.is_parent"):
        return False
    info = StudentInfo.objects.get(user=user_id)
    return info.parent.filter(email=requesting_user.email).exists()


class TaskViewSet(viewsets.ViewSet):
    """ViewSet fot handling Task-related operations."""

    def list(self, request):
        """
        List Tasks based on query parameters.

        There are 3 query parameters: taskboard, user, and exclude.
        :taskboard: used to get all Tasks related to a specific Taskboard.
        :exclude:   used to filter out one specific Tasks status
                    and Tasks that belonged to other user.
        :user:      used to get all tasks belonging to the given user.
        If none of the query parameters are given, it will list all Tasks.

        :param request: The HTTP request.
        :return: Response with tasks.
        """
        taskboard_id = request.query_params.get("taskboard")
        ignore_status = request.query_params.get("exclude")
        user = request.query_params.get("user")
        # get all non-finished tasks from the taskboard.
        if ignore_status and taskboard_id:
            queryset = Task.objects.filter(
                ~Q(status=ignore_status), taskboard=taskboard_id
            )
        # get tasks in a taskboard.
        elif taskboard_id:
            # see if the taskboard exists
            try:
                owner = Taskboard.objects.get(pk=taskboard_id).user.id
            except Taskboard.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if request.user.id != owner and not is_user_authorized(request.user, owner):
                return Response(status=status.HTTP_404_NOT_FOUND)
            queryset = Task.objects.filter(taskboard=taskboard_id)
        # get non-finished tasks for the calendar.
        elif ignore_status:
            queryset = Task.objects.filter(
                ~Q(status=ignore_status), taskboard__user=request.user
            )
        # get all tasks of the given user, if self should have access
        elif user:
            if not is_user_authorized(request.user, user):
                return Response(status=status.HTTP_404_NOT_FOUND)
            queryset = Task.objects.filter(taskboard__user=user)
        # get all tasks belonging to the current user
        else:
            queryset = Task.objects.filter(taskboard__user=request.user)
        queryset = queryset.order_by("end_date")
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
