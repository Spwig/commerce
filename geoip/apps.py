from django.apps import AppConfig


class GeoipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geoip'
    verbose_name = 'GeoIP Location Service'

    def ready(self):
        """
        Initialize the GeoIP app
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info("GeoIP app initialized")