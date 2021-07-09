"""Training reserve model."""

# Django
from django.db import models

# Utilities
from utils.models import GymModel


class TrainingReserve(GymModel):
    """"Training Reserve model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    date = models.DateTimeField(
        auto_now = False, 
        auto_now_add = False, 
        help_text='Date and time of the training reserve.'
    )
