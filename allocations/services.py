from datetime import date
from decimal import Decimal

FINE_PER_DAY = Decimal('50.00')


def approve_request(device_request):
    from .models import Assignment, DeviceRequest

    device = device_request.device
    user = device_request.user

    existing_assignment = Assignment.objects.filter(
        device=device,
        actual_return_date__isnull=True
    ).exists()

    if existing_assignment:
        device_request.status = 'REJECTED'
        device_request.save()
        raise ValueError("Device is already assigned to another user.")

    assignment = Assignment.objects.create(
        user=user,
        device=device,
        expected_return_date=device_request.to_date
    )

    device.status = 'ASSIGNED'
    device.save()

    device_request.status = 'APPROVED'
    device_request.save()

    # reject all other pending requests for this same device
    DeviceRequest.objects.filter(
        device=device,
        status='PENDING'
    ).exclude(id=device_request.id).update(status='REJECTED')

    return assignment


def return_device(assignment):
    today = date.today()

    assignment.actual_return_date = today

    if today > assignment.expected_return_date:
        days_late = (today - assignment.expected_return_date).days
        assignment.fine_amount = days_late * FINE_PER_DAY

    assignment.save()

    device = assignment.device
    device.status = 'AVAILABLE'
    device.save()

    return assignment