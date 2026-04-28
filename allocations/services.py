from datetime import date
from decimal import Decimal
from allocations.models import Assignment, DeviceRequest
import logging
logger = logging.getLogger(__name__)

FINE_PER_DAY = Decimal('50.00')

def create_request(user, device, from_date, to_date):
    # today = date.today()

    # if from_date < today or to_date < today:
    #     raise ValueError("Dates cannot be in the past")

    # if to_date < from_date:
    #     raise ValueError("To date cannot be before from date")

    if device.status != 'AVAILABLE':
        raise ValueError("Device is not available")

    device_request = DeviceRequest.objects.create(
        user=user,
        device=device,
        from_date=from_date,
        to_date=to_date,
        status='PENDING'
    )
    
    logger.info(f"Request created: {device_request.id} by user {user.id} for device {device.id}")
    return device_request

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
    logger.info(f"Request approved: {device_request.id}")
    
    # reject all other pending requests for this same device
    DeviceRequest.objects.filter(
        device=device,
        status='PENDING'
    ).exclude(id=device_request.id).update(status='REJECTED')

    return assignment

def reject_request(device_request):
    if device_request.status != 'PENDING':
        raise ValueError("Only pending requests can be rejected")
    device_request.status = 'REJECTED'
    device_request.save()
    logger.info(f"Request rejected: {device_request.id}")
    return device_request

from datetime import datetime, date

def extend_date(assignment, new_date):
    today = date.today()

    if not new_date:
        raise ValueError("expected_return_date is required")

    # 🔥 string → date conversion
    try:
        if isinstance(new_date, str):
            new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    if assignment.expected_return_date < today:
        raise ValueError("This device is overdue and cannot be extended.")

    if assignment.actual_return_date:
        raise ValueError("Cannot extend a returned assignment")

    if new_date <= assignment.expected_return_date:
        raise ValueError("New date must be after the current return date.")

    old_date = assignment.expected_return_date

    assignment.expected_return_date = new_date
    assignment.save()

    logger.info(f"Assignment extended: {assignment.id} from {old_date} to {new_date}")

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
    logger.info(f"Device returned: {device.id} by user {assignment.user.id}")

    return assignment