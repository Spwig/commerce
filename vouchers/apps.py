from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VouchersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vouchers"
    verbose_name = _("Vouchers")
