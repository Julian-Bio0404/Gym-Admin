"""Appointment model."""

# Django
from django.db import models

# Utilities
from utils.models import GymModel


class Appointment(GymModel):
    """"
    Appointment model.
    
    An model of a physio appointment."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    
    physio = models.ForeignKey(
        "users.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name='physio'
    )

    date = models.DateTimeField(
        auto_now = False , 
        auto_now_add = False, 
        help_text='Date and time of the physio appointment.'
    )
