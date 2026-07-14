from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DomainSslConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "domain_ssl"
    verbose_name = _("Domain & SSL")
