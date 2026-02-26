from django.urls import path
from .views import available_devices

urlpatterns = [
    path('available/', available_devices, name='available_devices'),
]
