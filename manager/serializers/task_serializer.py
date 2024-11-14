"""Module for Task serializer."""

from rest_framework import serializers
from manager.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""

    type = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source="end_date")

    class Meta:
        """Meta definition for Task."""

        model = Task
        fields = "__all__"

    def get_type(self, obj):
        """Get the value of a custom field to indicate that this is a task."""
        return "task"
