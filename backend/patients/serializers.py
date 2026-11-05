from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer with SPEC validations for Patient."""

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["created_at"]
