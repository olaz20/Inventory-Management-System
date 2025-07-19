from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import logging
from django.core.management import CommandError
from decouple import config


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automatically creates a superuser if none exists, using environment variables'
    def handle(self, *args, **kwargs):
        User = get_user_model()
        try:
            if User.objects.filter(is_superuser=True).exists():
                self.stdout.write(self.style.WARNING('Superuser already exists. Skipping creation.'))
                logger.info('Superuser creation skipped: superuser already exists.')
                return
            username = config('SUPERUSER_USERNAME', 'admin')
            email = config('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            password = config('DJANGO_SUPERUSER_PASSWORD')

            if not password:
                raise CommandError('DJANGO_SUPERUSER_PASSWORD must be set.')
            if not username:
                raise CommandError('SUPERUSER_USERNAME must be set.')
            if not email:
                raise CommandError('DJANGO_SUPERUSER_EMAIL must be set.')
            
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
        except Exception as e:
            logger.error(f'Error creating superuser: {str(e)}')
            raise CommandError(f'Failed to create superuser: {str(e)}')