from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AttributionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "attribution"
    verbose_name = _("Revenue Attribution")

    def ready(self):
        # Signals are wired in later phases (identity stitch, order-completion
        # orchestrator). Import guarded so P0 stays behaviour-free.
        try:
            import attribution.signals  # noqa: F401
        except ImportError:
            pass
