"""
Django Theme System Models
Implements the theme architecture with versioning, packaging, and migration support
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import json
import hashlib
import re
import semver

User = get_user_model()


class Theme(models.Model):
    """Enhanced theme model with packaging and versioning support"""

    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    # Versioning (SemVer)
    version = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\d+\.\d+\.\d+(?:[-+][\w\d.]+)?$',
            message='Version must follow SemVer format (e.g., 1.2.3)'
        )]
    )

    # Compatibility
    engine_min_version = models.CharField(
        max_length=20,
        help_text=_("Minimum shop platform version required"),
        validators=[RegexValidator(
            regex=r'^\d+\.\d+\.\d+$',
            message='Version must be in format X.Y.Z'
        )]
    )
    engine_max_version = models.CharField(
        max_length=20,
        blank=True,
        help_text=_("Maximum compatible shop platform version"),
        validators=[RegexValidator(
            regex=r'^\d+\.\d+\.\d+$|^\d+\.x$',
            message='Version must be in format X.Y.Z or X.x'
        )]
    )

    # Authorship and licensing
    author = models.CharField(max_length=200)
    author_email = models.EmailField(blank=True)
    author_website = models.URLField(blank=True)
    license = models.CharField(
        max_length=100,
        default='Proprietary',
        help_text=_("e.g., MIT, GPL-3.0, Proprietary")
    )

    # Manifest and configuration
    manifest = models.JSONField(
        default=dict,
        help_text=_("Complete theme manifest including tokens, templates, widgets")
    )
    feature_flags = models.JSONField(
        default=list,
        help_text=_("List of required feature flags")
    )

    # Token migrations for version upgrades
    token_migrations = models.JSONField(
        default=list,
        help_text=_("Token rename/migration rules for upgrades")
    )

    # File storage
    package_file = models.FileField(
        upload_to='themes/packages/',
        validators=[FileExtensionValidator(allowed_extensions=['zip'])],
        help_text=_("Theme package ZIP file")
    )
    package_checksum = models.CharField(
        max_length=64,
        editable=False,
        help_text=_("SHA256 checksum of package file")
    )
    extracted_path = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Path where theme assets are extracted")
    )

    # Database-served CSS (survives platform updates)
    compiled_css = models.TextField(
        blank=True,
        help_text=_("Compiled theme CSS (tokens.css + reset.css + components.css + theme.css)")
    )
    css_hash = models.CharField(
        max_length=32,
        blank=True,
        editable=False,
        help_text=_("MD5 hash for cache busting")
    )

    # Preview assets
    preview_images = models.JSONField(
        default=list,
        help_text=_("List of preview image paths")
    )

    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_marketplace = models.BooleanField(
        default=False,
        help_text=_("Whether this theme is from the marketplace")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    installed_at = models.DateTimeField(null=True, blank=True)

    # Relations
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='themes_created'
    )

    class Meta:
        ordering = ['-created_at', 'name']
        unique_together = [['slug', 'version']]
        indexes = [
            models.Index(fields=['slug', '-version']),
            models.Index(fields=['is_active', 'is_default']),
        ]

    def __str__(self):
        return f"{self.name} v{self.version}"

    @property
    def css_url(self):
        """Get the URL for the theme's CSS file (property for template access)"""
        return self.get_css_url()

    def get_css_url(self):
        """Get URL for theme CSS - returns dynamic URL served from database."""
        # If we have compiled_css in database, return dynamic URL
        if self.compiled_css and self.css_hash:
            return f"/theme/css/theme/{self.slug}.css?v={self.css_hash}"

        # Fallback to static file URL for backward compatibility
        return self.get_extracted_css_url()

    @property
    def supports_dark_mode(self):
        """Check if this theme declares dark mode support in its manifest."""
        features = self.manifest.get('features', {})
        if isinstance(features, dict):
            return features.get('dark_mode', False)
        return False

    def save(self, *args, **kwargs):
        # Ensure only one default theme
        if self.is_default:
            Theme.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)

        # Calculate checksum if package file exists
        if self.package_file and not self.package_checksum:
            self.package_checksum = self.calculate_checksum()

        super().save(*args, **kwargs)

        # Auto-set force_light_mode based on theme's dark mode support
        if self.is_default:
            self._sync_force_light_mode()

        # Auto-extract theme files when theme is saved (especially for default themes)
        # This ensures CSS and assets are web-accessible
        if self.package_file and not self.extracted_path:
            self.extract_theme()

    def _sync_force_light_mode(self):
        """Auto-set force_light_mode when theme doesn't support dark mode.

        Prevents broken dark mode rendering for themes without dark tokens.
        """
        import logging
        logger = logging.getLogger(__name__)
        try:
            from design.models import GlobalDesignSettings
            settings = GlobalDesignSettings.get_settings()
            if not self.supports_dark_mode:
                # Theme has no dark mode support - force light to prevent broken rendering
                if not settings.force_light_mode:
                    settings.force_light_mode = True
                    settings.save(update_fields=['force_light_mode'])
                    logger.info(
                        f"Auto-enabled force_light_mode for theme '{self.name}' "
                        f"(dark_mode: false)"
                    )
            else:
                # Theme supports dark mode - allow user preference
                if settings.force_light_mode:
                    settings.force_light_mode = False
                    settings.save(update_fields=['force_light_mode'])
                    logger.info(
                        f"Auto-disabled force_light_mode for theme '{self.name}' "
                        f"(dark_mode: true)"
                    )
        except Exception as e:
            logger.warning(f"Could not sync force_light_mode for theme '{self.name}': {e}")

    def calculate_checksum(self):
        """Calculate SHA256 checksum of package file"""
        if not self.package_file:
            return ''

        sha256_hash = hashlib.sha256()
        for chunk in self.package_file.chunks():
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def verify_checksum(self):
        """Verify package file integrity"""
        return self.calculate_checksum() == self.package_checksum

    def is_compatible(self, platform_version):
        """Check if theme is compatible with platform version"""
        try:
            platform_ver = semver.VersionInfo.parse(platform_version)
            min_ver = semver.VersionInfo.parse(self.engine_min_version)

            if platform_ver < min_ver:
                return False

            if self.engine_max_version and not self.engine_max_version.endswith('.x'):
                max_ver = semver.VersionInfo.parse(self.engine_max_version)
                if platform_ver > max_ver:
                    return False

            return True
        except:
            return False


    def get_tokens(self):
        """Get theme design tokens"""
        return self.manifest.get('tokens', {})

    def get_templates(self):
        """Get available templates"""
        return self.manifest.get('templates', {})

    def get_widgets(self):
        """Get available widgets"""
        return self.manifest.get('widgets', [])

    def extract_theme(self):
        """
        Extract theme package to static directory using ThemeVersionManager.
        Handles both v1 (bundled CSS) and v2 (tokens-only) theme formats.
        Returns True if successful, False otherwise
        """
        if not self.package_file:
            return False

        import zipfile
        import os
        import tempfile
        import logging
        from django.conf import settings
        from pathlib import Path
        from .theme_version_manager import ThemeVersionManager

        logger = logging.getLogger(__name__)

        try:
            # Extract package to temp directory first
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = os.path.join(temp_dir, 'extracted')
                os.makedirs(temp_path, exist_ok=True)

                # Extract ZIP to temp
                with zipfile.ZipFile(self.package_file.path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)

                # Use ThemeVersionManager to install version
                result = ThemeVersionManager.install_theme_version(
                    self.slug,
                    self.version,
                    Path(temp_path)
                )

                if not result['success']:
                    logger.error(f"Failed to install theme version: {result.get('error')}")
                    return False

                # Activate the version (symlink only, don't change active_theme)
                activate_result = ThemeVersionManager.activate_theme_version(
                    self.slug,
                    self.version,
                    update_active_theme=False,
                )

                if not activate_result['success']:
                    logger.error(f"Failed to activate theme version: {activate_result.get('error')}")
                    return False

                # Update extracted_path to point to current symlink in components_data
                base_path = os.path.join(settings.BASE_DIR, 'components_data', 'static', 'design')
                extract_dir = os.path.join(base_path, 'themes', self.slug, 'current')

                self.extracted_path = extract_dir

                # Build compiled CSS — detect v1 vs v2 theme format
                theme_dir = Path(extract_dir) / 'theme'
                css_dir = theme_dir / 'css'
                tokens_css_path = css_dir / 'tokens.css'
                tokens_json_path = theme_dir / 'tokens.json'

                if tokens_css_path.exists():
                    # v1 theme: bundled CSS files
                    css_files = ['tokens.css', 'reset.css', 'components.css', 'theme.css']
                    combined_css = []
                    for css_file in css_files:
                        css_path = css_dir / css_file
                        if css_path.exists():
                            combined_css.append(f"/* {css_file} */\n{css_path.read_text()}")
                    self.compiled_css = '\n\n'.join(combined_css)
                else:
                    # v2 theme: auto-generate tokens.css, use platform CSS
                    combined_css = []
                    design_app_path = os.path.dirname(os.path.abspath(__file__))
                    platform_dir = Path(design_app_path) / 'static' / 'design' / 'platform'

                    # 1. Platform reset.css
                    platform_reset = platform_dir / 'reset.css'
                    if platform_reset.exists():
                        combined_css.append(f"/* reset.css */\n{platform_reset.read_text()}")

                    # 2. Auto-generate tokens.css from tokens.json
                    if tokens_json_path.exists():
                        try:
                            from design.services.token_css_generator import generate_tokens_css
                            tokens_css_content = generate_tokens_css(
                                tokens_json_path,
                                self.name,
                                dark_mode_enabled=self.supports_dark_mode,
                            )
                            combined_css.append(f"/* tokens.css (auto-generated) */\n{tokens_css_content}")
                        except Exception as e:
                            logger.error(f"Failed to generate tokens.css for {self.slug}: {e}")

                    # 3. Platform components.css
                    platform_components = platform_dir / 'components.css'
                    if platform_components.exists():
                        combined_css.append(f"/* components.css */\n{platform_components.read_text()}")

                    # 4. Theme overrides.css (optional)
                    overrides_path = theme_dir / 'overrides.css'
                    if overrides_path.exists():
                        overrides_content = overrides_path.read_text().strip()
                        if overrides_content:
                            combined_css.append(f"/* overrides.css */\n{overrides_content}")

                    self.compiled_css = '\n\n'.join(combined_css)

                # Strip relative @import statements (keep external font imports like Google Fonts)
                self.compiled_css = re.sub(
                    r'@import\s+url\([\'"]?(?!https?://)[^\'")\s]+[\'"]?\)\s*;?\s*\n?',
                    '',
                    self.compiled_css
                )

                self.css_hash = hashlib.md5(self.compiled_css.encode()).hexdigest()[:8]

                # Update all fields in one query
                Theme.objects.filter(pk=self.pk).update(
                    extracted_path=extract_dir,
                    compiled_css=self.compiled_css,
                    css_hash=self.css_hash
                )

                # Install header/footer presets if theme includes them
                presets_dir = theme_dir / 'presets'
                if presets_dir.is_dir():
                    try:
                        from design.services.theme_preset_installer import ThemePresetInstaller
                        preset_result = ThemePresetInstaller.install_presets(self.slug, presets_dir)
                        logger.info(
                            f"Installed presets for {self.slug}: "
                            f"{preset_result['headers_created']} headers, "
                            f"{preset_result['footers_created']} footers"
                        )
                    except Exception as e:
                        logger.error(f"Failed to install presets for {self.slug}: {e}")

                return True

        except Exception as e:
            logger.error(f"Failed to extract theme {self.slug}: {e}")
            return False

    def get_extracted_css_url(self):
        """Get URL to extracted CSS file"""
        from django.conf import settings

        if not self.extracted_path:
            # Try to extract if not already done
            if self.extract_theme():
                pass  # extracted_path is now set

        if self.extracted_path:
            # Theme extracted to design/static/design/themes/{slug}/current/
            # The 'current' symlink always points to the active version
            # URL is /static/design/themes/{slug}/current/theme/css/theme.css
            return f"{settings.STATIC_URL}design/themes/{self.slug}/current/theme/css/theme.css"

        return None

    def get_bundled_components(self):
        """
        Get all components bundled with this theme.

        Returns:
            QuerySet of ComponentStore instances that were bundled with this theme.
        """
        from .models import ComponentStore
        return ComponentStore.objects.filter(source_theme=self)

    @property
    def bundled_component_count(self):
        """
        Get count of bundled components.

        Returns:
            Integer count of components bundled with this theme.
        """
        return self.get_bundled_components().count()

    def get_bundled_component_info(self):
        """
        Get detailed information about bundled components.

        Returns:
            List of dictionaries with component details.
        """
        components = self.get_bundled_components()
        return [
            {
                'component_type': comp.component_type,
                'display_name': comp.display_name,
                'version': comp.version,
                'description': comp.description,
                'review_status': comp.review_status,
                'allowed_tiers': comp.allowed_tiers,
                'is_installed': True,  # By definition, if it's in ComponentStore, it's installed
            }
            for comp in components
        ]


