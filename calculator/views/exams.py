"""API Views for handling Exams."""

from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.serializers import ExamSerializer
from calculator.models import Exams


class ExamsViewSet(viewsets.ViewSet):
    """ViewSet for handling getting Exam information."""

    def list(self, request) -> Response:
        """List all Exam objects, based on the query parameters.

        :param request: GET Request.
        :return: Response with exams data.
        """
        queryset = Exams.objects.all()
        exam_type = request.query_params.get("exam_type")
        core = request.query_params.get("core")
        if core is not None and exam_type:
            queryset = Exams.objects.filter(core=core).filter(name__contains=exam_type)
        elif core is not None:
            queryset = Exams.objects.filter(core=core)
        elif exam_type:
            queryset = Exams.objects.filter(name__contains=exam_type)
        serializer = ExamSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None) -> Response:
        """Retrieve ONE exam object.

        :param request: GET Request
        :param pk: primary key of that exam object.
        :return: Response with ONE exam data or 404 if error
        """
        try:
            return Response(
                ExamSerializer(Exams.objects.get(id=pk)).data, status=status.HTTP_200_OK
            )
        except Exams.DoesNotExist:
            return Response("Exam Does Not Exists", status=status.HTTP_404_NOT_FOUND)
