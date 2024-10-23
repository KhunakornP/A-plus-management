"""Views for handling taskboard creation, deletion, update and render."""

from manager.models import Taskboard
from django.views import generic

from rest_framework import viewsets
from manager.serializers import TaskboardSerializer


class TaskboardViewSet(viewsets.ModelViewSet):
    """A viewset to handle create/update/delete operations for Taskboard."""

    queryset = Taskboard.objects.all()
    serializer_class = TaskboardSerializer


class TaskboardIndexView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"
    context_object_name = "taskboard_list"
    model = Taskboard


class TaskboardView(generic.DetailView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"
    model = Taskboard
