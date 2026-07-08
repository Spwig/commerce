"""
Address Autocomplete App Configuration
Handles automatic geocoder token provisioning on startup
"""

import asyncio
import logging
from django.apps import AppConfig
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class AddressAutocompleteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'address_autocomplete'
    verbose_name = 'Address Autocomplete'

    def ready(self):
        """
        App initialization - provision geocoder token on startup.
        """
        # Only run in main process (not in migrations or commands)
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0] if sys.argv else False:
            self.provision_geocoder_token()

    def provision_geocoder_token(self):
        """
        Automatically provision geocoder token based on license.
        """
        # Check if we already have a valid token
        existing_token = cache.get('geocoder_jwt_token')
        if existing_token:
            logger.info("Geocoder token already provisioned")
            return

        # Check if license key is configured
        license_key = getattr(settings, 'PLATFORM_LICENSE_KEY', None)
        if not license_key:
            logger.info(
                "No PLATFORM_LICENSE_KEY in settings. "
                "Configure license to enable geocoder service."
            )
            return

        try:
            # Schedule provisioning as background task
            from django.core.management import call_command
            call_command('provision_geocoder_token', '--output-format=text')
            logger.info("Geocoder token provisioning completed")

        except Exception as e:
            logger.error(f"Failed to provision geocoder token: {e}")
