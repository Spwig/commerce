from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShippingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipping"
    verbose_name = _("Shipping & Fulfillment")

    def ready(self):
        """
        Import signal handlers when the app is ready
        This ensures signals are registered before any models are saved
        """
        import shipping.signals  # noqa: F401
