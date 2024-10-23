"""Module for Event serializer."""

from rest_framework import serializers
from manager.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""

    class Meta:
        """Meta definition for Event."""

        model = Event
        fields = "__all__"
