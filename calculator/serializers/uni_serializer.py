"""Module for University serializer."""

from rest_framework import serializers
from calculator.models import University


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for the University model."""

    class Meta:
        """Meta definition for University."""

        model = University
        fields = "__all__"
