from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from inventory.models import Device
from accounts.models import User
from allocations.models import Assignment
from .serializers import DeviceSerializer, AssignmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from allocations.models import DeviceRequest
from .serializers import DeviceRequestReadSerializer, DeviceRequestCreateSerializer, UserSerializer, CreateUserSerializer, DeviceCreateSerializer, UpdateUserSerializer
from allocations.services import approve_request, return_device, extend_date, create_request, reject_request
from inventory.services import create_device, delete_device, update_device
from accounts.services import create_employee, update_user, delete_user
from datetime import datetime
from .permissions import IsAdminRole
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
import logging
logger = logging.getLogger(__name__)

class DeviceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Device.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'device_type']
    search_fields = ['serial_number', 'brand', 'model', 'configuration']
    ordering_fields = ['serial_numer', 'location']
    ordering = ['device_type']

    def get_serializer_class(self):
        if self.action == 'create':
            return DeviceCreateSerializer
        return DeviceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminRole()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = create_device(serializer.validated_data)

        return Response(
            DeviceSerializer(device).data,
            status=status.HTTP_201_CREATED
        ) 
    
    def destroy(self, request, pk=None):
        device = self.get_object()
        delete_device(device)
        return Response({"message": "Device deleted"}, status=200)
    
    def update(self, request, pk=None):
        device = self.get_object()

        serializer = self.get_serializer(device, data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_device = update_device(device, serializer.validated_data)

        return Response(DeviceSerializer(updated_device).data)

    def partial_update(self, request, pk=None):
        device = self.get_object()

        serializer = self.get_serializer(device, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_device = update_device(device, serializer.validated_data)

        return Response(DeviceSerializer(updated_device).data) 

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']
    ordering = ['username']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminRole()]
        return [IsAuthenticated()]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_employee(serializer.validated_data)

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = update_user(instance, serializer.validated_data)

        return Response(UserSerializer(user).data)    
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = update_user(instance, serializer.validated_data)

        return Response(UserSerializer(user).data)
    
    def destroy(self, request, pk=None):
        user = self.get_object()
        
        if user == request.user:
            logger.warning(f"User {request.user.id} attempted self-delete")
            return Response(
                {"error": "You cannot delete yourself"},
                status=400
            )
        
        delete_user(user)

        return Response({"message": "User deleted"}, status=200)


class AssignmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Assignment.objects.select_related('user', 'device')
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['device', 'user']
    search_fields = [
        'user__username',
        'device__serial_number',
        'device__brand',
        'device__model',
        'device__device_type'
    ]
    ordering_fields = ['issue_date', 'expected_return_date']
    ordering = ['-issue_date']
    
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Assignment.objects.select_related('user', 'device')
        return Assignment.objects.select_related('user', 'device').filter(user=user)
    
    @action(detail=True, methods=['post'])
    def return_device(self, request, pk=None): 
        assignment = self.get_object()
        return_device(assignment)
        return Response({"message": "Device returned"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        assignment = self.get_object()

        try:
            extend_date(assignment, request.data.get('expected_return_date'))
            return Response({"message": "Return date extended"}, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    
class DeviceRequestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = DeviceRequest.objects.select_related('device','user')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'user__username',
        'device__serial_number',
        'device__brand',
        'device__model',
        'device__device_type'
    ]
    ordering_fields = ['request_date']
    ordering = ['-request_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DeviceRequestCreateSerializer
        return DeviceRequestReadSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return DeviceRequest.objects.select_related('user', 'device')
        return DeviceRequest.objects.select_related('user', 'device').filter(user = user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_request = create_request(
            user=request.user,
            device=serializer.validated_data['device'],
            from_date=serializer.validated_data['from_date'],
            to_date=serializer.validated_data['to_date']
        )

        return Response(
            DeviceRequestReadSerializer(device_request).data,
            status=201
        ) 
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def approve(self, request, pk=None):
        device_request = self.get_object()
        approve_request(device_request)
        return Response({"message": "Request approved"}, status=status.HTTP_200_OK) 
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def reject(self, request, pk=None):
        device_request = self.get_object()
        reject_request(device_request)
        return Response({"message": "Request rejected"}, status=status.HTTP_200_OK) 
    
