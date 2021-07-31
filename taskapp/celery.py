"""Celery app config."""

from __future__ import absolute_import, unicode_literals

# Celery
from celery import Celery
from celery.schedules import crontab

# Utilities
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gym_admin.settings')
app = Celery(
    'taskapp', 
    include=['taskapp.tasks']
)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-75-minutes': {
        'task': 'taskapp.tasks.remove_appointments',
        'schedule': crontab(minute=0, hour='*/2')
    }, 
    
    'every-80-minutes': {
        'task': 'taskapp.tasks.remove_training_reserves',
        'schedule': crontab(minute=0, hour='*/2')
    },

    'every-1-day': {
        'task': 'taskapp.tasks.finalize_memberships',
        'schedule': crontab(minute=0, hour=0)
    }
}

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()