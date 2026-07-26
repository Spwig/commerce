from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"
    verbose_name = _("Cart")

    def ready(self):
        from . import signals  # noqa: F401
