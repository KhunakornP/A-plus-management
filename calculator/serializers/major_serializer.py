"""Module for Major serializer."""

from rest_framework import serializers
from calculator.models import Major


class MajorSerializer(serializers.ModelSerializer):
    """Serializer for the Major model."""

    class Meta:
        """Meta definition for Major."""

        model = Major
        fields = "__all__"
