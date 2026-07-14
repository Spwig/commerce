from django.apps import AppConfig


class EnterpriseSsoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "enterprise_sso"
    verbose_name = "Enterprise SSO"

    def ready(self):
        import enterprise_sso.signals  # noqa: F401
