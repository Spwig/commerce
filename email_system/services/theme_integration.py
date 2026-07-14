"""
Theme Integration Service
Generates CSS variables and template context from theme tokens for email templates.

Uses TokenResolver for proper 4-level cascade:
1. Brand Builder (priority 1) - Merchant customizations (highest priority)
2. Theme (priority 2) - Active theme tokens
3. Component (priority 3) - Component-specific tokens
4. System (priority 4) - Default system tokens (lowest priority)
"""

import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)


# Fallback defaults organized by category (from Starter theme)
# Used when no theme/branding is applied or tokens are missing
EMAIL_COLOR_DEFAULTS = {
    "primary": "#2563eb",
    "primary-hover": "#1d4ed8",
    "primary-light": "#dbeafe",
    "primary-dark": "#0b0b60",
    "secondary": "#64748b",
    "secondary-hover": "#475569",
    "accent": "#10b981",
    "text": "#1f2937",
    "text-light": "#374151",
    "text-muted": "#6b7280",
    "text-inverse": "#ffffff",
    "background": "#ffffff",
    "background-alt": "#f9fafb",
    "surface": "#ffffff",
    "surface-hover": "#f3f4f6",
    "border": "#e5e7eb",
    "border-light": "#f3f4f6",
    "success": "#10b981",
    "success-light": "#d1fae5",
    "warning": "#f59e0b",
    "warning-light": "#fef3c7",
    "error": "#ef4444",
    "error-light": "#fee2e2",
    "info": "#3b82f6",
    "info-light": "#dbeafe",
}

EMAIL_FONT_DEFAULTS = {
    "family-body": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    "family-heading": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    "sans": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "serif": "Georgia, 'Times New Roman', serif",
}

EMAIL_RADIUS_DEFAULTS = {
    "sm": "0.25rem",
    "md": "0.5rem",
    "lg": "0.75rem",
}

EMAIL_SPACE_DEFAULTS = {
    "2": "0.5rem",
    "4": "1rem",
    "6": "1.5rem",
    "8": "2rem",
}


