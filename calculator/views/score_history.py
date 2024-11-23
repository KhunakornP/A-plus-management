"""API Views for handling Score History."""

from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.serializers import ScoreHistorySerializer
from calculator.models import ScoreHistory


class ScoreHistoryViewSet(viewsets.ModelViewSet):
    """ViewSet for handling getting Exam information."""

    queryset = ScoreHistory.objects.all()
    serializer_class = ScoreHistorySerializer

    def list(self, request) -> Response:
        """List all ScoreHistory objects based on query parameters.

        :param request: GET Request
        :return: Response with ScoreHistory data.
        """
        criteria_set = request.query_params.get("criteria_set")
        major = request.query_params.get("major")
        year = request.query_params.get("year")

        if not criteria_set and major is not None:
            if year is not None:
                queryset = ScoreHistory.objects.filter(major=major, year=year)
            else:
                queryset = ScoreHistory.objects.filter(major=major)
            return Response(
                self.serializer_class(queryset, many=True).data,
                status=status.HTTP_200_OK,
            )

        if criteria_set is not None:
            if year is not None:
                queryset = ScoreHistory.objects.filter(
                    criteria_set=criteria_set, year=year
                )
            else:
                queryset = ScoreHistory.objects.filter(criteria_set=criteria_set)
            return Response(
                self.serializer_class(queryset, many=True).data,
                status=status.HTTP_200_OK,
            )

        return super().list(request)
