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
        start_estimate = EstimateHistory.objects.filter(date__lte=start_day).last()
        end_estimate = EstimateHistory.objects.filter(taskboard__id=taskboard_id).last()
        work_done = start_estimate.time_remaining - end_estimate.time_remaining
        # add 1 because start day is inclusive
        length = self.get_timeframe(start_day, unit)
        velocity = work_done / length
        if velocity == 0:
            return {"x": "", "velocity": velocity}
        fin_date = ceil(end_estimate.time_remaining / velocity)
        day = (timezone.now() + timezone.timedelta(days=fin_date)).strftime("%Y-%m-%d")
        return {"x": day, "velocity": velocity}

    def get_timeframe(self, start_day, interval):
        """
        Get the total duration of work for calculating the basic velocity
        based on the time interval.
        """
        if interval == "week":
            return (
                timezone.now().isocalendar().week - start_day.isocalendar().week
            ) + 1
        elif interval == "month":
            return (timezone.now().month - start_day.month) + 1
        return (timezone.now().day - start_day.day) + 1

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
        start_estimate = EstimateHistory.objects.filter(date__lte=start_day).last()
        # add 1 because start day is inclusive
        length = self.get_timeframe(start_day, unit)
        history = self.aggregate_history_data(start_day, taskboard_id, unit)
        total_work = 0
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
        fin_date = ceil(today.time_remaining / velocity)
        day = (timezone.now() + timezone.timedelta(days=fin_date)).strftime("%Y-%m-%d")
        return {"x": day, "velocity": velocity}

    def aggregate_history_data(self, start_day, taskboard_id, interval):
        """
        Group the data for each estimateHistory object based on the given
        interval.
        """
        taskboard_data = EstimateHistory.objects.filter(
            taskboard__id=taskboard_id, date__gte=start_day
        )
        if interval == "week":
            # get the latest history objects for each week
            latest_entries = (
                taskboard_data.annotate(weeks=TruncWeek("date"))
                .values("weeks")
                .annotate(most_recent=Max("date"))
                .values_list("most_recent", flat=True)
            )
            # filter the db again for objects that are in the above query
            data = EstimateHistory.objects.filter(date__in=latest_entries)
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
            data = EstimateHistory.objects.filter(date__in=latest_entries)
            return data.order_by("date")
        return taskboard_data


class BurndownView(generic.TemplateView):
    """A view for the burndown chart page."""

    template_name = "manager/burndown.html"

class PBurndownView(generic.TemplateView):
    """A view for the burndown chart page."""

    template_name = "manager/p_burndown.html"


class EstimateHistoryViewset(viewsets.ViewSet):
    """A viewset for EstimateHistory."""

    def list(self, request):
        """
        List all EstimateHistory objects.

        If a taskboard_id is given return all EstimateHistory objects within
        the taskboard. If not or the taskboard_id is invalid returns a
        400 bad request. Returns grouped data if the interval is given.
        :param request: The HTTP request.
        :return: HttpResponse with EstimateHistory data.
        """
        taskboard_id = self.request.query_params.get("taskboard")
        queryset = EstimateHistory.objects.filter(taskboard=taskboard_id).order_by(
            "date"
        )
        interval = request.query_params.get("interval", "day")
        if interval == "week":
            # get the latest history objects for each week
            latest_entries = (
                queryset.annotate(weeks=TruncWeek("date"))
                .values("weeks")
                .annotate(most_recent=Max("date"))
                .values_list("most_recent", flat=True)
            )
            # filter the db again for objects that are in the above query
            queryset = EstimateHistory.objects.filter(date__in=latest_entries)
        elif interval == "month":
            # get the latest history objects for each month
            latest_entries = (
                queryset.annotate(months=TruncMonth("date"))
                .values("months")
                .annotate(most_recent=Max("date"))
                .values_list("most_recent", flat=True)
            )
            # filter the db again for objects that are in the above query
            queryset = EstimateHistory.objects.filter(date__in=latest_entries)
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = EstimateHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# hate the fact that this does not comply with DRY.
# someone should probably refactor this.
