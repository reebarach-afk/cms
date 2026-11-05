import re

from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with SPEC validations."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def validate_email(self, value):
        """Email is required and must be unique."""
        if not value:
            raise serializers.ValidationError("Email is required.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        """At least 8 chars and not all digits."""
        if value.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric.")
        return value

    def validate_role(self, value):
        """Must be one of the three allowed roles."""
        valid = {c[0] for c in User.Role.choices}
        if value not in valid:
            raise serializers.ValidationError(
                f"Role must be one of: {', '.join(valid)}."
            )
        return value

    def create(self, validated_data):
        """Create user with hashed password."""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
