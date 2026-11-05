from rest_framework.routers import DefaultRouter

from .views import PatientViewSet

# /api/patients/ and /api/patients/<pk>/
router = DefaultRouter()
router.register("patients", PatientViewSet)

urlpatterns = router.urls
