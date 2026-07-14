"""
Custom template loader for theme system
Allows dynamic loading of templates from theme packages
"""

import logging
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader
from django.utils._os import safe_join

logger = logging.getLogger(__name__)


class ThemeTemplateLoader(Loader):
    """
    Custom template loader that loads templates from active theme
    Priority order:
    1. Merchant overrides (from database or custom directory)
    2. Active theme templates
    3. Fallback to default Django templates
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.theme_root = Path(settings.STATIC_ROOT) / "themes"

    def get_theme(self):
        """Get the currently active theme"""
        from .theme_models import Theme

        # Cache the active theme for performance
        theme = cache.get("active_theme")
        if not theme:
            theme = Theme.objects.filter(is_active=True, is_default=True).first()
            if theme:
                cache.set("active_theme", theme, 300)  # Cache for 5 minutes
        return theme

    def get_dirs(self):
        """Get template directories for current theme"""
        dirs = []

        theme = self.get_theme()
        if theme and theme.extracted_path:
            # Add theme template directory
            theme_template_dir = Path(theme.extracted_path) / "templates"
            if theme_template_dir.exists():
                dirs.append(str(theme_template_dir))

        # Add merchant override directory if configured
        merchant_override_dir = getattr(settings, "THEME_OVERRIDE_DIR", None)
        if merchant_override_dir:
            override_path = Path(merchant_override_dir)
            if override_path.exists():
                dirs.insert(0, str(override_path))  # Merchant overrides have priority

        return dirs

    def get_template_sources(self, template_name):
        """
        Return possible absolute paths for a template name
        """
        for template_dir in self.get_dirs():
            try:
                name = safe_join(template_dir, template_name)
            except ValueError:
                # The joined path was located outside of template_dir
                pass
            else:
                yield Origin(
                    name=name,
                    template_name=template_name,
                    loader=self,
                )

    def get_contents(self, origin):
        """
        Return the template content from the origin
        """
        try:
            with open(origin.name, encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)

    def load_template_source(self, template_name, template_dirs=None):
        """
        Load template source from theme directory
        """
        tried = []

        for origin in self.get_template_sources(template_name):
            try:
                return self.get_contents(origin), origin.name
            except TemplateDoesNotExist:
                tried.append(origin.name)

        if tried:
            error_msg = f"Theme template {template_name} not found. Tried: {', '.join(tried)}"
        else:
            error_msg = f"No theme directories found for template {template_name}"

        raise TemplateDoesNotExist(error_msg)

    def reset(self):
        """Reset the template cache when theme changes"""
        cache.delete("active_theme")
        super().reset()


from django.template import Origin


class ThemeOrigin(Origin):
    """Custom Origin for theme templates"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_name = kwargs.get("theme_name")


class CachedThemeTemplateLoader(ThemeTemplateLoader):
    """
    Cached version of ThemeTemplateLoader
    Caches compiled templates for better performance
    """

    def __init__(self, engine):
        super().__init__(engine)
        self._cache = {}
        self._cache_key_prefix = "theme_template_"

    def cache_key(self, template_name):
        """Generate cache key for template"""
        theme = self.get_theme()
        theme_id = theme.id if theme else "default"
        return f"{self._cache_key_prefix}{theme_id}_{template_name}"

    def _is_dev_mode(self):
        """Check if theme dev mode is active (bypass caching)."""
        return getattr(settings, "DEBUG", False) and getattr(settings, "THEME_DEV_SERVER", {}).get(
            "ENABLED", False
        )

    def get_template(self, template_name, skip=None):
        """
        Get compiled template, using cache if available.

        In dev mode (DEBUG + THEME_DEV_SERVER enabled), caching is bypassed
        to allow hot reload of template changes from the SDK.
        """
        # Bypass cache in dev mode for hot reload support
        if self._is_dev_mode():
            return super().get_template(template_name, skip)

        key = self.cache_key(template_name)

        # Try memory cache first
        template = self._cache.get(key)
        if template:
            return template

        # Try Django cache
        template = cache.get(key)
        if template:
            self._cache[key] = template
            return template

        # Load and compile template
        template = super().get_template(template_name, skip)

        # Cache the compiled template
        self._cache[key] = template
        cache.set(key, template, 3600)  # Cache for 1 hour

        return template

    def reset(self):
        """Clear all caches when theme changes"""
        super().reset()
        self._cache.clear()

        # Clear Django cache
        theme = self.get_theme()
        if theme:
            cache.delete_pattern(f"{self._cache_key_prefix}{theme.id}_*")
        cache.delete_pattern(f"{self._cache_key_prefix}default_*")


