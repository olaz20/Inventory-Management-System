from .base import *
import sys
from decouple import config

import os
DEBUG = False
ALLOWED_HOSTS = ['inventory-project.onrender.com', 'localhost', '127.0.0.1']


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

