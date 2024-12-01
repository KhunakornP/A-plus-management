"""Views for handling taskboard creation, deletion, update and render."""

from rest_framework.authtoken.admin import User
from rest_framework.response import Response
from manager.models import Taskboard
from django.views import generic
from rest_framework import viewsets, status
from manager.serializers import TaskboardSerializer
from django.shortcuts import redirect, reverse, render


class TaskboardViewSet(viewsets.ModelViewSet):
    """A viewset to handle create/update/delete operations for Taskboard."""

    serializer_class = TaskboardSerializer

    def get_queryset(self):
        """Return all Taskboards related to the user.

        If the current user is a parent, check if they are accessing a
        child's Taskboards, if not return all Taskboards of the current user.
        """
        # if the user is not a parent
        if not self.request.user.has_perm("manager.is_parent"):
            return Taskboard.objects.filter(user=self.request.user)
        query = self.request.GET.get("user_id", None)
        if query:
            return Taskboard.objects.filter(user__pk=query)
        return Taskboard.objects.filter(user=self.request.user)

    def create(self, request):
        """
        Create a new Task object.

        :param request: The HTTP request with event data.
        :return: Response with created event.
        """
        data = request.data
        serializer = TaskboardSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskboardIndexView(generic.TemplateView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"


class TaskboardView(generic.TemplateView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"


def get_user_taskboard(request, user_id: int):
    """
    Display the taskboard index of a given user.

    :param request: The HttpRequest
    :param user_id: The id of the user who owns the taskboards.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect(reverse("manager:dashboard"))
    context = {"viewed_user": user}
    return render(request, "manager/taskboard_index.html", context)


def get_taskboard_details(request, taskboard_id: int, user_id: int):
    """
    Display the details of a taskboard belonging to the given user.

    :param request: The HttpRequest
    :param user_id: The id of the user who owns the taskboards.
    :param taskboard_id: The id of the taskboard to view.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect(reverse("manager:dashboard"))
    context = {"user_id": user.id}
    return render(request, "manager/taskboard.html", context)
