"""API Views to handle saving student's exam score.."""

from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.models import StudentExamScore
from calculator.serializers import ExamScoreSerializer


class StudentExamScoreViewSet(viewsets.GenericViewSet):
    """A ViewSet for updating student's score."""

    def list(self, request):
        """List all exam scores of a student."""
        queryset = StudentExamScore.objects.filter(user=request.user)
        serializer = ExamScoreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create the score of the student, update if that already exists."""
        _status = status.HTTP_200_OK
        for data in request.data:
            try:
                exam_score = StudentExamScore.objects.get(
                    user=self.request.user, exam=data["exam"]
                )
                serializer = ExamScoreSerializer(exam_score, data=data, partial=True)
            except StudentExamScore.DoesNotExist:
                serializer = ExamScoreSerializer(data=data)
                _status = status.HTTP_201_CREATED

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=_status)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
