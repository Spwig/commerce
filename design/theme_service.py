"""
Theme Service - Handles theme operations including installation, migration, and CSS generation
"""

import logging
from pathlib import Path

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class ThemeService:
    """Service class for theme operations"""

    def __init__(self):
        self.themes_root = Path(settings.STATIC_ROOT) / "themes"
        self.themes_root.mkdir(exist_ok=True, parents=True)

    def get_current_theme(self):
        """Get currently active theme.

        Delegates to get_active_theme() — the canonical source of truth —
        so all callers resolve the active theme consistently via
        GlobalDesignSettings.active_theme.
        """
        from .theme_utils import get_active_theme

        current = cache.get("current_theme")
        if not current:
            current = get_active_theme()
            if current:
                cache.set("current_theme", current, 3600)
        return current

    def generate_layered_css(self, request=None):
        """
        Generate complete CSS with proper layering:
        1. Base CSS (platform utilities)
        2. Theme CSS (from theme package)
        3. Brand CSS (from database)
        4. Overrides (per-page/widget)
        """
        from .theme_models import ThemeBranding

        css_parts = []

        # 1. Base CSS (loaded separately via static files)
        # This would be in base.css

        # 2. Theme CSS
        theme = self.get_current_theme()
        if theme:
            css_parts.append(f"/* Theme: {theme.name} v{theme.version} */")
            theme_css_url = theme.get_css_url()
            if theme_css_url:
                css_parts.append(f'@import url("{theme_css_url}");')

        # 3. Brand CSS
        try:
            branding = ThemeBranding.objects.first()
            if branding:
                if not branding.generated_css:
                    branding.generate_css()
                css_parts.append("\n/* Brand Customizations */")
                css_parts.append(branding.generated_css)
        except Exception:
            pass

        # 4. Page/Widget overrides would be added dynamically

        return "\n".join(css_parts)

    def preview_theme(self, theme_id, branding_tokens=None):
        """
        Generate preview of theme with optional branding tokens
        Returns preview CSS for iframe rendering
        """
        from .theme_models import Theme

        try:
            theme = Theme.objects.get(id=theme_id)
            css_parts = []

            # Add theme CSS
            if theme.get_css_url():
                css_parts.append(f'@import url("{theme.get_css_url()}");')

            # Apply branding tokens if provided
            if branding_tokens:
                css_parts.append(":root {")
                for token, value in branding_tokens.items():
                    css_parts.append(f"  --{token}: {value};")
                css_parts.append("}")

            return "\n".join(css_parts)

        except Theme.DoesNotExist:
            return ""


# Singleton instance
theme_service = ThemeService()
