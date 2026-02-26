from django.db import models

class Device(models.Model):
    DEVICE_TYPE_CHOICES = (
        ('GPU', 'GPU'),
        ('CPU', 'CPU'),
        ('RAM', 'RAM'),
        ('SSD', 'SSD'),
        ('OTHER', 'Other'),
    )

    serial_number = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    configuration = models.CharField(max_length=200)  # e.g., 16GB VRAM, 3.5GHz, etc.
    location = models.CharField(max_length=100)  # Rack A3, Shelf 2, etc.
    status = models.CharField(
        max_length=20,
        choices=(('AVAILABLE', 'Available'), ('ASSIGNED', 'Assigned'), ('MAINTENANCE', 'Maintenance')),
        default='AVAILABLE'
    )

    def __str__(self):
        return f"{self.device_type} - {self.serial_number}"
