"""Module for Score History serializer."""

from rest_framework import serializers
from calculator.models import ScoreHistory


class ScoreHistorySerializer(serializers.ModelSerializer):
    """Serializer for the ScoreHistory model."""

    class Meta:
        """Meta definition for ScoreHistory."""

        model = ScoreHistory
        fields = "__all__"
