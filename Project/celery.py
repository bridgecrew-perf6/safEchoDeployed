from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from celery.schedules import crontab
from celery import Celery
from . import celeryconfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

app = Celery('time_consultants',
             broker=celeryconfig.broker_url,
             backend=celeryconfig.result_backend,
             )
app.config_from_object("Project.celeryconfig")
app.autodiscover_tasks()

