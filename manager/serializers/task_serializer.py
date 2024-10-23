"""Module for Task serializer."""

from rest_framework import serializers
from manager.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""

    class Meta:
        """Meta definition for Task."""

        model = Task
        fields = "__all__"
