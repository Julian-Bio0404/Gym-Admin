"""Users permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from users.models import User


class IsAccountOwner(BasePermission):
    """Allow access only to the account owner."""

    def has_permission(self, request, view):
        """Check obj and user are the same. """
        return request.user == view.get_object()


class IsAdminGym(BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        """Verify that user is admin."""
        try:
            User.objects.get(
                username=request.user.username,
                rol='admin',
                is_verified=True
            )
        except User.DoesNotExist:
            return False
        return True
