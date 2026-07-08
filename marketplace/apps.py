from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketplace'
    verbose_name = _('Marketplace')
