from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomFieldsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "custom_fields"
    verbose_name = _("Custom Fields")

    def ready(self):
        import custom_fields.signals  # noqa: F401
