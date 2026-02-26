from django.contrib import admin
from .models import DeviceRequest, Assignment
from .services import approve_request, return_device

@admin.register(DeviceRequest)
class DeviceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'from_date', 'to_date', 'status')
    actions = ['approve_selected_requests']

    def approve_selected_requests(self, request, queryset):
        for req in queryset:
            if req.status == 'PENDING' and req.device.status == 'AVAILABLE':
                approve_request(req)
    approve_selected_requests.short_description = "Approve selected requests"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'expected_return_date', 'actual_return_date', 'fine_amount')
    actions = ['mark_as_returned']

    def mark_as_returned(self, request, queryset):
        for assignment in queryset:
            if assignment.actual_return_date is None:
                return_device(assignment)
    mark_as_returned.short_description = "Mark selected assignments as returned"
