from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_api'
    verbose_name = _('Admin API')

    def ready(self):
        # Import signals when app is ready
        try:
            import admin_api.signals  # noqa: F401
        except ImportError:
            pass
