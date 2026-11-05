from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import User

# Valid roles for quick membership check
_VALID_ROLES = {c[0] for c in User.Role.choices}


def _is_valid_user(request):
    """Return True only if the user is authenticated with a known role."""
    return (
        request.user
        and request.user.is_authenticated
        and request.user.role in _VALID_ROLES
    )


class IsAdmin(BasePermission):
    """Only admin users."""

    def has_permission(self, request, view):
        return _is_valid_user(request) and request.user.role == User.Role.ADMIN


class IsAdminOrReceptionist(BasePermission):
    """Admin or receptionist users."""

    def has_permission(self, request, view):
        return _is_valid_user(request) and request.user.role in (
            User.Role.ADMIN,
            User.Role.RECEPTIONIST,
        )


class IsAdminOrReceptionistOrReadOnly(BasePermission):
    """Admin/receptionist: full access. Doctor: read-only. Others: denied."""

    def has_permission(self, request, view):
        if not _is_valid_user(request):
            return False
        if request.method in SAFE_METHODS:
            return True  # any valid role can read
        return request.user.role in (User.Role.ADMIN, User.Role.RECEPTIONIST)
