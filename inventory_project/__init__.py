from .celery import app as celery_app
from common import tasks
__all__ = ('celery_app',)
