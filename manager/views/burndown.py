"""Module for views relating to burndown chart pages."""

from django.shortcuts import render
from django.http import JsonResponse
from manager.serializers import EstimateHistorySerialzer
from manager.models import EstimateHistory
from django.views import generic
from .taskboard import get_taskboard


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
