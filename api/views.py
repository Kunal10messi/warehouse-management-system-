from django.shortcuts import render
from rest_framework import mixins, viewsets
from inventory.models import Device
from allocations.models import Assignment
from .serializers import DeviceSerializer, AssignmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from allocations.models import DeviceRequest
from .serializers import DeviceRequestSerializer
from allocations.services import approve_request, return_device, extend_date
from datetime import datetime

class DeviceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'device_type']

class AssignmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Assignment.objects.select_related('user', 'device')
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['device', 'user']
    
    @action(detail=True, methods=['post'])
    def return_device(self, request, pk=None): 
        assignment = self.get_object()
        return_device(assignment)
        return Response({"message": "Device returned"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        assignment = self.get_object()
        new_date = request.data.get('expected_return_date')
        if not new_date:
            return Response({"error": "expected_return_date required"}, status=400)
        try:
            from datetime import datetime
            new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=400)
        print("DATA:", request.data)
        extend_date(assignment, new_date)
        return Response({"message": "Return date extended"}, status=status.HTTP_200_OK)

    
class DeviceRequestViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = DeviceRequest.objects.select_related('device','user')
    serializer_class = DeviceRequestSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        device_request = self.get_object()
        approve_request(device_request)
        return Response({"message": "Request approved"}, status=status.HTTP_200_OK) 