from datetime import date
from decimal import Decimal

FINE_PER_DAY = Decimal('50.00')  # ₹50 per day late


def approve_request(device_request):
    from .models import Assignment  # import here to avoid circular import

    device = device_request.device
    user = device_request.user

    assignment = Assignment.objects.create(
        user=user,
        device=device,
        expected_return_date=device_request.to_date
    )

    device.status = 'ASSIGNED'
    device.save()

    device_request.status = 'APPROVED'
    device_request.save()

    return assignment


def return_device(assignment):
    today = date.today()

    # mark return date
    assignment.actual_return_date = today

    # calculate fine
    if today > assignment.expected_return_date:
        days_late = (today - assignment.expected_return_date).days
        assignment.fine_amount = days_late * FINE_PER_DAY

    assignment.save()

    # VERY IMPORTANT: reset device state
    device = assignment.device
    device.status = 'AVAILABLE'
    device.save()

    return assignment