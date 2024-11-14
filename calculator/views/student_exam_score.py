"""API Views to handle saving student's exam score.."""

import ast
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from calculator.models import StudentExamScore
from calculator.serializers import (
    ExamScoreSerializer,
    CriterionSerializer,
)


class StudentExamScoreViewSet(viewsets.GenericViewSet):
    """A ViewSet for updating student's score."""

    def list(self, request: HttpRequest) -> Response:
        """List all exam scores of a student."""
        queryset = StudentExamScore.objects.filter(student=request.user)
        serializer = ExamScoreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: HttpRequest) -> Response:
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def calculate_score(self, request: HttpRequest) -> HttpResponse:
        """Calculate the user's score based on the score weights.

        :param request: POST request
        :return: 404 if the format of the request is not valid. Otherwise, redirects
        the user to the score page and show the score.
        """
        serializer = CriterionSerializer(
            # change string of dict to dict: https://stackoverflow.com/q/988228
            data=[ast.literal_eval(i) for i in request.data.getlist("criteria")],
            many=True,
        )

        if not serializer.is_valid():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        result = 0
        for criterion in serializer.validated_data:
            try:
                student_exam = StudentExamScore.objects.get(
                    exam=criterion["exam"], student=self.request.user
                )
                if student_exam.score < criterion["min_score"]:
                    messages.error(
                        request,
                        f"FAILED MINIMUM REQUIREMENT: {criterion['exam'].name.upper()}",
                    )
                    return redirect(reverse("calculator:score"))
                result += student_exam.score * criterion["weight"] / 100
            except StudentExamScore.DoesNotExist:
                messages.error(
                    request,
                    f"SCORE FOR {criterion["exam"].name.upper()} DOES NOT EXIST",
                )
                return redirect(reverse("calculator:score"))

        messages.success(request, result)
        return redirect(reverse("calculator:score"))
