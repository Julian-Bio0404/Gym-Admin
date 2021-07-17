"""Celery tasks."""

from __future__ import absolute_import, unicode_literals

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from celery import shared_task

# Models
from users.models import Membership, User
from bookings.models import *

# Utilities
from datetime import timedelta
import jwt


#------------------------------Users---------------------------------------
def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    # Generacion del token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


@shared_task # Asynch task
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! Verify your account'.format(user.username)
    from_email = 'Gym Admin <frameworkdjango7@gmail.com>'
    content = render_to_string(
        'users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()


#----------------------------Memberships-------------------------------------
@shared_task # Periodic task
def finalize_memberships():
    """Discounts one day from memberships each 
       day and remove them after 30 days."""
    memberships = Membership.objects.all()
    for membership in memberships:
        membership.available_days -= 1
        membership.save()
        if membership.available_days == 0:
            membership.delete()
            profile = membership.user.profile
            profile.is_active = False
            profile.save()


#----------------------------TrainingReserve----------------------------------
@shared_task # Periodic task
def remove_training_reserves():
    """Delete the reservation if it is already expired."""
    reserves = TrainingReserve.objects.all()
    now = timezone.now()
    for reserve in reserves:
        if reserve.date < now:
            reserve.delete()


#-----------------------------Appointments-------------------------------------
@shared_task # Periodic task
def remove_appointments():
    """"Delete the appointment if it is already expired."""
    appointments = Appointment.objects.all()
    now = timezone.now()
    for appointment in appointments:
        if appointment.date < now:
            appointment.delete()

