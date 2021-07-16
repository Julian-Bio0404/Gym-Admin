"""Celery tasks."""

from __future__ import absolute_import, unicode_literals

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from .celery import app

# Models
from users.models import User

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


@app.task(name='send_confirmation_email')
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

