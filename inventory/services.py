from allocations.models import Assignment
from inventory.models import Device
import logging
logger = logging.getLogger(__name__)

def create_device(data):
    device = Device.objects.create(**data)
    logger.info(f"Device created: {device.id} ({device.serial_number})")
    return device

def delete_device(device):
    # check if device is currently assigned
    is_assigned = Assignment.objects.filter(
        device=device,
        actual_return_date__isnull=True
    ).exists()

    if is_assigned:
        raise ValueError("Cannot delete device that is currently assigned")
    logger.info(f"Device deleted: {device.id}")
    device.delete()
    
def update_device(device, data):
    # Validate serial number once
    if 'serial_number' in data:
        if Device.objects.filter(
            serial_number=data['serial_number']
        ).exclude(id=device.id).exists():
            raise ValueError("Serial number already exists")

    # Apply updates
    for field, value in data.items():
        setattr(device, field, value)

    device.save()
    logger.info(f"Device updated: {device.id}")
    return device