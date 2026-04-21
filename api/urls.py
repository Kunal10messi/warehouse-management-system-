from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, AssignmentViewSet, DeviceRequestViewSet

router = DefaultRouter()

router.register('devices', DeviceViewSet, basename='device')
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('requests', DeviceRequestViewSet, basename='request')


urlpatterns = router.urls