from django.shortcuts import render
from .models import Device
from django.contrib.auth.decorators import login_required

@login_required
def available_devices(request):
    devices = Device.objects.filter(status='AVAILABLE')
    return render(request, 'inventory/available_devices.html', {'devices': devices})
