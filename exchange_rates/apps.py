from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExchangeRatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exchange_rates'
    verbose_name = _("Exchange Rates")

    def ready(self):
        """Import signals and load providers"""
        from exchange_rates.providers.loader import ProviderLoader
        # Trigger provider discovery on app startup
        ProviderLoader.discover_providers()
