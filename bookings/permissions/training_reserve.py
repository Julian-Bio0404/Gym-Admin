"""Training Reserve permissions classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsSameClient(BasePermission):
    """Allow access only if the account owner is
     the same user who appears in the reservation."""

    def has_permission(self, request, view):
        """Verify that user is admin."""
        return request.user.identification_number ==  request.data['identification_number']
