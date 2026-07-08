from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarketplaceCheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketplace_checkout'
    verbose_name = _('Marketplace Checkout')
