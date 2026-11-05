from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with a role field."""

    class Role(models.TextChoices):
        ADMIN = "admin"
        RECEPTIONIST = "receptionist"
        DOCTOR = "doctor"

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.ADMIN,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
