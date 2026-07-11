from datetime import datetime, date
from decimal import Decimal
from allocations.models import Assignment, DeviceRequest
from inventory.models import Device
from django.db import transaction
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
        logger.warning(
            "Request denied | user=%s attempted unavailable device=%s",
            user.username,
            device.serial_number,
        )
        raise ValueError("Device is not available")

    device_request = DeviceRequest.objects.create(
        user=user,
        device=device,
        from_date=from_date,
        to_date=to_date,
        status='PENDING'
    )
    
    logger.info(
        "Request created | request_id=%s user=%s device=%s from=%s to=%s",
        device_request.id,
        user.username,
        device.serial_number,
        from_date,
        to_date,
    )
    return device_request

def approve_request(device_request):
    from .models import Assignment, DeviceRequest

    with transaction.atomic():

        device = device_request.device
        device = Device.objects.select_for_update().get(
            id=device_request.device_id
        )
        user = device_request.user

        existing_assignment = Assignment.objects.filter(
            device=device,
            actual_return_date__isnull=True
        ).exists()

        if existing_assignment:
            device_request.status = 'REJECTED'
            device_request.save()
            logger.warning(
                    "Approval failed | request_id=%s device=%s already assigned",
                    device_request.id,
                    device.serial_number,
                )
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
        logger.info(
            "Request approved | request_id=%s user=%s device=%s assignment_id=%s",
            device_request.id,
            user.username,
            device.serial_number,
            assignment.id,
        )
        
        # reject all other pending requests for this same device
        rejected_count = DeviceRequest.objects.filter(
            device=device,
            status='PENDING'
        ).exclude(id=device_request.id).update(status='REJECTED')

        if rejected_count:
            logger.info(
                "Auto-rejected %s competing request(s) for device=%s",
                rejected_count,
                device.serial_number,
            )

        return assignment

def reject_request(device_request):
    if device_request.status != 'PENDING':
        raise ValueError("Only pending requests can be rejected")
    device_request.status = 'REJECTED'
    device_request.save()
    logger.info(
        "Request rejected | request_id=%s user=%s device=%s",
        device_request.id,
        device_request.user.username,
        device_request.device.serial_number,
    )
    return device_request

def extend_date(assignment, new_date):
    today = date.today()

    if not new_date:
        logger.warning(
            "Extension failed | assignment_id=%s reason=missing_return_date",
            assignment.id,
        )
        raise ValueError("expected_return_date is required")

    # string → date conversion
    try:
        if isinstance(new_date, str):
            new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
    except Exception:
        logger.warning(
            "Extension failed | assignment_id=%s invalid_date_format=%s",
            assignment.id,
            new_date,
        )
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    if assignment.expected_return_date < today:
        logger.warning(
            "Extension denied | assignment_id=%s device=%s reason=device_overdue",
            assignment.id,
            assignment.device.serial_number,
        )
        raise ValueError("This device is overdue and cannot be extended.")

    if assignment.actual_return_date:
        logger.warning(
            "Extension denied | assignment_id=%s already_returned",
            assignment.id,
        )
        raise ValueError("Cannot extend a returned assignment")

    if new_date <= assignment.expected_return_date:
        logger.warning(
            "Extension denied | assignment_id=%s current_date=%s requested_date=%s",
            assignment.id,
            assignment.expected_return_date,
            new_date,
        )
        raise ValueError("New date must be after the current return date.")

    old_date = assignment.expected_return_date

    assignment.expected_return_date = new_date
    assignment.save()

    logger.info(
        "Assignment extended | assignment_id=%s device=%s from=%s to=%s",
        assignment.id,
        assignment.device.serial_number,
        old_date,
        new_date,
    )

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
    logger.info(
        "Device returned | assignment_id=%s user=%s device=%s fine=%s",
        assignment.id,
        assignment.user.username,
        device.serial_number,
        assignment.fine_amount,
    )

    return assignment

