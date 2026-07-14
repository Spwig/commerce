from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AnnouncementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "announcements"
    verbose_name = _("Announcements")

    def ready(self):
        import announcements.signals  # noqa: F401
