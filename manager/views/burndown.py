"""Module for views relating to burndown chart pages."""

from manager.serializers import EstimateHistorySerializer
from manager.models import EstimateHistory
from django.views import generic
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
from typing import Any
from math import ceil


class VelocityViewSet(viewsets.ViewSet):
    """Viewset for getting velocity."""

    def list(self, request):
        """Get a velocity depending on the given query parameters."""
        mode = request.query_params.get("mode")
        start_date = request.query_params.get("start")
        taskboard_id = request.query_params.get("taskboard")
        interval = request.query_params.get("interval", "day")
        if mode == "average":
            data = self.compute_average_velocity(start_date, interval, taskboard_id)
        else:
            data = self.compute_basic_velocity(start_date, interval,
                                               taskboard_id)
        return Response(data, status=status.HTTP_200_OK)

    def compute_basic_velocity(self, start_date: str, unit: str, taskboard_id: int) -> dict[str, Any]:
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
        start_estimate = EstimateHistory.objects.filter(date__lte=start_day).last()
        end_estimate = EstimateHistory.objects.filter(taskboard__id=taskboard_id).last()
        work_done = start_estimate.time_remaining - end_estimate.time_remaining
        # add 1 because start day is inclusive
        length = (timezone.now().day - start_day.day) + 1
        velocity = work_done / length
        if velocity == 0:
            return {"x": "", "velocity": velocity}
        fin_date = ceil(end_estimate.time_remaining / velocity)
        day = (timezone.now() + timezone.timedelta(days=fin_date)).strftime("%Y-%m-%d")
        return {"x": day, "velocity": velocity}

    def get_basic_interval(self, interval):
        """"""

    def compute_average_velocity(self, start_date: str, unit: str, taskboard_id: int) -> dict[str, Any]:
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
        # add 1 because start day is inclusive
        length = (timezone.now().day - start_day.day) + 1
        history = EstimateHistory.objects.filter(taskboard__id=taskboard_id, date__gte=start_day)
        total_work = 0
        for day in range(1, len(history)):
            diff = history[day - 1].time_remaining - history[day].time_remaining
            if 0 < diff:
                total_work += diff
        velocity = total_work / length
        today = history.last()
        if velocity == 0:
            return {"x": "", "velocity": velocity}
        fin_date = ceil(today.time_remaining/velocity)
        day = (timezone.now() + timezone.timedelta(days=fin_date)).strftime("%Y-%m-%d")
        return {"x": day, "velocity": velocity}

    def get_average_interval(self, interval):
        """"""


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
