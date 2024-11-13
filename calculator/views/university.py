"""APIs for getting university data for major selection page."""

from calculator.models import University, Faculty, Major
from rest_framework import status, viewsets
from rest_framework.response import Response
from calculator.serializers import (
    UniversitySerializer,
    FacultySerializer,
    MajorSerializer,
)


class UniversityViewSet(viewsets.ModelViewSet):
    """API for university data."""

    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class FacultyViewSet(viewsets.ViewSet):
    """API for faculty data."""

    def list(self, request) -> Response:
        """List of faculty of a university.

        :param request: GET request.
        :return: All Faculties of a university, None if university id is not given.
        """
        uni_id = request.query_params.get("university")
        if uni_id:
            queryset = Faculty.objects.filter(university=uni_id)
            serializer = FacultySerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class MajorViewSet(viewsets.ViewSet):
    """API for major data."""

    def list(self, request) -> Response:
        """List of majors belonging to a faculty.

        :param request: GET request.
        :return: All majors of a faculty, None if faculty id is not given.
        """
        faculty_id = request.query_params.get("faculty")
        if faculty_id:
            queryset = Major.objects.filter(faculty=faculty_id)
            serializer = MajorSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
