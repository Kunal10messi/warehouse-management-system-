from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, AssignmentViewSet

router = DefaultRouter()

router.register('devices', DeviceViewSet, basename='device')
router.register('assignments', AssignmentViewSet, basename='assignment')

urlpatterns = router.urls