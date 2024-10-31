"""An API View for A-Level Calculator page."""

from calculator.models import University, Faculty, Major
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from calculator.serializers import (
    UniversitySerializer,
    FacultySerializer,
    MajorSerializer,
)


class CalculatorAPIView(APIView):
    """List all University, Faculty and Majors."""

    def get(self, request, format=None) -> Response:
        """Get all University, Faculty and Major depending on query parameters.

        TODO test this thing out once the model is finalised.
        :param request: GET request.
        :param format: Inherits from APIView, defaults to None.
        :return: Response with either University, Faculty or Major.
        """
        uni_id = request.query_params.get("university")
        faculty_id = request.query_params.get("faculty")
        queryset = University.objects.all()
        if faculty_id and uni_id:
            queryset = Major.objects.filter(faculty=faculty_id)
            serializer = MajorSerializer(queryset, many=True)
        elif uni_id:
            queryset = Faculty.objects.filter(university=uni_id)
            serializer = FacultySerializer(queryset, many=True)
        else:
            serializer = UniversitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None) -> Response:
        """TODO Handle score calculation as well as returning admission statistics.

        :param request: POST request
        :param format: Inherits from APIView, defaults to None
        :return: Response with the calculated score data and admission statistics.
        """
        raise NotImplementedError("To be done when the criteria model is finalised.")
