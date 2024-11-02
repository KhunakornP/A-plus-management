"""API View for A-Level Exams."""

from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.serializers import ExamSerializer
from calculator.models import Exams


class ExamsViewSet(viewsets.ViewSet):
    """ViewSet for handling getting Exam information."""

    def list(self, request):
        """
        List all Exam objects, based on the query parameters.
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

