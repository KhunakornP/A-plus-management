"""Module for views relating to burndown chart pages."""

from django.shortcuts import render
from manager.serializers import EstimateHistorySerialzer
from manager.models import EstimateHistory
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import Optional
from manager.models import Taskboard
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, viewsets


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


class EstimateHistoryViewset(viewsets.ViewSet):
    """A view getting EstimateHistory data."""
    
    serializer_class = EstimateHistorySerialzer

    def get_queryset(self):
        taskboard_id = self.kwargs['taskboard_id']
        return EstimateHistory.objects.filter(taskboard_id=taskboard_id).order_by('date')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BurndownView(generic.View):
    """A view for the burndown chart page."""

    template_name = "manager/burndown.html"

    def get_context_data(self, **kwargs):
        """Get context data for burndown chart view."""
        context = {}
        taskboard_id = self.kwargs.get("taskboard_id")
        context["taskboard_id"] = taskboard_id
        if "events" in kwargs:
            context["events"] = kwargs["events"]
        return context

    def get(self, request, *args, **kwargs):
        """Render burndown chart page when there's a GET request."""
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Render burndown chart page when there's a POST request."""
        kwargs["events"] = request.POST.getlist("events")
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


# @api_view(['GET', 'POST'])
# def estimate_histories_json(request, taskboard_id):
#     """Return EstimateHistory as a json file."""
#     if request.method == 'GET':
#         estimate_histories = get_estimate_history_data(taskboard_id)
#         eh_serializer = EstimateHistorySerialzer(estimate_histories, many=True)
#         return Response(eh_serializer.data)
    
#     elif request.method == 'POST':
#         eh_serializer = EstimateHistorySerialzer(data=request.data)
#         if eh_serializer.is_valid():
#             eh_serializer.save()
#             return Response(eh_serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def estimate_histories_detail(request, taskboard_id, eh_id):
#     """Return or update data of, or delete a specific EstimateHistory as a json file."""
#     try:
#         eh = EstimateHistory.objects.get(pk=eh_id)
#     except EstimateHistory.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         eh_serializer = EstimateHistorySerialzer(eh)
#         return Response(eh_serializer.data)
#     elif request.method == 'PUT':
#         eh_serializer = EstimateHistorySerialzer(eh, data=request.data)
#         if eh_serializer.is_valid():
#             eh_serializer.save()
#             return Response(eh_serializer.data)
#         return Response(eh_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         eh.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
