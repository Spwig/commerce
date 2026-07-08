from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebhooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhooks'
    verbose_name = _('Webhooks')

    def ready(self):
        # Import signals to register them
        from . import signals  # noqa: F401
