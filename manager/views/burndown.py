"""Module for views relating to burndown chart pages."""

from manager.serializers import EstimateHistorySerializer
from manager.models import EstimateHistory
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import Optional
from manager.models import Taskboard
from rest_framework import status, viewsets
from rest_framework.response import Response


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


class BurndownView(generic.TemplateView):
    """A view for the burndown chart page."""

    template_name = "manager/burndown.html"


class EstimateHistoryViewset(viewsets.ModelViewSet):
    """A viewset for EstimateHistory."""

    serializer_class = EstimateHistorySerializer

    def get_queryset(self):
        """Return EstimateHistory objects based on taskboard id."""
        taskboard_id = self.request.query_params.get("taskboard")
        return EstimateHistory.objects.filter(taskboard=taskboard_id).order_by("date")
    
    def list(self, request):
        """
        List EstimateHistory objects of a certain taskboard.

        :param request: The HTTP request.
        :return: Response with tasks.
        """
        queryset = self.get_queryset()
        serializer = EstimateHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
