from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SocialSharingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "social_sharing"
    verbose_name = _("Social Sharing")

    def ready(self):
        """Import signals when app is ready"""
        import social_sharing.signals  # noqa
