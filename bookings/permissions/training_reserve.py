"""Training Reserve permissions classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    """Allow access only if the account owner is
     the same user who appears in the reservation."""

    def has_permission(self, request, view):
        """Verify that user is self."""
        try:
            return request.user.identification_number ==  request.data['identification_number']
        except KeyError:
            return request.user == view.get_object().user
