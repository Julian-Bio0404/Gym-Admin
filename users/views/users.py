"""Users views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models.memberships import Membership

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import IsAccountOwner, IsAdminGym

# Serializers
from users.serializers import ProfileModelSerializer
from users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer, 
    UserModelSerializer,
    UserSignUpSerializer,
    MembershipModelSerializer,
    CreateMembershipSerializer,
    ChangePasswordSerializer
)

# Models
from users.models import User


class UserViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """User view set.
    Handle signup, login and account verification."""
    
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update', 'profile', 'change_password']:
            permissions = [IsAuthenticated, IsAccountOwner]
        elif self.action == 'membership':
            permissions = [IsAuthenticated, IsAdminGym]
        else:
            permissions = [IsAuthenticated]
        return[permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulation! Now choose a membership and start training with us.'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def change_password(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def membership(self, request, *args, **kwargs):
        """User membership."""
        serializer = CreateMembershipSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        membership = serializer.save()
        data = MembershipModelSerializer(membership).data
        return Response(data, status=status.HTTP_201_CREATED)
        