"""Views for handling taskboard creation, deletion, update and render."""

from rest_framework.authtoken.admin import User
from manager.models import Taskboard
from django.views import generic
from rest_framework import viewsets
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


class TaskboardIndexView(generic.TemplateView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"


class TaskboardView(generic.TemplateView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"

    def get_context_data(self, **kwargs):
        """Pass the id of the taskboard as context."""
        context = super().get_context_data(**kwargs)
        context["taskboard_id"] = self.kwargs["pk"]
        return context


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
    context = {"user_id": user.id, "taskboard_id": taskboard_id}
    return render(request, "manager/taskboard.html", context)
