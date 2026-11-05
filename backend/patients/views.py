from rest_framework.viewsets import ModelViewSet

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(ModelViewSet):
    """CRUD API for patients."""

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
