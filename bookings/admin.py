"""Booking models admin."""

# Django
from django.contrib import admin

# Models
from bookings.models import Appointment, TrainingReserve


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Appointment model admin."""

    list_display = ('user', 'physio', 'date')
    search_fields = ('user__username', 'physio', 'date')
    list_filter = ('physio', 'date')


@admin.register(TrainingReserve)
class TrainingReserveAdmin(admin.ModelAdmin):
    """TrainingReserve model admin."""

    list_display = ('user', 'date')
    search_fields = ('user__username', 'date')
