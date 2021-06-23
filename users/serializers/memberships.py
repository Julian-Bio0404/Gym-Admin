"""Membership serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Membership

# Serializers
from users.serializers import UserModelSerializer, ProfileModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            'category', 'available_days', 
            'user', 'profile'
        )
        read_only_fields = [
            'user', 'profile', 
            'available_days'
        ]

    def create(self, validated_data):
        """"Create a membership."""
        membership = Membership.objects.create(**validated_data)
        return membership
