from django.urls import path
from .views import (
    admin_dashboard, approve_request_view, reject_request_view,
    manage_devices, add_device, edit_device, delete_device,
    user_list, user_detail, add_employee   
)

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('approve/<int:request_id>/', approve_request_view),
    path('reject/<int:request_id>/', reject_request_view),

    path('devices/', manage_devices, name='admin_devices'),
    path('devices/add/', add_device, name='admin_add_device'),
    path('devices/edit/<int:device_id>/', edit_device, name='admin_edit_device'),
    path('devices/delete/<int:device_id>/', delete_device, name='admin_delete_device'),

    path('users/', user_list, name='admin_users'),
    path('users/<int:user_id>/', user_detail, name='admin_user_detail'),

    path('users/add/', add_employee, name='admin_add_employee'),  
]
