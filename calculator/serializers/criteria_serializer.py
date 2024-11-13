"""Serializers for CriteriaSet and Criterion models."""

from rest_framework import serializers
from calculator.models import CriteriaSet, Criterion


class CriterionSerializer(serializers.ModelSerializer):
    """Serializer for the Criterion model."""

    min_score = serializers.FloatField(required=False, default=0)

    class Meta:
        """Meta definition of Criterion."""

        model = Criterion
        fields = "__all__"


class CriteriaSetSerializer(serializers.ModelSerializer):
    """Serializer for the CriteriaSet model."""

    criteria = CriterionSerializer(many=True)

    class Meta:
        """Meta definition for CriteriaSet."""

        model = CriteriaSet
        fields = "__all__"
