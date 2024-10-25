"""Module for Event serializer."""

from rest_framework import serializers
from manager.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""

    type = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source="start_date")
    end = serializers.DateTimeField(source="end_date")

    class Meta:
        """Meta definition for Event."""

        model = Event
        fields = "__all__"

    def get_type(self, obj):
        """Get the value of a custom field to indicate that this is an event."""
        return "event"
