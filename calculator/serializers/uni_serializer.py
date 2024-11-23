"""Module for University, Faculty and Major serializers."""

from rest_framework import serializers
from calculator.models import University, Faculty, Major


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for the University model."""

    class Meta:
        """Meta definition for University."""

        model = University
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    """Serializer for the Faculty model."""

    class Meta:
        """Meta definition for Faculty."""

        model = Faculty
        fields = "__all__"


class MajorSerializer(serializers.ModelSerializer):
    """Serializer for the Major model."""

    class Meta:
        """Meta definition for Major."""

        model = Major
        fields = "__all__"
