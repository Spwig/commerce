from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PosAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pos_app"
    verbose_name = _("Point of Sale")

    def ready(self):
        # Import signals to register them
        import pos_app.signals  # noqa: F401