class ThemeIntegrationService:
    """
    Integrates shop theme and branding into email templates.

    Provides two methods for theme integration:
    1. generate_theme_css() - Returns CSS variables string (legacy, for CSS injection)
    2. get_email_context() - Returns nested dict of resolved token values (new, for template context)

    The get_email_context() method uses TokenResolver for proper 4-level cascade,
    ensuring Brand Builder customizations take priority over theme defaults.
    """

    CACHE_KEY = "email_theme_css"
    CONTEXT_CACHE_KEY = "email_theme_context"
    CACHE_TIMEOUT = 300  # 5 minutes

    def generate_theme_css(self, force_refresh: bool = False) -> str:
        """
        Generate CSS with design variables for email templates

        Branding takes priority over theme:
        1. Check if custom branding exists → use branding
        2. Otherwise, use active theme
        3. Fall back to default values

        Args:
            force_refresh: Skip cache and regenerate

        Returns:
            CSS string with CSS variables
        """
        # Check cache first
        if not force_refresh:
            cached_css = cache.get(self.CACHE_KEY)
            if cached_css:
                logger.debug("Using cached theme CSS")
                return cached_css

        # Load branding (takes priority)
        branding = self._load_branding()

        # Load theme
        theme = self._load_theme()

        # Generate CSS variables
        css_vars = self._generate_css_variables(branding, theme)

        # Cache the result
        cache.set(self.CACHE_KEY, css_vars, self.CACHE_TIMEOUT)

        return css_vars

    def _load_branding(self) -> dict | None:
        """
        Load active theme branding configuration
        """
        try:
            from design.models import ThemeInstallation

            # Get active theme installation
            installation = (
                ThemeInstallation.objects.filter(is_active=True).select_related("branding").first()
            )

            if installation and installation.branding:
                branding = installation.branding
                return {
                    "colors": branding.colors_config or {},
                    "typography": branding.typography_config or {},
                    "spacing": branding.spacing_config or {},
                    "borders": branding.borders_config or {},
                    "logo_url": branding.logo.url if branding.logo else None,
                }

        except Exception as e:
            logger.warning(f"Could not load branding: {e}")

        return None

    def _load_theme(self) -> dict | None:
        """
        Load active theme configuration
        """
        try:
            from design.models import ThemeInstallation

            installation = (
                ThemeInstallation.objects.filter(is_active=True).select_related("theme").first()
            )

            if installation and installation.theme:
                theme = installation.theme
                return {
                    "colors": theme.colors or {},
                    "typography": theme.typography or {},
                    "spacing": theme.spacing or {},
                }

        except Exception as e:
            logger.warning(f"Could not load theme: {e}")

        return None

    def _generate_css_variables(self, branding: dict | None, theme: dict | None) -> str:
        """
        Generate CSS variables string

        Priority: branding > theme > defaults
        """
        # Default values (Spwig brand colors)
        defaults = {
            "primary_color": "#1a73e8",
            "secondary_color": "#34a853",
            "accent_color": "#fbbc04",
            "text_color": "#202124",
            "background_color": "#ffffff",
            "border_color": "#dadce0",
            "success_color": "#34a853",
            "warning_color": "#fbbc04",
            "error_color": "#ea4335",
            "font_family": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            "heading_font": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            "font_size_base": "16px",
            "font_size_small": "14px",
            "font_size_large": "18px",
            "line_height": "1.5",
            "border_radius": "8px",
            "spacing_small": "8px",
            "spacing_medium": "16px",
            "spacing_large": "24px",
        }

        # Merge with theme
        if theme:
            if theme.get("colors"):
                defaults["primary_color"] = theme["colors"].get(
                    "primary", defaults["primary_color"]
                )
                defaults["secondary_color"] = theme["colors"].get(
                    "secondary", defaults["secondary_color"]
                )
                defaults["text_color"] = theme["colors"].get("text", defaults["text_color"])
                defaults["background_color"] = theme["colors"].get(
                    "background", defaults["background_color"]
                )

            if theme.get("typography"):
                defaults["font_family"] = theme["typography"].get(
                    "body_font", defaults["font_family"]
                )
                defaults["heading_font"] = theme["typography"].get(
                    "heading_font", defaults["heading_font"]
                )
                defaults["font_size_base"] = theme["typography"].get(
                    "base_size", defaults["font_size_base"]
                )

        # Override with branding (highest priority)
        if branding:
            if branding.get("colors"):
                defaults["primary_color"] = branding["colors"].get(
                    "primary", defaults["primary_color"]
                )
                defaults["secondary_color"] = branding["colors"].get(
                    "secondary", defaults["secondary_color"]
                )
                defaults["accent_color"] = branding["colors"].get(
                    "accent", defaults["accent_color"]
                )

            if branding.get("typography"):
                defaults["font_family"] = branding["typography"].get(
                    "body_font", defaults["font_family"]
                )
                defaults["heading_font"] = branding["typography"].get(
                    "heading_font", defaults["heading_font"]
                )

            if branding.get("spacing"):
                defaults["spacing_small"] = branding["spacing"].get(
                    "small", defaults["spacing_small"]
                )
                defaults["spacing_medium"] = branding["spacing"].get(
                    "medium", defaults["spacing_medium"]
                )
                defaults["spacing_large"] = branding["spacing"].get(
                    "large", defaults["spacing_large"]
                )

        # Generate CSS string
        css_lines = []
        for key, value in defaults.items():
            css_var_name = key.replace("_", "-")
            css_lines.append(f"  --{css_var_name}: {value};")

        css = "/* Theme and Branding Variables */\n* {\n" + "\n".join(css_lines) + "\n}"

        logger.info("Generated theme CSS with variables")
        return css

    def clear_cache(self):
        """Clear cached theme CSS and context"""
        cache.delete(self.CACHE_KEY)
        cache.delete(self.CONTEXT_CACHE_KEY)
        logger.info("Cleared theme CSS and context cache")

    def get_email_context(self, force_refresh: bool = False) -> dict[str, dict[str, str]]:
        """
        Get resolved theme token values for email template context.

        Uses TokenResolver for proper 4-level cascade:
        1. Brand Builder - Merchant customizations (highest priority)
        2. Theme - Active theme tokens
        3. Component - Component-specific tokens
        4. System - Default system tokens (lowest priority)

        Args:
            force_refresh: Skip cache and regenerate

        Returns:
            Nested dict structure matching token naming for template access:
            {
                'color': {
                    'primary': '#2563eb',
                    'primary_hover': '#1d4ed8',
                    'text': '#1f2937',
                    'text_muted': '#6b7280',
                    'text_inverse': '#ffffff',
                    'background': '#ffffff',
                    'background_alt': '#f9fafb',
                    'surface': '#ffffff',
                    'border': '#e5e7eb',
                    'success': '#10b981',
                    'warning': '#f59e0b',
                    'error': '#ef4444',
                    'info': '#3b82f6',
                    ...
                },
                'font': {
                    'family_body': 'system-ui, ...',
                    'family_heading': 'system-ui, ...',
                },
                'radius': {
                    'sm': '0.25rem',
                    'md': '0.5rem',
                    'lg': '0.75rem',
                },
                'space': {
                    '2': '0.5rem',
                    '4': '1rem',
                    '6': '1.5rem',
                }
            }

        Template Usage:
            {{ theme.color.primary }}
            {{ theme.color.text_muted }}
            {{ theme.font.family_body }}
            {{ theme.radius.md }}
        """
        # Check cache first
        if not force_refresh:
            cached_context = cache.get(self.CONTEXT_CACHE_KEY)
            if cached_context:
                logger.debug("Using cached email theme context")
                return cached_context

        # Build nested context structure
        context = {
            "color": {},
            "font": {},
            "radius": {},
            "space": {},
        }

        try:
            from design.theme_utils import get_active_theme
            from design.token_resolver import get_token_resolver

            theme = get_active_theme()
            # Use tier 'C' (Marketing) which has full access to all tokens
            resolver = get_token_resolver(page_tier="C", theme=theme)

            # Resolve color tokens
            color_keys = [
                "primary",
                "primary-hover",
                "primary-light",
                "primary-dark",
                "secondary",
                "secondary-hover",
                "accent",
                "accent-hover",
                "text",
                "text-light",
                "text-muted",
                "text-inverse",
                "background",
                "background-alt",
                "surface",
                "surface-hover",
                "border",
                "border-light",
                "border-dark",
                "success",
                "success-light",
                "warning",
                "warning-light",
                "error",
                "error-light",
                "info",
                "info-light",
            ]
            for key in color_keys:
                token = resolver.resolve_token(f"theme-color-{key}")
                # Convert hyphens to underscores for Django template dot notation
                # e.g., 'primary-hover' -> 'primary_hover' -> {{ theme.color.primary_hover }}
                context_key = key.replace("-", "_")
                if token:
                    context["color"][context_key] = token.value
                else:
                    context["color"][context_key] = EMAIL_COLOR_DEFAULTS.get(key, "")

            # Resolve font tokens
            font_keys = ["family-body", "family-heading", "sans", "serif"]
            for key in font_keys:
                token = resolver.resolve_token(f"theme-font-{key}")
                # Convert hyphens to underscores for Django template dot notation
                context_key = key.replace("-", "_")
                if token:
                    context["font"][context_key] = token.value
                else:
                    context["font"][context_key] = EMAIL_FONT_DEFAULTS.get(key, "")

            # Resolve radius tokens
            radius_keys = ["sm", "md", "lg"]
            for key in radius_keys:
                token = resolver.resolve_token(f"theme-radius-{key}")
                if token:
                    context["radius"][key] = token.value
                else:
                    context["radius"][key] = EMAIL_RADIUS_DEFAULTS.get(key, "")

            # Resolve spacing tokens
            space_keys = ["2", "4", "6", "8"]
            for key in space_keys:
                token = resolver.resolve_token(f"theme-space-{key}")
                if token:
                    context["space"][key] = token.value
                else:
                    context["space"][key] = EMAIL_SPACE_DEFAULTS.get(key, "")

            logger.info("Generated email theme context from TokenResolver")

        except Exception as e:
            logger.warning(f"Could not load theme tokens via TokenResolver: {e}")
            # Fall back to defaults - convert hyphens to underscores for Django templates
            for key in EMAIL_COLOR_DEFAULTS:
                context_key = key.replace("-", "_")
                context["color"][context_key] = EMAIL_COLOR_DEFAULTS[key]
            for key in EMAIL_FONT_DEFAULTS:
                context_key = key.replace("-", "_")
                context["font"][context_key] = EMAIL_FONT_DEFAULTS[key]
            for key in EMAIL_RADIUS_DEFAULTS:
                context["radius"][key] = EMAIL_RADIUS_DEFAULTS[key]
            for key in EMAIL_SPACE_DEFAULTS:
                context["space"][key] = EMAIL_SPACE_DEFAULTS[key]
            logger.info("Using fallback defaults for email theme context")

        # Cache the result
        cache.set(self.CONTEXT_CACHE_KEY, context, self.CACHE_TIMEOUT)

        return context
