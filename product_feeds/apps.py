from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductFeedsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product_feeds"
    verbose_name = _("Product Feeds")

    def ready(self):
        """Import signals and load providers on app startup"""
        from product_feeds.providers.loader import ProviderLoader

        # Trigger provider discovery on app startup
        ProviderLoader.discover_providers()
