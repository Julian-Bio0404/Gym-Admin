"""Membership model."""

# Django
from django.db import models

# Utilities 
from utils.models import GymModel


class Membership(GymModel):
    """Membership model.

    Membership is created every time a user makes a monthly payment.
    This has a duration of 30 days."""
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    category = models.CharField(
        max_length=1,
        default='P',
        help_text='category according to the type of affiliation of the user: A, B, C or P.'
    )

    available_days = models.PositiveSmallIntegerField(default=30)

    def __str__(self):
        """Return username and available_days."""
        return '{} has #{} days available.'.format(
            self.user.username,
            self.available_days
        )
        