"""Module for views relating to burndown chart pages."""

from manager.serializers import EstimateHistorySerializer
from manager.models import EstimateHistory
from django.views import generic
from manager.models import Taskboard
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
from typing import Any
from math import ceil
from django.db.models import Max
from django.db.models.functions import TruncMonth, TruncWeek


class VelocityViewSet(viewsets.ViewSet):
    """Viewset for getting velocity."""

    def list(self, request):
        """Get a velocity depending on the given query parameters."""
        mode = request.query_params.get("mode")
        start_date = request.query_params.get(
            "start", timezone.now().strftime("%Y-%m-%d")
        )
        taskboard_id = request.query_params.get("taskboard")
        interval = request.query_params.get("interval", "day")
        if mode == "average":
            data = self.compute_average_velocity(start_date, interval, taskboard_id)
        else:
            data = self.compute_basic_velocity(start_date, interval, taskboard_id)
        return Response(data, status=status.HTTP_200_OK)

    def compute_basic_velocity(
        self, start_date: str, unit: str, taskboard_id: int
    ) -> dict[str, Any]:
        """
        Return the velocity from the given estimate history objects.

        This computation does not take work created between the start and
        end date into account which sacrifices precision for speed.

        :param start_date: The ISO string of the starting date.
        :param unit: The unit or interval of time to find the velocity.
        :param taskboard_id: The id of the taskboard to calculate velocity for.
        :return: The averaged difference of velocity from the start to end date.
            and the finishing date.
        """
        start_day = timezone.make_aware(datetime.fromisoformat(start_date))
        start_estimate = (
            EstimateHistory.objects.filter(date__lte=start_day).order_by("date").last()
        )
        end_estimate = (
            EstimateHistory.objects.filter(taskboard__id=taskboard_id)
            .order_by("date")
            .last()
        )
        if not start_estimate or not end_estimate:
            return {"x": "", "velocity": 0}
        work_done = start_estimate.time_remaining - end_estimate.time_remaining
        length = self.get_timeframe(start_day, unit)
        if length == 0:
            return {"x": "", "velocity": 0}
        velocity = work_done / length
        if velocity == 0:
            return {"x": "", "velocity": velocity}
        units_needed = ceil(end_estimate.time_remaining / velocity)
        day = self.get_finishing_date(units_needed, unit)
        return {"x": day, "velocity": velocity}

    def get_timeframe(self, start_day: datetime, interval: str):
        """
        Get the total duration of work for based on the time interval.

        :param start_day: The first recorded date from the chart.
        :param interval: The interval between each data point.
        :return: The number of intervals between the start date and today.
        """
        if interval == "week":
            return (
                timezone.now().isocalendar().week - start_day.isocalendar().week
            ) + 1
        elif interval == "month":
            today = timezone.now()
            return (
                (today.year - start_day.year) * 12 + (today.month - start_day.month) + 1
            )
        return (timezone.now() - start_day).days

    def compute_average_velocity(
        self, start_date: str, unit: str, taskboard_id: int
    ) -> dict[str, Any]:
        """
        Return the average velocity of the user based on work done.

        Calculates the amount of work done between the starting date and today
        then computes the average work done per given unit of time.
        :param start_date: The ISO string of the start date.
        :param taskboard_id: The id of the taskboard to calculate velocity for.
        :param unit: The unit or interval of time to find the velocity.
        :return: The average work done per unit of time and finishing date.
        """
        start_day = timezone.make_aware(datetime.fromisoformat(start_date))
        start_estimate = (
            EstimateHistory.objects.filter(date__lte=start_day).order_by("date").last()
        )
        length = self.get_timeframe(start_day, unit)
        if length == 0:
            return {"x": "", "velocity": 0}
        history = self.aggregate_history_data(start_day, taskboard_id, unit)
        total_work = 0
        if not history or not start_estimate:
            return {"x": "", "velocity": 0}
        diff = start_estimate.time_remaining - history[0].time_remaining
        if diff > 0:
            total_work += diff
        for day in range(1, len(history)):
            diff = history[day - 1].time_remaining - history[day].time_remaining
            if 0 < diff:
                total_work += diff
        velocity = total_work / length
        today = history.last()
        if velocity == 0:
            return {"x": "", "velocity": velocity}
        units_needed = ceil(today.time_remaining / velocity)
        day = self.get_finishing_date(units_needed, unit)
        return {"x": day, "velocity": velocity}

    def get_finishing_date(self, units: int, interval: str) -> datetime:
        """
        Get the predicted finishing date for clearing all tasks.

        :param units: The number of intervals between today and the start date.
        :param interval: The interval of the data.
        :return: The predicted date where all tasks are finished.
        """
        today = timezone.now()
        if interval == "week":
            return (today + timezone.timedelta(days=units * 7)).strftime("%Y-%m-%d")
        elif interval == "month":
            finish_date = today.replace(
                month=max((today.month + units - 1) % 12 + 1, 1)
            )
            return finish_date.strftime("%Y-%m-%d")
        return (today + timezone.timedelta(days=units)).strftime("%Y-%m-%d")

    def aggregate_history_data(
        self, start_day: datetime, taskboard_id: int, interval: str
    ):
        """
        Group the data for each estimateHistory object based on the given interval.

        :param start_day: The first recorded date from the chart.
        :param taskboard_id: The taskboard which contains the EstimateHistory.
        :param interval: The interval to group data to.
        :return: A Query set containing aggregated EstimatedHistory objects.
        """
        taskboard_data = EstimateHistory.objects.filter(
            taskboard__id=taskboard_id, date__gte=start_day
        ).order_by("date")
        if interval == "week":
            # get the latest history objects for each week
            latest_entries = (
                taskboard_data.annotate(weeks=TruncWeek("date"))
                .values("weeks")
                .annotate(most_recent=Max("date"))
                .values_list("most_recent", flat=True)
            )
            # filter the db again for objects that are in the above query
            data = EstimateHistory.objects.filter(
                date__in=latest_entries, taskboard=taskboard_id
            )
            return data.order_by("date")
        elif interval == "month":
            # get the latest history objects for each month
            latest_entries = (
                taskboard_data.annotate(months=TruncMonth("date"))
                .values("months")
                .annotate(most_recent=Max("date"))
                .values_list("most_recent", flat=True)
            )
            # filter the db again for objects that are in the above query
            data = EstimateHistory.objects.filter(
                date__in=latest_entries, taskboard=taskboard_id
            )
            return data.order_by("date")
        return taskboard_data


class BurndownView(generic.TemplateView):
    """A view for the burndown chart page."""

    template_name = "manager/burndown.html"


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
