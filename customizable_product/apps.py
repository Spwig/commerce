from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomizableProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customizable_product"
    verbose_name = _("Customizable Products")
