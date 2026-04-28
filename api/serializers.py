from rest_framework import serializers
from accounts.models import User
from inventory.models import Device
from allocations.models import DeviceRequest, Assignment

class DeviceRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceRequest
        fields = [
            'device',
            'from_date',
            'to_date',
        ]

    def validate_device(self, value):
        if value.status != 'AVAILABLE':
            raise serializers.ValidationError("Device is not available")
        return value

    def validate(self, data):
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError("Invalid date range")
        return data

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
            'email',
            'role'
        ]
    
class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    def validate_email(self, value):
        from accounts.models import User

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def validate_role(self, value):
        if value not in ['ADMIN', 'EMPLOYEE']:
            raise serializers.ValidationError("Invalid role")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class DeviceRequestReadSerializer(serializers.ModelSerializer):
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
        ]
    
class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'serial_number',
            'device_type',
            'brand',
            'model',
            'configuration',
            'location',
            'status'
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


