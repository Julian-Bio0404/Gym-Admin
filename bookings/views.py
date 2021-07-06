"""Bookings views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from bookings.permissions import IsSameClient, IsPhysio
from users.permissions import IsAdminGym

# Serializers
from bookings.serializers import (
    TrainingReserveModelSerializer, 
    CreateTrainingReserveSerializer,
    AppointmentModelSerializer,
    CreateAppointmentSerializer
)

# Models
from bookings.models import TrainingReserve, Appointment


class TrainingReserveViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """TrainingReserve view set."""

    queryset = TrainingReserve.objects.all()
    serializer_class = TrainingReserveModelSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action == 'reserve':
            permissions = [IsAuthenticated, IsSameClient]
        elif self.action == 'list':
            permissions = [IsAuthenticated, IsAdminGym]
        return[permission() for permission in permissions]
    
    @action(detail=False, methods=['post'])
    def reserve(self, request):
        """Training reserve."""
        serializer = CreateTrainingReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserve = serializer.save()
        data = TrainingReserveModelSerializer(reserve).data
        return Response(data, status=status.HTTP_201_CREATED)


class AppointmentViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """Appointment view set."""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentModelSerializer
    lookup_field = 'physio__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action == 'reserve_appointment':
            permissions = [IsAuthenticated, IsSameClient]
        elif self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated, IsPhysio]
        return[permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def reserve_appointment(self, request):
        """Appointment reserve."""
        serializer = CreateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserve_appointment = serializer.save()
        data = AppointmentModelSerializer(reserve_appointment).data
        return Response(data, status=status.HTTP_201_CREATED)
