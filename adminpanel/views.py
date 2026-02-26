from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from datetime import date

from allocations.models import DeviceRequest, Assignment
from allocations.services import approve_request
from inventory.models import Device
from .forms import EmployeeCreateForm

User = get_user_model()

@login_required
def admin_dashboard(request):
    pending_requests = DeviceRequest.objects.filter(status='PENDING')
    total_devices = Device.objects.count()
    available_devices = Device.objects.filter(status='AVAILABLE').count()
    assigned_devices = Device.objects.filter(status='ASSIGNED').count()
    overdue_assignments = Assignment.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lt=date.today()
    )

    context = {
        'pending_requests': pending_requests,
        'total_devices': total_devices,
        'available_devices': available_devices,
        'assigned_devices': assigned_devices,
        'overdue_assignments': overdue_assignments
    }

    return render(request, 'adminpanel/dashboard.html', context)

@login_required
def approve_request_view(request, request_id):
    req = get_object_or_404(DeviceRequest, id=request_id, status='PENDING')
    approve_request(req)
    return redirect('/admin-panel/')

@login_required
def reject_request_view(request, request_id):
    req = get_object_or_404(DeviceRequest, id=request_id, status='PENDING')
    req.status = 'REJECTED'
    req.save()
    return redirect('/admin-panel/')

@login_required
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


@login_required
def add_device(request):
    if request.method == 'POST':
        Device.objects.create(
            serial_number=request.POST['serial_number'],
            device_type=request.POST['device_type'],
            brand=request.POST['brand'],
            model=request.POST['model'],
            configuration=request.POST['configuration'],
            location=request.POST['location'],
            status=request.POST['status'],
        )
        return redirect('/admin-panel/devices/')
    return render(request, 'adminpanel/add_device.html')

@login_required
def edit_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    if request.method == 'POST':
        device.serial_number = request.POST['serial_number']
        device.device_type = request.POST['device_type']
        device.brand = request.POST['brand']
        device.model = request.POST['model']
        device.configuration = request.POST['configuration']
        device.location = request.POST['location']
        device.status = request.POST['status']
        device.save()
        return redirect('/admin-panel/devices/')
    return render(request, 'adminpanel/edit_device.html', {'device': device})

@login_required
def delete_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device.delete()
    return redirect('/admin-panel/devices/')

@login_required
def user_list(request):
    users = User.objects.filter(role='EMPLOYEE')
    return render(request, 'adminpanel/users.html', {'users': users})


@login_required
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

@login_required
def add_employee(request):
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form = EmployeeCreateForm()
    return render(request, 'adminpanel/add_employee.html', {'form': form})

