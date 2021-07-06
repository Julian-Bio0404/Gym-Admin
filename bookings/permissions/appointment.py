"""Appointment permissions classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from users.models import User


class IsPhysio(BasePermission):
    """Allow access only to physiotherapists"""

    def has_permission(self, request, view):
        """Verify that user is physio."""
        try:
            User.objects.get(
                username=request.user.username,
                rol='physio',
                is_verified=True
            )
        except User.DoesNotExist:
            return False
        return True
