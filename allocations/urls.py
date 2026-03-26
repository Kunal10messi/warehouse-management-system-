from django.urls import path
from .views import request_device, my_devices, return_assigned_device, extend_return_date

urlpatterns = [
    path('request/', request_device, name='request_device'),
    path('my-devices/', my_devices, name='my_devices'),
    path('return/<int:assignment_id>/', return_assigned_device, name='return_device'),
    path('extend/<int:assignment_id>/', extend_return_date, name='extend_date')
]