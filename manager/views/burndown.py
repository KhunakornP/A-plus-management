"""Module for views relating to burndown chart pages."""

from manager.serializers import EstimateHistorySerializer
from manager.models import EstimateHistory
from django.views import generic
from rest_framework import status, viewsets
from rest_framework.response import Response


class VelocityViewSet(viewsets.ViewSet):
    """Viewset for getting velocity."""

    def list(self, request):
        """Get a velocity depending on the given query parameters."""
        mode = request.query_params.get("mode")
        start_id = request.query_params.get("start")
        end_id = request.query_params.get("end")
        velocity = self.compute_basic_velocity(start_id, end_id)
        if mode == "average":
            velocity = self.compute_average_velocity(start_id, end_id)
        return Response({"velocity": velocity}, status=status.HTTP_200_OK)

    def compute_basic_velocity(self, start_id: int, end_id: int) -> float:
        """
        Return the velocity from the given estimate history objects.

        This computation does not take work created between the start and
        end date into account which sacrifices precision for speed.

        :param start_id: The id of the first estimate history object.
        :param end_id: The id of the last estimate history object.
        :return: The averaged difference of velocity from the start to end date.
        """
        start_estimate = EstimateHistory.objects.get(pk=start_id)
        end_estimate = EstimateHistory.objects.get(pk=end_id)
        work_done = start_estimate.time_remaining - end_estimate.time_remaining
        # add 1 because start day is inclusive
        length = (end_estimate.date.day - start_estimate.date.day) + 1
        return work_done / length

    def compute_average_velocity(self, start_id: int, end_id: int) -> float:
        """
        Return the average velocity of the user based on work done.

        Calculates the amount of work done between the start and end dates and
        computes the average work done per given unit of time.
        :param start_id: The id of the first estimate history object.
        :param end_id: The id of the last estimate history object.
        :return: The average work done per unit of time.
        """
        start_estimate = EstimateHistory.objects.get(pk=start_id)
        end_estimate = EstimateHistory.objects.get(pk=end_id)
        # add 1 because start day is inclusive
        length = (end_estimate.date.day - start_estimate.date.day) + 1
        history = EstimateHistory.objects.filter(taskboard=start_estimate.taskboard)
        total_work = 0
        for day in range(1, len(history)):
            diff = history[day - 1].time_remaining - history[day].time_remaining
            if 0 < diff:
                total_work += diff
        return total_work / length


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
