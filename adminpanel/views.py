from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from datetime import date
from allocations.models import DeviceRequest, Assignment
from allocations.services import approve_request, reject_request
from inventory.services import delete_device as delete_device_service
from inventory.services import update_device as update_device_service
from inventory.services import create_device as create_device_service
from inventory.models import Device
from .forms import EmployeeCreateForm
from .forms import DeviceForm
from .decorators import admin_required
from django.contrib import messages
from accounts.services import create_employee
from django.core.exceptions import ValidationError

User = get_user_model()

@admin_required
def admin_dashboard(request):
    pending_requests = DeviceRequest.objects.filter(status='PENDING')
    
    total_devices = Device.objects.count()
    available_devices = Device.objects.filter(status='AVAILABLE').count()
    assigned_devices = Device.objects.filter(status='ASSIGNED').count()
    total_employees = User.objects.filter(role='EMPLOYEE').count()
    
    overdue_assignments = Assignment.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lt=date.today()
    )
    
    active_assignments = Assignment.objects.filter(
        actual_return_date__isnull=True
    ).select_related("device", "user").order_by("expected_return_date")

    context = {
        'pending_requests': pending_requests,
        'total_devices': total_devices,
        'available_devices': available_devices,
        'assigned_devices': assigned_devices,
        'overdue_assignments': overdue_assignments,
        'active_assignments': active_assignments,
        'total_employees': total_employees,
        "today": date.today()
    }

    return render(request, 'adminpanel/dashboard.html', context)

@admin_required
def approve_request_view(request, request_id):

    req = get_object_or_404(DeviceRequest, id=request_id, status='PENDING')

    try:
        approve_request(req)
        messages.success(request, "Device request approved.")

    except ValueError as e:
        messages.error(request, str(e))

    return redirect('/admin-panel/')

@admin_required
def reject_request_view(request, request_id):
    req = get_object_or_404(DeviceRequest, id=request_id, status='PENDING')
    try:
        reject_request(req)
        messages.success(request, "Request rejected.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('/admin-panel/')

@admin_required
def manage_devices(request):
    devices = Device.objects.all()

    device_type = request.GET.get('type')
    status = request.GET.get('status')
    search = request.GET.get('search')

    if device_type:
        devices = devices.filter(device_type=device_type)

    if status:
        devices = devices.filter(status=status)

    if search:
        devices = devices.filter(serial_number__icontains=search)

    device_types = Device.objects.values_list('device_type', flat=True).distinct()
    statuses = Device.objects.values_list('status', flat=True).distinct()

    return render(request, 'adminpanel/manage_devices.html', {
        'devices': devices,
        'device_types': device_types,
        'statuses': statuses,
        'selected_type': device_type,
        'selected_status': status,
        'search': search
    })


@admin_required
def add_device(request):
    if request.method == "POST":
        form = DeviceForm(request.POST)

        if form.is_valid():
            try:
                create_employee(form.clened_data)
                messages.success(request, "Employee created successfully")
                return redirect('admin_users')

            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = DeviceForm()

    return render(request, "adminpanel/add_device.html", {"form": form})


@admin_required
def edit_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        data = {
            'serial_number': request.POST.get('serial_number'),
            'device_type': request.POST.get('device_type'),
            'brand': request.POST.get('brand'),
            'model': request.POST.get('model'),
            'configuration': request.POST.get('configuration'),
            'location': request.POST.get('location'),
            'status': request.POST.get('status'),
        }

        update_device_service(device, data)

        return redirect('/admin-panel/devices/')

    return render(request, 'adminpanel/edit_device.html', {'device': device})

@admin_required
def delete_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    try:
        delete_device_service(device)
        messages.success(request, "Device deleted successfully")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('/admin-panel/devices/')

@admin_required
def user_list(request):
    users = User.objects.filter(role='EMPLOYEE').order_by('username')
    return render(request, 'adminpanel/users.html', {'users': users})


@admin_required
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    assignments = Assignment.objects.filter(user=user)
    active_assignments = assignments.filter(actual_return_date__isnull=True)
    total_fine = sum(a.fine_amount for a in assignments if a.fine_amount)

    return render(request, 'adminpanel/user_detail.html', {
        'emp': user,
        'assignments': assignments,
        'active_assignments': active_assignments,
        'total_fine': total_fine
    })

@admin_required
def add_employee(request):
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form = EmployeeCreateForm()
    return render(request, 'adminpanel/add_employee.html', {'form': form})



@login_required
def pending_requests_count(request):
    from django.http import JsonResponse
    count = DeviceRequest.objects.filter(status='PENDING').count()
    return JsonResponse({'count': count})
