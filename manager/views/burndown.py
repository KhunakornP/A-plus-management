"""Module for views relating to burndown chart pages."""

from django.shortcuts import render
from django.http import JsonResponse
from manager.serializers import EstimateHistorySerialzer
from manager.models import EstimateHistory
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import Optional
from manager.models import Taskboard


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


def create_figure(estimate_histories):
    """Create figure from estimate_history data."""
    pass


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
        estimate_histories = get_estimate_history_data(taskboard_id)
        fig = create_figure(estimate_histories)
        context["burndown"] = fig
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


def estimate_histories_json(request, taskboard_id):
    """Return EstimateHistory as a json file."""
    estimate_histories = get_estimate_history_data(taskboard_id)
    eh_serializer = EstimateHistorySerialzer(estimate_histories, many=True)
    return JsonResponse(eh_serializer.data, safe=False)


class ChartIndexView(generic.ListView):
    """A view that displays all burn-down charts of a student."""

    template_name = "manager/chart_index.html"
    context_object_name = "taskboards"

    def get_queryset(self):
        """
        Get a list of all taskboards belonging to the user.

        Get all taskboards to generate a link to the burndown
        chart for each taskboard.
        """
        return Taskboard.objects.filter(user__id=self.kwargs["user_id"])

    def get_context_data(self, **kwargs):
        """Pass the current student's id as context data."""
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.kwargs["user_id"]
        return context
