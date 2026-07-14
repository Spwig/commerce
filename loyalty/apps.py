from django.apps import AppConfig


class LoyaltyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "loyalty"

    def ready(self):
        """Import signal handlers when app is ready."""
        import loyalty.signals  # noqa
