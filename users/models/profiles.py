"""Profile model."""

# Django
from django.db import models

# Utilities
from utils.models import GymModel


class Profile(GymModel):
    """Profile model.
    
    A profile holds a users public data like,
    picture, features and if it is active."""

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    age = models.PositiveSmallIntegerField(null=True, blank=True)

    weight = models.PositiveIntegerField(
        'user weight',
        default=0,
        help_text='user weight in float.'
    )

    height = models.PositiveIntegerField(
        'user height',
        default=0,
       help_text= 'user height in float.'
    )

    is_active = models.BooleanField(
        default=False,
        help_text='Only active users can have gym services.'
    )

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
        