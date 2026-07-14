import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class DesignConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "design"
    verbose_name = _("Design")

    def ready(self):
        """Import signals when app is ready and auto-populate theme CSS."""
        import design.signals  # noqa: F401

        # Auto-populate compiled_css for themes that don't have it
        # This ensures themes work after platform updates without manual intervention
        self._auto_populate_theme_css()

    def _auto_populate_theme_css(self):
        """Populate compiled_css for themes missing it.

        This runs on app startup to ensure themes extracted from ZIP packages
        have their CSS stored in the database for serving via ThemeCSSView.
        Runs safely without blocking startup even if DB isn't ready.
        """
        import sys

        # Skip during migrations and other management commands
        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return

        try:
            from django.db import connection

            # Check if the theme table exists (handles fresh installs)
            table_names = connection.introspection.table_names()
            if "design_theme" not in table_names:
                return

            from .theme_models import Theme

            # Find active themes without compiled_css
            themes_to_populate = Theme.objects.filter(is_active=True, compiled_css="")

            if not themes_to_populate.exists():
                return

            for theme in themes_to_populate:
                try:
                    # extract_theme() will populate compiled_css
                    if theme.package_file:
                        logger.info(f"Auto-populating compiled_css for theme: {theme.slug}")
                        theme.extract_theme()
                except Exception as e:
                    # Don't block startup on individual theme failures
                    logger.warning(f"Failed to auto-populate CSS for theme {theme.slug}: {e}")

        except Exception as e:
            # Never block app startup - CSS can be populated on first request
            logger.debug(f"Theme CSS auto-populate skipped: {e}")
