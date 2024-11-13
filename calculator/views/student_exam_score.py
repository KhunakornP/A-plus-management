"""API Views to handle saving student's exam score.."""

from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.models import StudentExamScore
from calculator.serializers import ExamScoreSerializer


class StudentExamScoreViewSet(viewsets.GenericViewSet):
    """A ViewSet for updating student's score."""

    def list(self, request):
        """List all exam scores of a student."""
        queryset = StudentExamScore.objects.filter(student=request.user)
        serializer = ExamScoreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create the score of the student, update if that already exists."""
        _status = status.HTTP_200_OK
        try:
            exam_score = StudentExamScore.objects.get(
                student=self.request.user, exam=request.data.get("exam")
            )
            serializer = ExamScoreSerializer(
                exam_score, data=request.data, partial=True
            )
        except StudentExamScore.DoesNotExist:
            serializer = ExamScoreSerializer(data=request.data)
            _status = status.HTTP_201_CREATED

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=_status)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
