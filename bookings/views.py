"""Bookings views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    permission_classes = (IsAuthenticated,)
    lookup_field = 'user__username'
    
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
    serializer_class = TrainingReserveModelSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'physio__username'

    @action(detail=False, methods=['post'])
    def reserve_appointment(self, request):
        """Appointment reserve."""
        serializer = CreateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserve_appointment = serializer.save()
        data = AppointmentModelSerializer(reserve_appointment).data
        return Response(data, status=status.HTTP_201_CREATED)
