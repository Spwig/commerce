from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AgenticConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "agentic"
    verbose_name = _("Agentic Commerce")

    def ready(self):
        try:
            import agentic.signals  # noqa: F401
        except ImportError:
            pass
