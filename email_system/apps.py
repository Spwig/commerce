from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailSystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_system"
    verbose_name = _("Email System")

    def ready(self):
        """
        Import signal handlers when app is ready
        """
        try:
            import email_system.signals  # noqa: F401
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to import email_system signals: {e}")
