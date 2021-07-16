"""Celery app config."""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gym_admin.settings')
app = Celery(
    'taskapp', 
    broker='amqp://guest:admin1234@localhost:5672/django',
    include=['taskapp.tasks']
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()