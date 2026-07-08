from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = _('Catalog')

    def ready(self):
        """Import signal handlers when app is ready"""
        import catalog.signals  # noqa: F401
