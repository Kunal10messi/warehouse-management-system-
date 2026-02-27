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
        for i in range(1, 3):
            username = f"emp{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=f"emp{i}@gmail.com",
                    password="0728"
                )

        self.stdout.write(self.style.SUCCESS("Sample users created."))

        # ==========================
        # Create Devices
        # ==========================

        devices = [
            {
                "serial_number": "GPU-001",
                "device_type": "GPU",
                "brand": "NVIDIA",
                "model": "RTX 3080",
                "configuration": "10GB GDDR6X",
                "location": "Rack A1",
            },
            {
                "serial_number": "CPU-001",
                "device_type": "CPU",
                "brand": "Intel",
                "model": "i9-13900K",
                "configuration": "3.0GHz 24-Core",
                "location": "Rack B2",
            },
            {
                "serial_number": "RAM-001",
                "device_type": "RAM",
                "brand": "Corsair",
                "model": "Vengeance LPX",
                "configuration": "16GB DDR4",
                "location": "Rack C3",
            },
            {
                "serial_number": "SSD-001",
                "device_type": "SSD",
                "brand": "Samsung",
                "model": "970 EVO",
                "configuration": "1TB NVMe",
                "location": "Rack D4",
            },
        ]

        for device_data in devices:
            Device.objects.get_or_create(
                serial_number=device_data["serial_number"],
                defaults=device_data
            )

        self.stdout.write(self.style.SUCCESS("Devices created successfully."))
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))