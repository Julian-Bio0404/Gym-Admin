"""Profile serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Profile, Membership


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""
        model = Profile
        fields = (
            'picture',
            'age',
            'weight',
            'height',
            'is_active'
        )
        read_only_fields = ['is_active']
