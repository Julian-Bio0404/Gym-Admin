"""User model."""

# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Utilities
from utils.models import GymModel


class User(GymModel, AbstractUser):
    """User model.
    Extend from Django's Abstract User and add some extra fields."""

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
            }
    )

    # phone number validator
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17, 
        blank=True
    )

    rol = models.CharField(
        'rol',
        max_length=7,
        default='client',
        help_text=(
            'Help easily distringuish users and perform queries. Clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text=(
            'Set to true when the user have verified its email add'
        )
    )

    CEDULA = 'CC'
    ID_CARD = 'TI'
    types_identification = [(CEDULA, 'cedula'), (ID_CARD, 'id_card')]

    type_identification = models.CharField(
        max_length=2,
        choices=types_identification,
        null=False, 
        help_text='type of user identification document: CC or TI.'
    )

    identification_regex = RegexValidator(
        regex=r"\d{6,10}$",
        message='Identification number must be entered in the format: 199999999. Up to 11 digits allowed'
    )

    identification_number = models.CharField(
        validators=[identification_regex],
        max_length=11, 
        blank=False
    )

    # Username configuration
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'type_identification', 'identification_number']
    
    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
        