"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Tasks
from taskapp.tasks import send_confirmation_email

# Serializers
from users.serializers.profiles import ProfileModelSerializer

# Models
from users.models import User, Profile

# Utilities
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'rol',
            'type_identification',
            'identification_number',
            'profile'
        )
        read_only_fields = [
            'rol',
            'type_identification',
            'identification_number',
            'profile'
        ]


class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer.
    Handle sign up data validation and user/profile creation."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    # Phone number
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}",
        message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    # Role
    def rol_validator(rol):
        """Verify the rol."""
        if rol not in ['client', 'admin', 'trainer', 'physio']:
            raise serializers.ValidationError('rol not allowed.')

    rol = serializers.CharField(validators=[rol_validator], default='client')

    # Identification document
    type_identification = serializers.CharField(max_length=2)
    identification_regex = RegexValidator(
        regex=r"\d{6,10}$",
        message='Identification number must be entered in the format: 199999999. Up to 11 digits allowed'
    )
    identification_number = serializers.CharField(validators=[
        identification_regex, 
        UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify password match and type identification."""

        # Identification
        type_identification = data['type_identification']
        if type_identification not in ['CC', 'TI']:
            raise serializers.ValidationError('type of identification not allowed.')

        # Password
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Password don??t match')
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
        handle the login request data."""
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve token."""
        token, created = Token.objects.get_or_create(user= self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    """Change user's password serializer."""
    
    old_password = serializers.CharField(required=True, min_length=8, max_length=64)
    password = serializers.CharField(required=True,min_length=8, max_length=64)
    password_confirmation = serializers.CharField(required=True, min_length=8, max_length=64)

    def validate(self, data):
        """Check password."""
        if not self.context['user'].check_password(data['old_password']):
            raise serializers.ValidationError('Wrong password.')

        if data['password_confirmation'] != data['password']:
            raise serializers.ValidationError('Password don??t match')
        password_validation.validate_password(data['password'])
        return data
    
    def save(self):
        """Update user's password."""
        user = self.context['user']
        user.set_password(self.validated_data['password'])
        user.save()
