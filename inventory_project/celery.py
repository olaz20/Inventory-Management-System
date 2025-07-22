from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")
if ENV == "production":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings.production')
elif ENV == "testing":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings.testing')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings.development')



load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

import django
django.setup()


app = Celery('inventory_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.autodiscover_tasks(['common'])



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')