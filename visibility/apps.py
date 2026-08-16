from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VisibilityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "visibility"
    verbose_name = _("Visibility Rules")

    def ready(self):
        from . import signals  # noqa: F401  (register visibility-config signals)
