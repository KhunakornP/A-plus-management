"""Module for EstimateHistory serializer."""

from rest_framework import serializers
from manager.models import EstimateHistory


class EstimateHistorySerializer(serializers.ModelSerializer):
    """Serializer for EstimateHistory Model."""

    class Meta:
        """Meta definition for EstimateHistory."""

        model = EstimateHistory
        fields = ["id", "taskboard", "date", "time_remaining"]
