"""Memberships serializer."""

# Django
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Membership, User

# Serializers
from users.serializers import UserModelSerializer, ProfileModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = ('__all__')
        read_only_fields = [
            'user', 'available_days'
        ]

    
class CreateMembershipSerializer(serializers.Serializer):
    """Create a membership."""

    identification_regex = RegexValidator(
        regex=r"\d{6,10}$",
        message='Identification number must be entered in the format: 199999999. Up to 11 digits allowed'
    )
    identification_number = serializers.CharField(validators=[identification_regex])
    category = serializers.CharField(max_length=1, default='P')

    def validate(self, data):
        """Verify that the user exists, if it is verified 
        and if it has a membership."""

        # User
        user = User.objects.get(
            identification_number=data['identification_number'],
            is_verified=True
        )
        if not user:
            raise serializers.ValidationError('The user does not exist or is not verified.')

        # category
        category = data['category']
        if category not in ['A', 'B', 'C', 'P']:
            raise serializers.ValidationError('Category not allowed.')    
        
        # Membership
        try:
            membership = Membership.objects.get(user=user)
            if membership:
                raise serializers.ValidationError('The user already has a membership.')
        except Membership.DoesNotExist:
            return data

    def create(self, data):
        """"Create a membership."""
        user = User.objects.get(
            identification_number=data.pop('identification_number')
        )
        membership = Membership.objects.create(
            user=user, 
            category=data['category']
        )
        profile = user.profile
        profile.is_active = True
        profile.save()
        return membership
