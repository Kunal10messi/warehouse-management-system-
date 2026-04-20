from rest_framework import serializers
from accounts.models import User
from inventory.models import Device
from allocations.models import DeviceRequest, Assignment


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id',
            'serial_number',
            'device_type',
            'brand',
            'model',
            'configuration',
            'location',
            'status',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'role'
        ]
    

class DeviceRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)
    class Meta:
        model = DeviceRequest
        fields = [
            'id',
            'user',
            'device',
            'request_date',
            'from_date',
            'to_date',
            'status',
            'rejection_seen',
        ]
        

class AssignmentSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    fine = serializers.ReadOnlyField()
    class Meta:
        model = Assignment
        fields = [
            'id',
            'user',
            'device',
            'issue_date',
            'expected_return_date',
            'actual_return_date',
            'fine_amount',
            'fine',  # computed property
            'approval_seen',
        ]


