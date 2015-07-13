from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hitdong.settings.prod')

app = Celery('hitdong',
             backend=settings.BACKEND_URL,
             broker=settings.BROKER_URL)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
