from .base import *
import sys
from decouple import config

import os
DEBUG = False
ALLOWED_HOSTS = ['inventory-management-system-7t9o.onrender.com', 'localhost', '127.0.0.1']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

DATABASES = {
    'default': dj_database_url.config(
        default=config("DATABASE_URL")  # Uses the Render database URL
    )
}

CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
