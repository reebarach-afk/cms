from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin config for the custom User model with role field."""

    # Show role in the list view
    list_display = BaseUserAdmin.list_display + ("role",)
    list_filter = BaseUserAdmin.list_filter + ("role",)

    # Add role to the edit form (under Permissions section)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Clinic", {"fields": ("role",)}),
    )

    # Add role to the create form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Clinic", {"fields": ("role",)}),
    )
