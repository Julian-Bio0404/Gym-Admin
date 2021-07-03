"""Bookings views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
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
    serializers_class = TrainingReserveModelSerializer

    @action(detail=False, methods=['post'])
    def reserve(self, request):
        """Training reserve."""
        serializer = CreateTrainingReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserve = serializer.save()
        data = TrainingReserveModelSerializer(reserve).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def list_reserves(self, request):
        """List all the training reserves."""
        serializer = TrainingReserveModelSerializer(self.queryset, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class AppointmentViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """Appointment view set."""

    queryset = Appointment.objects.all()
    serializers_class = TrainingReserveModelSerializer
    lookup_field = 'physio'

    @action(detail=False, methods=['post'])
    def reserve_appointment(self, request):
        """Appointment reserve."""
        serializer = CreateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserve_appointment = serializer.save()
        data = AppointmentModelSerializer(reserve_appointment).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def list_appointments(self, request):
        """List all the appointments."""
        serializer = AppointmentModelSerializer(self.queryset, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
