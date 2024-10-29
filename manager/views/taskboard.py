"""Views for handling taskboard creation, deletion, update and render."""

from manager.models import Taskboard
from django.views import generic

from rest_framework import viewsets
from manager.serializers import TaskboardSerializer


class TaskboardViewSet(viewsets.ModelViewSet):
    """A viewset to handle create/update/delete operations for Taskboard."""

    serializer_class = TaskboardSerializer

    def get_queryset(self):
        """Return all Taskboards related to the user."""
        return Taskboard.objects.filter(user=self.request.user)


class TaskboardIndexView(generic.TemplateView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"


class TaskboardView(generic.TemplateView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"
