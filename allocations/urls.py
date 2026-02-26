from django.urls import path
from .views import request_device
from django.urls import path
from .views import request_device, my_devices, return_assigned_device

urlpatterns = [
    path('request/', request_device, name='request_device'),
    path('request/', request_device, name='request_device'),
    path('my-devices/', my_devices, name='my_devices'),
    path('return/<int:assignment_id>/', return_assigned_device, name='return_device'),
]
