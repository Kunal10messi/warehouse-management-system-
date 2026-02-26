from django.db import models
from django.conf import settings
from inventory.models import Device


User = settings.AUTH_USER_MODEL

class DeviceRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user} → {self.device} ({self.status})"


class Assignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def fine(self):
        from .services import FINE_PER_DAY  # import here, not at top

        if self.actual_return_date and self.actual_return_date > self.expected_return_date:
            days_late = (self.actual_return_date - self.expected_return_date).days
            return days_late * FINE_PER_DAY
        return 0

