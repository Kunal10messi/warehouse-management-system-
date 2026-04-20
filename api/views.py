from django.shortcuts import render
from rest_framework import mixins, viewsets
from inventory.models import Device
from allocations.models import Assignment
from .serializers import DeviceSerializer, AssignmentSerializer

class DeviceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class AssignmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Assignment.objects.select_related('user', 'device')
    serializer_class = AssignmentSerializer
    
    
    