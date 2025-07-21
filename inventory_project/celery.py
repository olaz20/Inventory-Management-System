from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings.base')


import django
django.setup()


app = Celery('inventory_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.autodiscover_tasks(['common'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')