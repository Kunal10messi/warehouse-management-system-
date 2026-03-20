from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Device
from .models import DeviceRequest
from datetime import date
from .models import Assignment
from .services import return_device



@login_required
def my_devices(request):
    active_assignments = Assignment.objects.filter(
        user=request.user,
        actual_return_date__isnull=True
    )

    history = Assignment.objects.filter(
        user=request.user,
        actual_return_date__isnull=False
    ).order_by('-actual_return_date')

    total_fine = sum(a.fine_amount or 0 for a in history)

    return render(request, 'allocations/my_devices.html', {
        'assignments': active_assignments,
        'history': history,
        'total_fine': total_fine
    })

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

    today = date.today()

    if request.method == 'POST':
        device_id = request.POST['device']
        from_date = date.fromisoformat(request.POST['from_date'])
        to_date = date.fromisoformat(request.POST['to_date'])

        # if from_date < today or to_date < today:
        #     device_types = Device.objects.values_list('device_type', flat=True).distinct()
        #     return render(request, 'allocations/request_device.html', {
        #         'devices': devices,
        #         'device_types': device_types,
        #         'selected_type': selected_type,
        #         'today': today,
        #         'error': 'Dates cannot be in the past.'
        #     })

        # if to_date < from_date:
        #     device_types = Device.objects.values_list('device_type', flat=True).distinct()
        #     return render(request, 'allocations/request_device.html', {
        #         'devices': devices,
        #         'device_types': device_types,
        #         'selected_type': selected_type,
        #         'today': today,
        #         'error': 'To date cannot be before from date.'
        #     })

        device = Device.objects.get(id=device_id)

        DeviceRequest.objects.create(
            user=request.user,
            device=device,
            from_date=from_date,
            to_date=to_date
        )

        return redirect('/')

    device_types = Device.objects.filter(status='AVAILABLE').values_list('device_type', flat=True).distinct()
    device_types = [t for t in device_types if t]  # remove empty strings
    selected_device_id = request.GET.get('device')

    return render(request, 'allocations/request_device.html', {
        'devices': devices,
        'device_types': device_types,
        'selected_type': selected_type,
        'selected_device_id': selected_device_id,
        'today': today,
    })