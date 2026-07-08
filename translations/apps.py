from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TranslationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translations'
    verbose_name = _('Translations')

    def ready(self):
        # Import signal handlers when app is ready
        try:
            from . import signals  # noqa: F401
        except ImportError:
            pass

        # Extend Django's LANGUAGES with active SiteLanguage records
        # so i18n_patterns, set_language, and LocaleMiddleware recognize them
        self._extend_languages_from_db()

    def _extend_languages_from_db(self):
        """Add active SiteLanguage codes to settings.LANGUAGES at startup."""
        try:
            from django.conf import settings
            from .models import SiteLanguage

            builtin_codes = {code for code, _ in settings.LANGUAGES}
            for sl in SiteLanguage.objects.filter(is_active=True):
                if sl.code not in builtin_codes:
                    settings.LANGUAGES.append((sl.code, sl.name))
                    builtin_codes.add(sl.code)
        except Exception:
            # Table may not exist yet during migrations
            pass
