"""Module for Faculty serializer."""

from rest_framework import serializers
from calculator.models import Faculty


class FacultySerializer(serializers.ModelSerializer):
    """Serializer for the Faculty model."""

    class Meta:
        """Meta definition for Faculty."""

        model = Faculty
        fields = "__all__"
