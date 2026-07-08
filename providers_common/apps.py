from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProvidersCommonConfig(AppConfig):
    """Configuration for the Providers Common app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'providers_common'
    verbose_name = _('Provider Common Components')

    def ready(self):
        """
        Perform initialization when Django starts.
        """
        pass
