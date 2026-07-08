from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    verbose_name = _('Search')

    def ready(self):
        # Import signals to register them
        from . import signals  # noqa: F401
        # Connect content model signals
        signals.connect_content_signals()
