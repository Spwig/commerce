from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReferralsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'referrals'
    verbose_name = _('Referrals')

    def ready(self):
        """Import signals when app is ready."""
        import referrals.signals  # noqa
