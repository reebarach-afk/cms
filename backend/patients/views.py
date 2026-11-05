from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsAdminOrReceptionistOrReadOnly

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(ModelViewSet):
    """CRUD API for patients."""

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrReceptionistOrReadOnly]
