from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PosApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pos_api'
    verbose_name = _('POS API')
