from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AffiliateConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "affiliate"
    verbose_name = _("Affiliate Marketing")

    # Admin sidebar configuration
    icon = "fas fa-handshake"  # Font Awesome icon for sidebar
    admin_section = "sales"  # Group with Sales & Promotions
    admin_order = 50  # Order within the section

    def ready(self):
        """
        Import signals when Django starts.
        This ensures signal handlers are registered.
        """
        import affiliate.signals  # noqa: F401
