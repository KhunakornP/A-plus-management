"""API Views to handle saving student's exam score.."""

from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from calculator.models import StudentExamScore, Major
from calculator.serializers import (
    ExamScoreSerializer,
    CriterionSerializer,
)


class StudentExamScoreViewSet(viewsets.ViewSet):
    """A ViewSet for updating student's score."""

    def list(self, request: HttpRequest) -> Response:
        """List all exam scores of a student."""
        queryset = StudentExamScore.objects.filter(student=request.user)
        serializer = ExamScoreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrieve one StudentExamScore object."""
        try:
            serializer = ExamScoreSerializer(StudentExamScore.objects.get(id=pk))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentExamScore.DoesNotExist:
            return Response(
                {"error": "Exam Score not found"}, status=status.HTTP_404_NOT_FOUND
            )

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
        if "criteria" not in request.data:
            return Response(
                {"error": "No Criteria Data"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CriterionSerializer(
            data=request.data["criteria"],
            many=True,
        )
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid POST Data"}, status=status.HTTP_400_BAD_REQUEST
            )

        criteria_id = request.data["criteria_id"]
        major_code = ""
        if request.data["major_id"] != "":
            major_code = Major.objects.get(pk=int(request.data["major_id"])).code

        result = 0
        for criterion in serializer.validated_data:
            try:
                exam = criterion["exam"]
                student_score = StudentExamScore.objects.get(
                    exam=exam, student=self.request.user
                ).score
                result += (
                    student_score * (100 / exam.max_score) * criterion["weight"] / 100
                )
            except StudentExamScore.DoesNotExist:
                txt = f"SCORE FOR {criterion['exam'].name.upper()} DOES NOT EXIST"
                messages.warning(request, txt)

        request.session["has_score"] = True
        request.session["score"] = result
        request.session["criteria_id"] = criteria_id
        request.session["major"] = major_code
        return redirect(reverse("calculator:score"))
