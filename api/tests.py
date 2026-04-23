from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User
from inventory.models import Device
from allocations.models import DeviceRequest

class APITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='admin',
            password='pass',
            role='ADMIN'
        )

        self.employee = User.objects.create_user(
            username='emp',
            password='pass',
            role='EMPLOYEE'
        )

        self.device = Device.objects.create(
            serial_number='TEST123',
            device_type='RAM',
            brand='Test',
            model='16GB',
            configuration='8GBx2',
            location='Rack',
            status='AVAILABLE'
        )

        self.request = DeviceRequest.objects.create(
            user=self.employee,
            device=self.device,
            from_date='2026-04-01',
            to_date='2026-04-10'
        )
        
    def test_unauthenticated_access(self):
        response = self.client.get('/api/v1/devices/')
        self.assertEqual(response.status_code, 403)
        
    def test_employee_cannot_approve(self):
        self.client.login(username='emp', password='pass')

        response = self.client.post(f'/api/v1/requests/{self.request.id}/approve/')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_approve(self):
        self.client.login(username='admin', password='pass')

        response = self.client.post(f'/api/v1/requests/{self.request.id}/approve/')
        self.assertEqual(response.status_code, 200)
        
    def test_employee_sees_only_own_assignments(self):
        self.client.login(username='emp', password='pass')

        response = self.client.get('/api/v1/assignments/')
        for item in response.data['results']:
            self.assertEqual(item['user']['username'], 'emp')