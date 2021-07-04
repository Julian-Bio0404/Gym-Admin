"""Appointments serializers."""

# Django
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import User
from bookings.models import Appointment

# Serializers
from users.serializers import UserModelSerializer, ProfileModelSerializer


class AppointmentModelSerializer(serializers.ModelSerializer):
    """Appointment model serializer."""

    user = UserModelSerializer(read_only=True)
    profile = ProfileModelSerializer(read_only=True)
    physio = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Appointment
        fields = ('__all__')
        read_only_fields = ['user', 'profile']


class CreateAppointmentSerializer(serializers.Serializer):
    """Create a Appointment"""

    def physio_validator(physio):
        """Verify that the physio exists"""
        physios = User.objects.filter(rol='physio')
        physios_usernames = [physio.username for physio in physios]
        if physio not in physios_usernames:
            raise serializers.ValidationError('The physio does not exist')

    identification_regex = RegexValidator(
        regex=r"\d{6,10}$",
        message='Identification number must be entered in the format: 199999999. Up to 11 digits allowed'
    )

    identification_number = serializers.CharField(validators=[identification_regex])
    physio = serializers.CharField(validators=[physio_validator])
    date = serializers.DateTimeField()

    def validate(self, data):
        """Verify that the user has an active membership """

        user = User.objects.get(
            identification_number=data['identification_number'],
            is_verified=True
        )
        profile = user.profile
        
        if profile.is_active == False:
            raise serializers.ValidationError('The user does not have an active membership.')
        elif profile.is_active == True:
            try:
                appointment = Appointment.objects.get(user=user)
                if appointment:
                    raise serializers.ValidationError('You already have an appointment')
            except Appointment.DoesNotExist:
                return data

    def create(self, data):
        """Create a training reserve."""
        user = User.objects.get(
            identification_number=data.pop('identification_number')
        )
        profile = user.profile
        physio = User.objects.get(
            username=data.pop('physio'),
            rol='physio'
        )
        appointment = Appointment.objects.create(
            user=user,
            profile=profile,
            physio=physio,
            date=data['date']
        )
        return appointment
