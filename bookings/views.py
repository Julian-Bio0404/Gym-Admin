"""Bookings views."""

# Django REST Framework
from django.db.models.query import QuerySet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users import serializers

# Serializers
from bookings.serializers import (
    TrainingReserveModelSerializer, 
    CreateTrainingReserveSerializer
)

# Models
from users.models import User
from bookings.models import TrainingReserve

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
        serializers.is_valid(raise_exception=True)
        reserve = serializer.save()
        data = TrainingReserveModelSerializer(reserve).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def list_reserves(self, request):
        """List all the training reserves."""
        serializer = TrainingReserveModelSerializer(self.queryset, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

