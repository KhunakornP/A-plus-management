"""Serilizer."""

from rest_framework import serializers
from .models import EstimateHistory

class EstimateHistorySerialzer(serializers.ModelSerializer):
    """TODO: write docstring."""

    class Meta:
        """TODO: write docstring."""

        model = EstimateHistory
        fields = ['id', 'taskboard', 'date', 'time_remaining']