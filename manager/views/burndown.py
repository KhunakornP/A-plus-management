"""Module for views relating to burndown chart pages."""

from django.shortcuts import render
from manager.serializers import EstimateHistorySerializer
from manager.models import EstimateHistory
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import Optional
from manager.models import Taskboard
from rest_framework.response import Response
from rest_framework import status, generics


def get_taskboard(taskboard_id: int) -> Optional[Taskboard]:
    """Return a Taskboard which has a specific taskboard id.

    :param taskboard_id: the ID of the taskboard
    :return: a Taskboard object, return None if it does not exists
    """
    try:
        return get_object_or_404(Taskboard, pk=taskboard_id)
    except Http404:
        return None


def get_estimate_history_data(taskboard_id):
    """Get EstimateHistory data."""
    taskboard = get_taskboard(taskboard_id)
    return EstimateHistory.objects.filter(taskboard=taskboard).order_by("date")


class BurndownView(generic.View):
    """A view for the burndown chart page."""

    template_name = "manager/burndown.html"

    def get_context_data(self, **kwargs):
        """Get context data for burndown chart view."""
        context = {}
        taskboard_id = self.kwargs.get("taskboard_id")
        context["taskboard_id"] = taskboard_id
        return context

    def get(self, request, *args, **kwargs):
        """Render burndown chart page when there's a GET request."""
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     """Render burndown chart page when there's a POST request."""
    #     kwargs["events"] = request.POST.getlist("events")
    #     context = self.get_context_data(**kwargs)
    #     return render(request, self.template_name, context)

class EstimateHistoryData(generics.ListAPIView):
    """A view getting EstimateHistory data."""
    
    serializer_class = EstimateHistorySerializer

    def get_queryset(self):
        """Return the all EstimateHistory objects sorted by date."""
        taskboard_id = self.kwargs['taskboard_id']
        return EstimateHistory.objects.filter(
            taskboard_id=taskboard_id).order_by('date')
    
    def list(self, request, *args, **kwargs):
        """Return serialized EstimateHistory data."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)