class ThemeTemplateManager:
    """
    Manager class for theme template operations
    """

    def __init__(self):
        self.theme_root = Path(settings.STATIC_ROOT) / "themes"

    def list_theme_templates(self, theme):
        """List all templates available in a theme"""
        templates = []

        if theme and theme.extracted_path:
            template_dir = Path(theme.extracted_path) / "templates"
            if template_dir.exists():
                for template_file in template_dir.rglob("*.html"):
                    relative_path = template_file.relative_to(template_dir)
                    templates.append(str(relative_path))

        return templates

    def get_template_context(self, theme):
        """Get theme-specific context variables"""
        from .theme_models import ThemeBranding

        context = {
            "theme": theme,
            "theme_static_url": f"/static/themes/{theme.slug}/" if theme else None,
        }

        # Add branding tokens
        try:
            branding = ThemeBranding.objects.filter(theme=theme).first()
            if branding:
                context["brand_tokens"] = {
                    **branding.color_tokens,
                    **branding.typography_tokens,
                    **branding.spacing_tokens,
                    **branding.border_tokens,
                }
                context["brand_css_url"] = branding.get_css_url()
        except Exception:
            pass

        return context

    def override_template(self, template_name, content):
        """
        Save merchant template override
        Returns the path where override was saved
        """
        merchant_override_dir = getattr(settings, "THEME_OVERRIDE_DIR", None)
        if not merchant_override_dir:
            merchant_override_dir = Path(settings.BASE_DIR) / "theme_overrides"

        override_path = Path(merchant_override_dir) / template_name
        override_path.parent.mkdir(parents=True, exist_ok=True)

        with open(override_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Clear template cache
        from django.template.loader import engines

        for engine in engines.all():
            engine.engine.template_loaders[0].reset()

        return str(override_path)

    def get_template_inheritance_chain(self, template_name):
        """
        Get the inheritance chain for a template
        Shows which templates will be checked in order
        """
        chain = []

        # Check merchant overrides
        merchant_override_dir = getattr(settings, "THEME_OVERRIDE_DIR", None)
        if merchant_override_dir:
            override_path = Path(merchant_override_dir) / template_name
            if override_path.exists():
                chain.append(
                    {"source": "merchant_override", "path": str(override_path), "exists": True}
                )

        # Check theme templates
        from .theme_models import Theme

        theme = Theme.objects.filter(is_active=True, is_default=True).first()
        if theme and theme.extracted_path:
            theme_path = Path(theme.extracted_path) / "templates" / template_name
            chain.append(
                {
                    "source": f"theme_{theme.slug}",
                    "path": str(theme_path),
                    "exists": theme_path.exists(),
                }
            )

        # Check app templates
        for app_config in settings.INSTALLED_APPS:
            app_name = app_config.split(".")[-1]
            app_path = Path(settings.BASE_DIR) / app_name / "templates" / template_name
            if app_path.exists():
                chain.append({"source": f"app_{app_name}", "path": str(app_path), "exists": True})

        return chain


# Singleton instance
theme_template_manager = ThemeTemplateManager()


def theme_context_processor(request):
    """
    Context processor to add theme-related variables to all templates
    """
    from .theme_models import Theme, ThemeBranding

    context = {}

    # Get active theme
    theme = cache.get("active_theme_context")
    if not theme:
        theme = Theme.objects.filter(is_active=True, is_default=True).first()
        if theme:
            cache.set("active_theme_context", theme, 300)

    if theme:
        context["active_theme"] = theme
        context["theme_static_url"] = f"/static/themes/{theme.slug}/"

        # Add theme CSS URL
        if theme.get_css_url():
            context["theme_css_url"] = theme.get_css_url()

        # Add branding CSS URL
        try:
            branding = ThemeBranding.objects.first()
            if branding:
                context["brand_css_url"] = branding.get_css_url()
        except Exception:
            pass

    return context
