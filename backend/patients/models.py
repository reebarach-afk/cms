import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def validate_name(value):
    """Letters and spaces only, 2-100 chars."""
    if not re.fullmatch(r"[A-Za-z ]{2,100}", value):
        raise ValidationError("Name must be 2-100 characters, letters and spaces only.")


def validate_phone(value):
    """Exactly 10 digits."""
    if not re.fullmatch(r"\d{10}", value):
        raise ValidationError("Phone must be exactly 10 digits.")


class Patient(models.Model):
    """Patient record."""

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100, validators=[validate_name])
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=10, unique=True, validators=[validate_phone])
    address = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
