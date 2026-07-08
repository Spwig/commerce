from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeveloperPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'developer_portal'
    verbose_name = _('Developer Portal')

    # Admin sidebar configuration
    icon = 'fas fa-code'
    admin_section = 'system'
    admin_order = 90
