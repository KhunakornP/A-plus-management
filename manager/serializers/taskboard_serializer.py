"""A serializer for the taskboard model."""

from rest_framework import serializers
from manager.models import Taskboard


class TaskboardSerializer(serializers.ModelSerializer):
    """A serializer for the taskboard model."""

    class Meta:
        """A Meta class."""

        model = Taskboard
        fields = "__all__"
