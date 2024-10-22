"""Views for handling task creation, deletion and updates."""

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect
from manager.models import Task
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from manager.serializers import TaskSerializer


class TaskForm(ModelForm):
    """Create a task object from POST request.

    More info at https://docs.djangoproject.com/en/5.1/topics/forms/modelforms
    """

    class Meta:
        """The Meta class."""

        model = Task
        fields = ["title", "status", "end_date", "details", "taskboard"]

    def __init__(self, *args, **kwargs):
        """Mark optional fields as not required."""
        super().__init__(*args, **kwargs)
        self.fields["status"].required = False
        self.fields["end_date"].required = False
        self.fields["details"].required = False


def create_task(request, taskboard_id: int) -> HttpResponse:
    """Create a new task bounded to a specific taskboard from POST request.

    :param request: django request object
    :param taskboard_id: id of the taskboard we're going to bound the task to
    cannot be tested until the taskboard.html page is finished.
    """
    post_data = request.POST.copy()
    post_data["taskboard"] = taskboard_id
    form = TaskForm(post_data)
    if form.is_valid():
        form.save()
        messages.success(request, f'Successfully created task {request.POST["title"]}')
        return redirect(reverse("manager:taskboard", args=(taskboard_id,)))
    else:
        messages.error(request, "Invalid data.")
        return redirect(reverse("manager:taskboard_index"))


def delete_task(request, task_id: int) -> HttpResponse:
    """Delete a specific task from the database.

    :param request: Django's request object
    :param task_id: the ID of the task which is to be deleted
    :return: redirects to the Taskboard page that this task belongs
    """
    try:
        task = Task.objects.get(pk=task_id)
        tb_id = task.taskboard.id
        task.delete()
        return redirect(reverse("manager:taskboard", args=(tb_id,)))
    except (KeyError, Task.DoesNotExist):
        messages.error(request, "This task does not exist")
        return redirect(reverse("manager:taskboard_index"))


def update_task(request, task_id: int) -> HttpResponse:
    """Update task attributes from POST request.

    This method will OVERRIDE the task with everything that's put in the
    POST request if the post request contains all non-optional attributes of
    a task, namely the title and the taskboard. it will DO NOTHING if the either
    the title, or the taskboard, or both, are not specified.

    :param request: Django's request object
    :param task_id: the ID of the task that is to be updated
    :return: redirects to the Taskboard page that this task belongs
    """
    try:
        task = Task.objects.get(pk=task_id)
    except (KeyError, Task.DoesNotExist):
        messages.error(request, "This task does not exist")
        return redirect(reverse("manager:taskboard_index"))
    post_data = request.POST.copy()
    assert task.taskboard is not None
    post_data["taskboard"] = task.taskboard.id
    form = TaskForm(post_data, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "The task has been updated")
    else:
        messages.error(request, "Task does not exist")
    return redirect(reverse("manager:taskboard", args=(task_id,)))


class TaskViewSet(viewsets.ViewSet):
    """ViewSet fot handling Task-related operations."""

    def list(self, request):
        """
        List all Task objects.

        :param request: The HTTP request.
        :return: Response with tasks.
        """
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new Event object.

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
        Retrieve an Event object data bt ID.

        :param request: The HTTP request.
        """
        try:
            event = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """
        Update an existing Event object by ID.

        :param request: The HTTP request with updated data.
        :param pk: Primary key of the Event to update.
        :return: Response with updated event.
        """
        try:
            event = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(event, data=request.data, partial=True)
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
            event = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