class ThemeInstallation(models.Model):
    """Track theme installations per site/merchant"""

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    # Installation details
    installed_at = models.DateTimeField(auto_now_add=True)
    installed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Previous theme for rollback
    previous_theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_NULL,
        null=True,
        related_name='replaced_by'
    )

    # Customization state snapshot
    customization_snapshot = models.JSONField(
        default=dict,
        help_text=_("Snapshot of customizations before installation")
    )

    # Migration status
    migrations_applied = models.JSONField(
        default=list,
        help_text=_("List of applied token migrations")
    )

    class Meta:
        ordering = ['-installed_at']

    def __str__(self):
        return f"{self.theme.name} installed at {self.installed_at}"


class ThemeBranding(models.Model):
    """Merchant's brand customizations layered over theme"""

    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)

    # Brand tokens override theme tokens
    color_tokens = models.JSONField(default=dict)
    typography_tokens = models.JSONField(default=dict)
    spacing_tokens = models.JSONField(default=dict)
    border_tokens = models.JSONField(default=dict)
    shadow_tokens = models.JSONField(default=dict)
    animation_tokens = models.JSONField(default=dict)

    # Extended token categories
    transition_tokens = models.JSONField(default=dict)
    header_tokens = models.JSONField(default=dict)
    footer_tokens = models.JSONField(default=dict)
    menu_tokens = models.JSONField(default=dict)
    search_tokens = models.JSONField(default=dict)
    element_tokens = models.JSONField(default=dict)

    # Component overrides
    component_overrides = models.JSONField(
        default=dict,
        help_text=_("Per-component style overrides")
    )

    # Custom CSS (last resort)
    custom_css = models.TextField(
        blank=True,
        help_text=_("Custom CSS code (use sparingly)")
    )

    # Generated CSS cache
    generated_css = models.TextField(
        blank=True,
        editable=False,
        help_text=_("Compiled brand CSS")
    )
    css_hash = models.CharField(
        max_length=32,
        blank=True,
        editable=False,
        help_text=_("Hash for cache busting")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Theme Branding")
        verbose_name_plural = _("Theme Brandings")

    def __str__(self):
        if self.theme:
            return f"Branding for {self.theme.name}"
        return "Default Branding"

    # CSS prefix mapping for token fields
    # Maps field_name (without _tokens suffix) to CSS prefix
    # Add new token types here - no other code changes needed
    TOKEN_CSS_PREFIXES = {
        'color': 'theme-color',           # color_tokens → --theme-color-{key}
        'typography': 'theme',            # typography_tokens → --theme-{key}
        'spacing': 'theme-space',         # spacing_tokens → --theme-space-{key}
        'border': 'theme',                # border_tokens → --theme-{key}
        'shadow': 'theme-shadow',         # shadow_tokens → --theme-shadow-{key}
        'animation': 'theme-transition',  # animation_tokens → --theme-transition-{key}
        'transition': 'theme-transition', # transition_tokens → --theme-transition-{key}
        # Component tokens use theme-{name} pattern automatically
    }

    def generate_css(self):
        """Generate CSS from brand tokens with standardized --theme- prefixes.

        Token type prefixes are defined in TOKEN_CSS_PREFIXES.
        New token fields ending in _tokens are automatically discovered.
        Component tokens (header, footer, menu, etc.) use --theme-{component}-{key}.
        Element tokens use --theme-element-{category}-{key} with nested structure support.
        """
        css_parts = ["/* Brand Customizations */", ":root {"]

        # Dynamically discover and process all *_tokens fields
        for field in self._meta.get_fields():
            if not field.name.endswith('_tokens'):
                continue

            # Skip element_tokens - handled separately with nesting support
            if field.name == 'element_tokens':
                continue

            tokens = getattr(self, field.name, None) or {}
            if not tokens:
                continue

            # Determine CSS prefix from field name
            token_type = field.name.replace('_tokens', '')

            if token_type in self.TOKEN_CSS_PREFIXES:
                # Use explicit prefix mapping
                prefix = self.TOKEN_CSS_PREFIXES[token_type]
            else:
                # Default: component tokens use theme-{name} pattern
                prefix = f"theme-{token_type}"

            # Generate CSS variables
            for key, value in tokens.items():
                css_key = key.replace('_', '-')

                # Handle nested zones structure in header_tokens and footer_tokens
                if key == 'zones' and isinstance(value, dict):
                    css_parts.append(f"  /* {token_type.title()} Zone Tokens */")
                    for zone_name, zone_props in value.items():
                        zone_css_name = zone_name.replace('_', '-')
                        if isinstance(zone_props, dict):
                            for prop_key, prop_value in zone_props.items():
                                prop_css_key = prop_key.replace('_', '-')
                                css_var = f"--{prefix}-zones-{zone_css_name}-{prop_css_key}"
                                css_parts.append(f"  {css_var}: {prop_value};")
                else:
                    css_var = f"--{prefix}-{css_key}"
                    css_parts.append(f"  {css_var}: {value};")

        # Element tokens → --theme-element-{category}-{key}
        # Supports nested structure: elements.heading.h1-color → --theme-element-heading-h1-color
        if self.element_tokens:
            def flatten_elements(obj, prefix=''):
                """Recursively flatten nested element tokens to CSS variables."""
                result = []
                for key, value in obj.items():
                    css_key = key.replace('_', '-')
                    new_prefix = f"{prefix}-{css_key}" if prefix else css_key

                    if isinstance(value, dict):
                        # Nested object - recurse
                        result.extend(flatten_elements(value, new_prefix))
                    elif value:
                        # Leaf value - output CSS variable
                        result.append(f"  --theme-element-{new_prefix}: {value};")
                return result

            element_css = flatten_elements(self.element_tokens)
            if element_css:
                css_parts.append("  /* Element Tokens */")
                css_parts.extend(element_css)

        css_parts.append("}")

        # Generate corner-shape CSS rules for components
        # corner-shape can't use CSS variables, so we need actual CSS rules
        border_contexts = {}
        for key, value in (self.border_tokens or {}).items():
            if '-corner-shape' in key:
                context = key.replace('-corner-shape', '')
                border_contexts[context] = value

        # Map context names to actual selectors
        context_selectors = {
            'button': 'button, .button, [type="button"], [type="submit"], [type="reset"]',
            'input': 'input, textarea, select, .input',
            'card': '.card, .product-card, article',
            'modal': '.modal, .dialog, [role="dialog"]'
        }

        for context, corner_shape in border_contexts.items():
            if corner_shape and corner_shape != 'round':
                selectors = context_selectors.get(context, f'.{context}')
                css_parts.append(f"\n/* Corner shape for {context} */")
                css_parts.append(f"{selectors} {{")
                css_parts.append(f"  corner-shape: {corner_shape};")
                css_parts.append("}")

        # Add component overrides (supports responsive tokens)
        if self.component_overrides:
            # Check for component tokens (like 'menu') that should become CSS variables
            component_token_keys = ['menu']  # Components with token-based styling
            component_tokens_css = []
            responsive_media_queries = {}  # {min_width: [css_vars]}

            # Valid breakpoint names for responsive tokens
            valid_breakpoints = {
                'mobile': None,  # Base (no media query)
                'tablet': '768px',
                'desktop': '1024px',
                'sm': '640px',
                'md': '768px',
                'lg': '1024px',
                'xl': '1280px',
                '2xl': '1536px',
            }

            def is_responsive_value(val):
                """Check if value is a responsive object with breakpoint keys."""
                if not isinstance(val, dict):
                    return False
                return any(k in valid_breakpoints for k in val.keys())

            def get_base_value(responsive_val):
                """Get mobile-first base value from responsive object."""
                if 'mobile' in responsive_val:
                    return responsive_val['mobile']
                if 'sm' in responsive_val:
                    return responsive_val['sm']
                return list(responsive_val.values())[0]

            for key, value in self.component_overrides.items():
                if key in component_token_keys and isinstance(value, dict):
                    # Generate CSS variables for component tokens
                    # e.g., menu.text-color → --theme-menu-text-color
                    for token_name, token_value in value.items():
                        css_var = f"--theme-{key}-{token_name}"

                        if is_responsive_value(token_value):
                            # Responsive token - add base value and collect media query values
                            base_val = get_base_value(token_value)
                            component_tokens_css.append(f"  {css_var}: {base_val};")

                            # Collect responsive values for media queries
                            for breakpoint, bp_value in token_value.items():
                                if breakpoint in ('mobile', 'sm'):
                                    continue  # Base value, no media query needed
                                min_width = valid_breakpoints.get(breakpoint)
                                if min_width:
                                    if min_width not in responsive_media_queries:
                                        responsive_media_queries[min_width] = []
                                    responsive_media_queries[min_width].append(f"    {css_var}: {bp_value};")
                        else:
                            # Flat value
                            component_tokens_css.append(f"  {css_var}: {token_value};")
                elif isinstance(value, dict):
                    # Legacy: treat as CSS selector with styles
                    css_parts.append(f"\n{key} {{")
                    for prop, val in value.items():
                        css_parts.append(f"  {prop}: {val};")
                    css_parts.append("}")

            # Add component tokens to :root
            if component_tokens_css:
                css_parts.append("\n/* Component Tokens */")
                css_parts.append(":root {")
                css_parts.extend(component_tokens_css)
                css_parts.append("}")

            # Add responsive media queries
            if responsive_media_queries:
                css_parts.append("\n/* Responsive Component Tokens */")
                for min_width in sorted(responsive_media_queries.keys(), key=lambda x: int(x.replace('px', ''))):
                    vars_list = responsive_media_queries[min_width]
                    if vars_list:
                        css_parts.append(f"@media (min-width: {min_width}) {{")
                        css_parts.append("  :root {")
                        css_parts.extend(vars_list)
                        css_parts.append("  }")
                        css_parts.append("}")

        # Add custom CSS
        if self.custom_css:
            css_parts.append(f"\n/* Custom CSS */\n{self.custom_css}")

        self.generated_css = "\n".join(css_parts)
        self.css_hash = hashlib.md5(self.generated_css.encode()).hexdigest()[:8]
        self.save()

        return self.generated_css

    def get_css_url(self):
        """Get URL for generated brand CSS"""
        if not self.css_hash:
            self.generate_css()
        return f"/theme/css/brand.css?v={self.css_hash}"


class ThemeAsset(models.Model):
    """Individual theme assets (CSS, JS, images, fonts)"""

    ASSET_TYPES = [
        ('css', 'CSS'),
        ('js', 'JavaScript'),
        ('image', 'Image'),
        ('font', 'Font'),
        ('icon', 'Icon'),
        ('template', 'Template'),
    ]

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='assets')

    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    path = models.CharField(
        max_length=255,
        help_text=_("Relative path within theme")
    )
    file = models.FileField(upload_to='themes/assets/')

    # Metadata
    mime_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveIntegerField(default=0)
    checksum = models.CharField(max_length=64, blank=True)

    # For critical CSS
    is_critical = models.BooleanField(
        default=False,
        help_text=_("Whether this is critical CSS for initial render")
    )
    route = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Specific route for critical CSS (e.g., home, plp, pdp)")
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['theme', 'path']]
        ordering = ['asset_type', 'path']

    def __str__(self):
        return f"{self.theme.slug}/{self.path}"