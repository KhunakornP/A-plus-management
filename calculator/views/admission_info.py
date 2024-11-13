"""API Views for handling Exams."""

from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.models import StudentExamScore, CriteriaSet


class StudentExamScoreViewSet(viewsets.GenericViewSet):
    """A ViewSet for updating student's score."""

    def update(self, request, pk=None):
        """Update the score of the student."""
        user = self.request.user
