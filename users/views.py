"""Users views."""

# Django REST framework
from users.models.memberships import Membership
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from users.serializers import ProfileModelSerializer
from users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer, 
    UserModelSerializer,
    UserSignUpSerializer,
    MembershipModelSerializer,
    CreateMembershipSerializer
)

# Models
from users.models import User


class UserViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """User view set.
    Handle signup, login and account verification."""
    
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

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
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
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

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        try:
            membership = Membership.objects.get(profile=profile)
            if membership:
                profile.is_active = True
                serializer = ProfileModelSerializer(
                    profile,
                    data=request.data,
                    partial=partial
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data = UserModelSerializer(user).data
                return Response(data)
        except:
            profile.is_active = False
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
        data.pop('profile')
        return Response(data, status=status.HTTP_201_CREATED)
        