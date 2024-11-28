"""Module for Exam serializer."""

from rest_framework import serializers
from calculator.models import StudentExamScore


class ExamScoreSerializer(serializers.ModelSerializer):
    """Serializer for the Exams model."""

    class Meta:
        """Meta definition for Exams."""

        model = StudentExamScore
        fields = "__all__"
