from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdmin
from .serializers import RegisterSerializer


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ — returns access + refresh tokens."""

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except (InvalidToken, TokenError):
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RegisterView(CreateAPIView):
    """POST /api/auth/register/ — admin-only user creation."""

    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]
