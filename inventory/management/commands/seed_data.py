from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import Device

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with initial demo data"

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Create Superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@gmail.com",
                password="0728",
                role='ADMIN',
            )
            self.stdout.write(self.style.SUCCESS("Superuser created."))
        else:
            self.stdout.write("Superuser already exists.")


        # Create Sample Users
        for i in range(1, 11):
            username = f"emp{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=f"emp{i}@gmail.com",
                    password="0728"
                )

        self.stdout.write(self.style.SUCCESS("Sample users created."))

        # Create Devices
        devices = [
            # GPUS
            {
                "serial_number": "GPU-001",
                "device_type": "GPU",
                "brand": "NVIDIA",
                "model": "RTX 3080",
                "configuration": "10GB GDDR6X",
                "location": "Rack A1",
            },
            {
                "serial_number": "GPU-002",
                "device_type": "GPU",
                "brand": "NVIDIA",
                "model": "RTX 4090",
                "configuration": "24GB GDDR6X",
                "location": "Rack A2",
            },
            {
                "serial_number": "GPU-003",
                "device_type": "GPU",
                "brand": "NVIDIA",
                "model": "RTX 3050",
                "configuration": "4GB GDDR6X",
                "location": "Rack A3",
            },
            {
                "serial_number": "GPU-004",
                "device_type": "GPU",
                "brand": "AMD",
                "model": "Radeon RX 7600",
                "configuration": "8GB GDDR6X",
                "location": "Rack A4",
            },
            {
                "serial_number": "GPU-005",
                "device_type": "GPU",
                "brand": "AMD",
                "model": "Radeon RX 4600",
                "configuration": "24GB GDDR6X",
                "location": "Rack A5",
            },
            # CPU
            {
                "serial_number": "CPU-001",
                "device_type": "CPU",
                "brand": "Intel",
                "model": "i9-13900K",
                "configuration": "3.0GHz 24-Core",
                "location": "Rack B1",
            },
            {
                "serial_number": "CPU-002",
                "device_type": "CPU",
                "brand": "AMD",
                "model": "Ryzen-7",
                "configuration": "2.3GHz 16-Core",
                "location": "Rack B2",
            },
            {
                "serial_number": "CPU-003",
                "device_type": "CPU",
                "brand": "Intel",
                "model": "i3-5900K",
                "configuration": "1.0GHz 2-Core",
                "location": "Rack B3",
            },
            {
                "serial_number": "CPU-004",
                "device_type": "CPU",
                "brand": "AMD",
                "model": "Ryzen-5",
                "configuration": "2.8GHz 16-Core",
                "location": "Rack B4",
            },
            {
                "serial_number": "CPU-005",
                "device_type": "CPU",
                "brand": "Intel",
                "model": "i9-11900H",
                "configuration": "2.8.0GHz 24-Core",
                "location": "Rack B5",
            },
            # RAM
            {
                "serial_number": "RAM-001",
                "device_type": "RAM",
                "brand": "Corsair",
                "model": "Vengeance LPX",
                "configuration": "16GB DDR4",
                "location": "Rack C1",
            },
            {
                "serial_number": "RAM-002",
                "device_type": "RAM",
                "brand": "Corsair",
                "model": "Vengeance LPX",
                "configuration": "32GB DDR4",
                "location": "Rack C2",
            },
            {
                "serial_number": "RAM-003",
                "device_type": "RAM",
                "brand": "G.Skill",
                "model": " Ripjaws",
                "configuration": "16GB DDR5",
                "location": "Rack C3",
            },
            {
                "serial_number": "RAM-004",
                "device_type": "RAM",
                "brand": "G,Skill",
                "model": " Ripjaws",
                "configuration": "8GB DDR4",
                "location": "Rack C4",
            },
            {
                "serial_number": "RAM-005",
                "device_type": "RAM",
                "brand": "Corsair",
                "model": "Vengeance LPX",
                "configuration": "8GB DDR5",
                "location": "Rack C5",
            },
            # SSD
            {
                "serial_number": "SSD-001",
                "device_type": "SSD",
                "brand": "Samsung",
                "model": "970 EVO",
                "configuration": "1TB NVMe",
                "location": "Rack D1",
            },
            {
                "serial_number": "SSD-002",
                "device_type": "SSD",
                "brand": "Samsung",
                "model": "970 EVO",
                "configuration": "5TB NVMe",
                "location": "Rack D2",
            },
            {
                "serial_number": "SSD-003",
                "device_type": "SSD",
                "brand": "Crosshair",
                "model": "Morbin",
                "configuration": "10TB NVMe",
                "location": "Rack D3",
            },
            {
                "serial_number": "SSD-004",
                "device_type": "SSD",
                "brand": "Samsung",
                "model": "970 EVO",
                "configuration": "1TB NVMe",
                "location": "Rack D4",
            },
            {
                "serial_number": "SSD-005",
                "device_type": "SSD",
                "brand": "Samsung",
                "model": "Morbin",
                "configuration": "1TB NVMe",
                "location": "Rack D5",
            },
        ]

        for device_data in devices:
            Device.objects.get_or_create(
                serial_number=device_data["serial_number"],
                defaults=device_data
            )

        self.stdout.write(self.style.SUCCESS("Devices created successfully."))
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))