"""Training reserves serializers."""

# Django
from django.core.validators import RegexValidator
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import User
from bookings.models import TrainingReserve

# Serializers
from users.serializers import UserModelSerializer, ProfileModelSerializer


class TrainingReserveModelSerializer(serializers.ModelSerializer):
    """Appointment model serializer."""

    user = UserModelSerializer(read_only=True)
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = TrainingReserve
        fields = ('__all__')
        read_only_fields = ['user', 'profile']


class CreateTrainingReserveSerializer(serializers.Serializer):
    """Create a training reserve."""

    identification_regex = RegexValidator(
        regex=r"\d{6,10}$",
        message='Identification number must be entered in the format: 199999999. Up to 11 digits allowed'
    )
    identification_number = serializers.CharField(validators=[identification_regex])
    date = serializers.DateTimeField()

    def validate(self, data):
        """Verify that the user has an active membership,
        and the reserve. """
        user = User.objects.get(
            identification_number=data['identification_number'],
            is_verified=True
        )
        profile = user.profile
        reserves = TrainingReserve.objects.filter(date=data['date']).count()

        try:
            user_reserve = TrainingReserve.objects.get(user=user)
            if user_reserve:
                raise serializers.ValidationError('You already have a reserve.')
        except TrainingReserve.DoesNotExist:
            if profile.is_active == False:
                raise serializers.ValidationError('The user does not have an active membership.')
            if data['date'] <= timezone.now():
                raise serializers.ValidationError('Time not available')
            if reserves == 26:
                raise serializers.ValidationError('The capacity at this time is full.')
            else:
                return data

    def create(self, validated_data):
        """Create a training reserve."""
        user = User.objects.get(
            identification_number=validated_data.pop('identification_number')
        )
        profile = user.profile
        reserve = TrainingReserve.objects.create(
            user=user,
            profile=profile,
            date=validated_data['date']
        )
        return reserve
