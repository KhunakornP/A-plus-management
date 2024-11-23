"""Module for Exam serializer."""

from rest_framework import serializers
from calculator.models import Exams


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for the Exams model."""

    class Meta:
        """Meta definition for Exams."""

        model = Exams
        fields = "__all__"
