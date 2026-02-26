from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Device
from .models import DeviceRequest
from datetime import date
from .models import Assignment
from .services import return_device

@login_required
def request_device(request):
    devices = Device.objects.filter(status='AVAILABLE')

    if request.method == 'POST':
        device_id = request.POST['device']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        device = Device.objects.get(id=device_id)

        DeviceRequest.objects.create(
            user=request.user,
            device=device,
            from_date=from_date,
            to_date=to_date
        )

        return redirect('/')

    return render(request, 'allocations/request_device.html', {'devices': devices})


@login_required
def my_devices(request):
    assignments = Assignment.objects.filter(user=request.user, actual_return_date__isnull=True)
    return render(request, 'allocations/my_devices.html', {'assignments': assignments})


@login_required
def return_assigned_device(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id, user=request.user)
    return_device(assignment)
    return redirect('/allocations/my-devices/')


@login_required
def request_device(request):
    selected_type = request.GET.get('type')
    devices = Device.objects.filter(status='AVAILABLE')

    if selected_type:
        devices = devices.filter(device_type=selected_type)

    if request.method == 'POST':
        device_id = request.POST['device']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        device = Device.objects.get(id=device_id)

        DeviceRequest.objects.create(
            user=request.user,
            device=device,
            from_date=from_date,
            to_date=to_date
        )

        return redirect('/')

    device_types = Device.objects.values_list('device_type', flat=True).distinct()

    return render(request, 'allocations/request_device.html', {
        'devices': devices,
        'device_types': device_types,
        'selected_type': selected_type
    })
