from allocations.models import Assignment
from inventory.models import Device
import logging
logger = logging.getLogger(__name__)

def create_device(data):
    device = Device.objects.create(**data)
    logger.info(
        "Device created | device_id=%s serial=%s type=%s",
        device.id,
        device.serial_number,
        device.device_type,
    )
    return device

def delete_device(device):
    # check if device is currently assigned
    is_assigned = Assignment.objects.filter(
        device=device,
        actual_return_date__isnull=True
    ).exists()

    if is_assigned:
        logger.warning(
            "Device deletion denied | device_id=%s serial=%s active_assignment_exists",
            device.id,
            device.serial_number,
        )
        raise ValueError("Cannot delete device that is currently assigned")
    device_id = device.id
    serial = device.serial_number
    device.delete()
    logger.info(
        "Device deleted | device_id=%s serial=%s",
        device_id,
        serial,
    )
    
def update_device(device, data):
    # Validate serial number once
    if 'serial_number' in data:
        if Device.objects.filter(
            serial_number=data['serial_number']
        ).exclude(id=device.id).exists():
            logger.warning(
                "Device update failed | device_id=%s duplicate_serial=%s",
                device.id,
                data["serial_number"],
            )
            raise ValueError("Serial number already exists")

    # Apply updates
    for field, value in data.items():
        setattr(device, field, value)

    device.save()
    logger.info(
        "Device updated | device_id=%s serial=%s",
        device.id,
        device.serial_number,
    )
    return device