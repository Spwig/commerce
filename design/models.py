from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .header_footer_models import (  # noqa: F401
    FooterTemplate,
    HeaderTemplate,
    Menu,
    MenuItem,
    Widget,
    WidgetPlacement,
)

# Import theme + header/footer models — force-loads their submodules so
# their models register with Django's app registry regardless of admin
# autodiscover timing. Matches the pattern in social_sharing/models.py.
from .theme_models import (  # noqa: F401
    Theme,
    ThemeAsset,
    ThemeBranding,
    ThemeInstallation,
)

User = get_user_model()


class DesignToken(models.Model):
    """Design tokens for consistent styling with tier-aware priority cascade.

    Supports 4-level priority cascade for token resolution:
    1. Brand Builder (priority_level=1) - Merchant customizations (highest priority)
    2. Theme (priority_level=2) - Active theme tokens
    3. Component (priority_level=3) - Component-specific tokens
    4. System (priority_level=4) - Default system tokens (lowest priority)

    Tokens can be restricted to specific page tiers (A/B/C) for security.
    Lower priority_level number = higher precedence in cascade.

    Example:
        >>> # Create Brand Builder token (highest priority)
        >>> token = DesignToken.objects.create(
        ...     name='primary-color',
        ...     token_type='color',
        ...     value='#FF5733',
        ...     source='brand_builder',
        ...     priority_level=1,
        ...     tier_restriction=['A', 'B', 'C']
        ... )
        >>> token.is_available_in_tier('A')
        True
        >>> token.get_priority_name()
        'Brand Builder'
    """

    TOKEN_TYPES = [
        ("color", _("Color")),
        ("font", _("Font")),
        ("spacing", _("Spacing")),
        ("border", _("Border")),
        ("shadow", _("Shadow")),
        ("animation", _("Animation")),
        ("breakpoint", _("Breakpoint")),
    ]

    SOURCE_CHOICES = [
        ("brand_builder", _("Brand Builder")),
        ("theme", _("Theme")),
        ("component", _("Component")),
        ("system", _("System Default")),
    ]

    PRIORITY_CHOICES = [
        (1, _("Brand Builder (Highest)")),
        (2, _("Theme")),
        (3, _("Component")),
        (4, _("System Default (Lowest)")),
    ]

    # Basic token information
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Token Name"),
        help_text=_(
            "e.g., primary-500, text-lg, spacing-4. Same name can exist at different priority levels for cascade."
        ),
    )
    token_type = models.CharField(
        max_length=20,
        choices=TOKEN_TYPES,
        db_index=True,
        verbose_name=_("Token Type"),
        help_text=_("Category of design token"),
    )
    value = models.TextField(
        verbose_name=_("Token Value"), help_text=_("CSS value: #3B82F6, 1.125rem, 16px, etc.")
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Human-readable description of token purpose"),
    )

    # Priority cascade fields
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="system",
        db_index=True,
        verbose_name=_("Token Source"),
        help_text=_("Where this token comes from in the cascade"),
    )
    priority_level = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=4,
        db_index=True,
        verbose_name=_("Priority Level"),
        help_text=_("Lower number = higher priority. 1=Brand Builder (highest), 4=System (lowest)"),
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="design_tokens",
        verbose_name=_("Theme"),
        help_text=_("Associated theme (only for theme-level tokens)"),
    )
    component = models.ForeignKey(
        "ComponentStore",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="design_tokens",
        verbose_name=_("Component"),
        help_text=_("Associated component (only for component-level tokens)"),
    )

    # Tier restrictions
    tier_restriction = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Tier Restrictions"),
        help_text=_(
            "List of tiers where this token is available. Empty = all tiers. Options: ['A', 'B', 'C']"
        ),
    )

    # Status and metadata
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this token is currently active"),
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_("Is Locked"),
        help_text=_("Locked tokens cannot be renamed. Theme tokens are locked by default."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "design_design_token"
        ordering = ["priority_level", "token_type", "name"]
        verbose_name = _("Design Token")
        verbose_name_plural = _("Design Tokens")
        constraints = [
            # For brand_builder and system tokens: name + source must be unique
            models.UniqueConstraint(
                fields=["name", "source"],
                condition=Q(source__in=["brand_builder", "system"]),
                name="unique_global_token",
            ),
            # For theme tokens: name + source + theme must be unique
            models.UniqueConstraint(
                fields=["name", "source", "theme"],
                condition=Q(source="theme"),
                name="unique_theme_token",
            ),
            # For component tokens: name + source + component must be unique
            models.UniqueConstraint(
                fields=["name", "source", "component"],
                condition=Q(source="component"),
                name="unique_component_token",
            ),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["token_type"]),
            models.Index(fields=["source"]),
            models.Index(fields=["priority_level"]),
            models.Index(fields=["priority_level", "name"]),  # For cascade queries
        ]

    def __str__(self):
        return f"{self.name}: {self.value} ({self.get_source_display()})"

    def __repr__(self):
        return f"<DesignToken: {self.name} priority={self.priority_level} source={self.source}>"

    @property
    def css_custom_property(self):
        """Generate CSS custom property name."""
        return f"--{self.name.replace('_', '-')}"

    def is_available_in_tier(self, tier):
        """Check if token is available in specific tier.

        Args:
            tier: Tier identifier ('A', 'B', or 'C')

        Returns:
            bool: True if token is available in tier, False otherwise

        Example:
            >>> token.tier_restriction = ['A', 'B']
            >>> token.is_available_in_tier('A')
            True
            >>> token.is_available_in_tier('C')
            False
        """
        if not self.tier_restriction:  # Empty list = all tiers
            return True
        return tier in self.tier_restriction

    def get_priority_name(self):
        """Get human-readable priority level name.

        Returns:
            str: Priority level name (e.g., 'Brand Builder', 'Theme')

        Example:
            >>> token.priority_level = 1
            >>> token.get_priority_name()
            'Brand Builder'
        """
        return dict(self.SOURCE_CHOICES).get(self.source, _("Unknown"))

    def is_brand_builder(self):
        """Check if this is a Brand Builder token (highest priority)."""
        return self.source == "brand_builder" and self.priority_level == 1

    def is_theme_token(self):
        """Check if this is a Theme token."""
        return self.source == "theme" and self.priority_level == 2

    def is_component_token(self):
        """Check if this is a Component token."""
        return self.source == "component" and self.priority_level == 3

    def is_system_token(self):
        """Check if this is a System default token (lowest priority)."""
        return self.source == "system" and self.priority_level == 4


# ThemePreset model has been replaced by Theme model in theme_models.py
# Migration 0012_convert_themepreset_to_theme handles the data conversion
# This model is kept commented for reference during the transition period

# class ThemePreset(models.Model):
#     """Pre-built theme collections for quick setup"""
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#
#     # Theme configuration as JSON
#     color_scheme = models.JSONField(default=dict, help_text="Primary, secondary, accent colors")
#     typography = models.JSONField(default=dict, help_text="Font families, sizes, weights")
#     spacing = models.JSONField(default=dict, help_text="Margin, padding, gap values")
#     borders = models.JSONField(default=dict, help_text="Border radius, width values")
#     shadows = models.JSONField(default=dict, help_text="Box shadow configurations")
#
#     # Component-specific overrides
#     component_styles = models.JSONField(default=dict, help_text="Button, card, input styles")
#
#     is_default = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     preview_image = models.ImageField(upload_to='theme_previews/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         # Ensure only one default theme
#         if self.is_default:
#             ThemePreset.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
#         super().save(*args, **kwargs)


class ComponentStyle(models.Model):
    """Reusable component style configurations"""

    COMPONENT_TYPES = [
        ("button", "Button"),
        ("card", "Card"),
        ("form", "Form"),
        ("navigation", "Navigation"),
        ("product_grid", "Product Grid"),
        ("product_card", "Product Card"),
        ("category_display", "Category Display"),
        ("hero_section", "Hero Section"),
        ("footer", "Footer"),
        ("header", "Header"),
        ("sidebar", "Sidebar"),
        ("modal", "Modal"),
        ("gallery", "Gallery"),
    ]

    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=30, choices=COMPONENT_TYPES)

    # Style configuration
    css_classes = models.JSONField(default=dict, help_text="CSS class mappings")
    layout_config = models.JSONField(default=dict, help_text="Layout configuration")
    responsive_config = models.JSONField(default=dict, help_text="Mobile/tablet/desktop settings")

    # Custom CSS
    custom_css = models.TextField(blank=True, help_text="Additional CSS rules")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["component_type", "name"]
        unique_together = ["name", "component_type"]

    def __str__(self):
        return f"{self.component_type}: {self.name}"


class DesignMixin(models.Model):
    """Abstract base class for design-aware models"""

    TEMPLATE_VARIANTS = [
        ("default", "Default"),
        ("minimal", "Minimal"),
        ("detailed", "Detailed"),
        ("compact", "Compact"),
        ("featured", "Featured"),
        ("custom", "Custom"),
    ]

    # Template and layout
    template_variant = models.CharField(
        max_length=20,
        choices=TEMPLATE_VARIANTS,
        default="default",
        help_text="Choose how this content is displayed",
    )

    # CSS and styling
    css_classes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom CSS classes: {'container': 'my-container', 'title': 'my-title'}",
    )

    # Layout configuration
    layout_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Layout settings: grid columns, spacing, alignment, etc.",
    )

    # Theme and styling overrides
    style_overrides = models.JSONField(
        default=dict, blank=True, help_text="Override colors, fonts, spacing for this item"
    )

    # Responsive settings
    responsive_config = models.JSONField(
        default=dict, blank=True, help_text="Mobile/tablet/desktop specific settings"
    )

    # Theme inheritance
    inherit_parent_theme = models.BooleanField(
        default=True, help_text="Whether to inherit styling from parent category/theme"
    )

    class Meta:
        abstract = True

    def get_css_classes(self, element="container"):
        """Get CSS classes for a specific element"""
        return self.css_classes.get(element, "")

    def get_layout_setting(self, key, default=None):
        """Get a specific layout configuration value"""
        return self.layout_config.get(key, default)

    def get_style_override(self, property_name, default=None):
        """Get a style override value"""
        return self.style_overrides.get(property_name, default)

    def get_responsive_setting(self, breakpoint, key, default=None):
        """Get responsive setting for specific breakpoint"""
        breakpoint_config = self.responsive_config.get(breakpoint, {})
        return breakpoint_config.get(key, default)


class GlobalDesignSettings(models.Model):
    """Site-wide design configuration"""

    site_name = models.CharField(max_length=100, default="My Shop")

    # Active theme
    active_theme = models.ForeignKey(
        Theme, on_delete=models.SET_NULL, null=True, related_name="active_sites"
    )

    # Logo and branding
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)
    brand_colors = models.JSONField(default=dict, help_text="Primary brand colors")

    # Typography
    primary_font = models.CharField(
        max_length=100, default="Inter", help_text="Primary font family"
    )
    secondary_font = models.CharField(
        max_length=100, default="Roboto", help_text="Secondary font family"
    )

    # Layout defaults
    container_max_width = models.CharField(max_length=10, default="1200px")
    default_spacing = models.CharField(max_length=10, default="1rem")

    # Custom CSS
    global_css = models.TextField(blank=True, help_text="Global CSS rules applied site-wide")

    # Dark mode control
    force_light_mode = models.BooleanField(
        default=False,
        verbose_name=_("Force Light Mode"),
        help_text=_(
            "Force light mode (disable dark mode). When enabled, site always uses light theme colors even if user's browser prefers dark mode."
        ),
    )

    # SEO and meta
    default_meta_description = models.TextField(max_length=160, blank=True)
    default_og_image = models.ImageField(upload_to="meta/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Global Design Settings"
        verbose_name_plural = "Global Design Settings"

    def __str__(self):
        return f"Design Settings for {self.site_name}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and GlobalDesignSettings.objects.exists():
            raise ValueError("Only one GlobalDesignSettings instance is allowed")
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get the global design settings instance"""
        settings, created = cls.objects.get_or_create(pk=1, defaults={"site_name": "My Shop"})
        return settings


class CustomCSS(models.Model):
    """Admin-injectable custom CSS rules"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    css_code = models.TextField(help_text="CSS code to inject into pages")

    # Targeting options
    apply_to_pages = models.JSONField(
        default=list,
        blank=True,
        help_text="List of page types/URLs to apply this CSS to. Empty = all pages",
    )

    # Conditions
    is_active = models.BooleanField(default=True)
    load_order = models.PositiveIntegerField(default=100, help_text="Lower numbers load first")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["load_order", "name"]
        verbose_name = "Custom CSS"
        verbose_name_plural = "Custom CSS"

    def __str__(self):
        return self.name


class PageTier(models.Model):
    """Page type security tier configuration.

    Defines security tiers for different page types:
    - Tier A (System-Critical): Checkout, cart - strictest security
    - Tier B (Semi-Critical): Product, collection - controlled customization
    - Tier C (Marketing): Home, landing - full flexibility

    Each tier has specific CSP policies, script limits, and customization rules.

    Attributes:
        page_type: Unique identifier for page type (e.g., 'checkout', 'product')
        tier: Security tier classification (A/B/C)
        display_name: Human-readable name for admin interface
        description: Detailed explanation of page type purpose
        schema: JSON schema defining page structure and allowed regions
        csp_policy: Content Security Policy rules for this tier
        max_external_scripts: Maximum number of external scripts allowed
        allows_custom_html: Whether custom HTML injection is permitted
        locked_regions: List of regions that cannot be modified

    Example:
        >>> checkout = PageTier.objects.get(page_type='checkout')
        >>> checkout.tier
        'A'
        >>> checkout.max_external_scripts
        0
    """

    TIER_CHOICES = [
        ("A", "System-Critical (Checkout)"),
        ("B", "Semi-Critical (Product/Collection)"),
        ("C", "Marketing (Full Flexibility)"),
    ]

    page_type = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique page type identifier (e.g., 'checkout', 'product', 'home')",
    )
    tier = models.CharField(
        max_length=1,
        choices=TIER_CHOICES,
        db_index=True,
        help_text="Security tier: A (strictest), B (moderate), C (flexible)",
    )
    display_name = models.CharField(
        max_length=100, help_text="Human-readable name for admin interface"
    )
    description = models.TextField(
        blank=True, help_text="Detailed description of page type and its purpose"
    )
    schema = models.JSONField(
        default=dict, help_text="Page structure schema defining regions and allowed components"
    )
    csp_policy = models.JSONField(
        default=dict, help_text="Content Security Policy rules for this tier"
    )
    max_external_scripts = models.IntegerField(
        default=0, help_text="Maximum number of external scripts allowed (-1 for unlimited)"
    )
    allows_custom_html = models.BooleanField(
        default=False, help_text="Whether custom HTML injection is permitted"
    )
    locked_regions = models.JSONField(
        default=list, help_text="List of region IDs that cannot be modified by themes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "design_page_tier"
        ordering = ["tier", "page_type"]
        verbose_name = "Page Tier"
        verbose_name_plural = "Page Tiers"
        indexes = [
            models.Index(fields=["page_type"]),
            models.Index(fields=["tier"]),
        ]

    def __str__(self):
        return f"{self.display_name} (Tier {self.tier})"

    def __repr__(self):
        return f"<PageTier: {self.page_type} - Tier {self.tier}>"

    def is_tier_a(self):
        """Check if this is a Tier A (system-critical) page."""
        return self.tier == "A"

    def is_tier_b(self):
        """Check if this is a Tier B (semi-critical) page."""
        return self.tier == "B"

    def is_tier_c(self):
        """Check if this is a Tier C (marketing) page."""
        return self.tier == "C"

    def get_security_level(self):
        """Get human-readable security level description."""
        return dict(self.TIER_CHOICES).get(self.tier, "Unknown")


class ComponentStore(models.Model):
    """Central registry for reviewed and signed components.

    All theme components must be registered, reviewed, and signed before
    they can be used. This provides security and quality control.

    Attributes:
        component_type: Unique identifier (e.g., 'checkout_header', 'product_card')
        display_name: Human-readable name for admin
        version: Semantic version (1.0.0)
        author: Component author name
        capabilities: List of required capabilities
        allowed_tiers: List of tiers where component can be used
        render_mode: How component is rendered (SSR, CSR, island, static)
        external_domains: Whitelisted external domains for scripts/resources
        script_budget_kb: JavaScript size budget in KB
        requires_sandbox: Whether component needs iframe sandbox
        package_file: Component package file
        signature: Cryptographic signature for verification
        review_status: Approval status (pending, approved, rejected)

    Example:
        >>> component = ComponentStore.objects.get(component_type='product_card')
        >>> component.allowed_tiers
        ['B', 'C']
        >>> component.review_status
        'approved'
    """

    REVIEW_STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("reviewing", "Under Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("suspended", "Suspended"),
    ]

    RENDER_MODE_CHOICES = [
        ("ssr", "Server-Side Render"),
        ("csr", "Client-Side Render"),
        ("island", "Island (Selective Hydration)"),
        ("static", "Static HTML"),
    ]

    component_type = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique component identifier (e.g., 'checkout_header', 'product_card')",
    )
    display_name = models.CharField(max_length=200, help_text="Human-readable component name")
    description = models.TextField(
        blank=True, help_text="Detailed description of component functionality"
    )
    version = models.CharField(max_length=20, help_text="Semantic version (e.g., '1.0.0')")
    author = models.CharField(max_length=200, help_text="Component author name")

    # Capabilities and restrictions
    capabilities = models.JSONField(
        default=list, help_text="Required capabilities (e.g., ['custom_html', 'external_scripts'])"
    )
    allowed_tiers = models.JSONField(
        default=list, help_text="List of tiers where component can be used (e.g., ['B', 'C'])"
    )
    render_mode = models.CharField(
        max_length=20,
        choices=RENDER_MODE_CHOICES,
        default="ssr",
        help_text="How this component should be rendered",
    )

    # Security settings
    external_domains = models.JSONField(
        default=list, help_text="Whitelisted external domains for scripts/resources"
    )
    script_budget_kb = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, help_text="JavaScript size budget in KB"
    )
    requires_sandbox = models.BooleanField(
        default=False, help_text="Whether component requires iframe sandbox for security"
    )

    # Distribution
    package_file = models.FileField(
        upload_to="components/", help_text="Component package file (.zip)"
    )
    signature = models.TextField(
        blank=True, help_text="Cryptographic signature for package verification"
    )
    checksum_sha256 = models.CharField(
        max_length=64, blank=True, help_text="SHA-256 checksum of package file"
    )
    signed_by = models.CharField(
        max_length=200, blank=True, help_text="Signing authority (typically 'Spwig')"
    )
    signed_at = models.DateTimeField(
        null=True, blank=True, help_text="When component was cryptographically signed"
    )

    # Theme bundling
    source_theme = models.ForeignKey(
        "Theme",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bundled_components",
        help_text="Theme that bundled this component (if component came from a theme package)",
    )

    # Review workflow
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default="pending",
        db_index=True,
        help_text="Component approval status",
    )
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_components",
        help_text="User who reviewed this component",
    )
    reviewed_at = models.DateTimeField(
        null=True, blank=True, help_text="When component was reviewed"
    )
    review_notes = models.TextField(blank=True, help_text="Review notes and feedback")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "design_component_store"
        ordering = ["component_type"]
        verbose_name = "Component"
        verbose_name_plural = "Component Store"
        indexes = [
            models.Index(fields=["component_type"]),
            models.Index(fields=["review_status"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"{self.display_name} v{self.version}"

    def __repr__(self):
        return f"<ComponentStore: {self.component_type} v{self.version} ({self.review_status})>"

    def is_approved(self):
        """Check if component is approved for use."""
        return self.review_status == "approved"

    def can_use_in_tier(self, tier):
        """Check if component can be used in specific tier."""
        return tier in self.allowed_tiers

    def has_capability(self, capability):
        """Check if component requires specific capability."""
        return capability in self.capabilities

    def is_signed(self):
        """Check if component has been cryptographically signed."""
        return bool(self.signature and self.checksum_sha256)

    def verify_integrity(self):
        """
        Verify component signature and package integrity.

        Returns:
            Tuple of (is_valid: bool, message: str)

        Example:
            >>> component = ComponentStore.objects.get(component_type='hero_banner')
            >>> is_valid, message = component.verify_integrity()
            >>> if is_valid:
            ...     print("Component is authentic and unmodified")
        """
        from .component_signer import get_component_signer

        signer = get_component_signer()
        return signer.verify_component(self)

    def sign_package(self):
        """
        Sign the component package.

        Returns:
            Tuple of (success: bool, message: str)

        Note:
            This method updates signature and checksum_sha256 fields
            but does NOT save the model. Caller must call save().

        Example:
            >>> component = ComponentStore.objects.get(component_type='hero_banner')
            >>> success, message = component.sign_package()
            >>> if success:
            ...     component.save()
            ...     print("Component signed successfully")
        """
        from .component_signer import get_component_signer

        signer = get_component_signer()
        return signer.sign_component(self)


class TierComponentPermission(models.Model):
    """Component whitelisting per tier.

    Controls which components can be used in which page tiers,
    and any specific restrictions for that tier.

    Attributes:
        tier: PageTier this permission applies to
        component: ComponentStore component being whitelisted
        allowed_regions: Specific regions where component can be placed
        max_instances: Maximum number of instances allowed on page

    Example:
        >>> perm = TierComponentPermission.objects.get(
        ...     tier__page_type='checkout',
        ...     component__component_type='checkout_header'
        ... )
        >>> perm.max_instances
        1
    """

    tier = models.ForeignKey(
        PageTier,
        on_delete=models.CASCADE,
        related_name="component_permissions",
        verbose_name=_("Page Tier"),
        help_text=_("Page tier this permission applies to"),
    )
    component = models.ForeignKey(
        ComponentStore,
        on_delete=models.CASCADE,
        related_name="tier_permissions",
        verbose_name=_("Component"),
        help_text=_("Component being whitelisted"),
    )
    allowed_regions = models.JSONField(
        default=list,
        verbose_name=_("Allowed Regions"),
        help_text=_("Specific region IDs where component can be placed (empty = all regions)"),
    )
    max_instances = models.IntegerField(
        default=-1,
        verbose_name=_("Max Instances"),
        help_text=_("Maximum instances allowed on page (-1 = unlimited)"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "design_tier_component_permission"
        unique_together = ["tier", "component"]
        verbose_name = _("Tier Component Permission")
        verbose_name_plural = _("Tier Component Permissions")

    def __str__(self):
        return f"{self.component.component_type} allowed in Tier {self.tier.tier}"

    def __repr__(self):
        return (
            f"<TierComponentPermission: {self.component.component_type} in {self.tier.page_type}>"
        )

    def is_unlimited(self):
        """Check if unlimited instances are allowed."""
        return self.max_instances == -1

    def allows_region(self, region_id):
        """Check if component can be placed in specific region."""
        if not self.allowed_regions:  # Empty list = all regions
            return True
        return region_id in self.allowed_regions


class ComponentValidationReport(models.Model):
    """Validation report for component packages.

    Stores validation history showing when components were validated,
    what errors/warnings were found, and who performed the validation.

    This provides an audit trail for the component review process.

    Attributes:
        component: ComponentStore being validated
        validated_at: When validation was performed
        validated_by: User who triggered validation
        is_valid: Whether validation passed (no critical errors)
        errors: JSON list of critical errors found
        warnings: JSON list of warnings found
        version_validated: Component version at time of validation

    Example:
        >>> report = ComponentValidationReport.objects.filter(
        ...     component__component_type='hero_banner'
        ... ).latest('validated_at')
        >>> report.is_valid
        True
        >>> len(report.warnings)
        2
    """

    component = models.ForeignKey(
        ComponentStore,
        on_delete=models.CASCADE,
        related_name="validation_reports",
        verbose_name=_("Component"),
        help_text=_("Component that was validated"),
    )
    validated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Validated At"),
        help_text=_("When this validation was performed"),
    )
    validated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="component_validations",
        verbose_name=_("Validated By"),
        help_text=_("User who triggered this validation"),
    )
    is_valid = models.BooleanField(
        default=False,
        verbose_name=_("Is Valid"),
        help_text=_("Whether validation passed (no critical errors)"),
    )
    errors = models.JSONField(
        default=list, verbose_name=_("Errors"), help_text=_("Critical errors that must be fixed")
    )
    warnings = models.JSONField(
        default=list, verbose_name=_("Warnings"), help_text=_("Warnings that should be reviewed")
    )
    version_validated = models.CharField(
        max_length=20,
        verbose_name=_("Version Validated"),
        help_text=_("Component version at time of validation"),
    )

    class Meta:
        db_table = "design_component_validation_report"
        ordering = ["-validated_at"]
        verbose_name = _("Component Validation Report")
        verbose_name_plural = _("Component Validation Reports")
        indexes = [
            models.Index(fields=["component", "-validated_at"]),
            models.Index(fields=["is_valid"]),
        ]

    def __str__(self):
        status = "Valid" if self.is_valid else "Invalid"
        return f"{self.component} - {status} ({self.validated_at.strftime('%Y-%m-%d %H:%M')})"

    def __repr__(self):
        return f"<ComponentValidationReport: {self.component.component_type} v{self.version_validated} - {self.is_valid}>"

    def error_count(self):
        """Get number of errors."""
        return len(self.errors) if self.errors else 0

    def warning_count(self):
        """Get number of warnings."""
        return len(self.warnings) if self.warnings else 0

    def has_errors(self):
        """Check if validation found any errors."""
        return self.error_count() > 0

    def has_warnings(self):
        """Check if validation found any warnings."""
        return self.warning_count() > 0


class DevSession(models.Model):
    """Development session for Theme SDK connections.

    Tracks active theme development sessions from the Spwig Theme SDK CLI.
    Each session represents a developer actively working on a theme with
    live sync enabled.

    Attributes:
        token: Unique authentication token for this session
        user: Staff user who created the session
        theme_name: Name of theme being developed
        theme_path: Local path to theme directory (on developer's machine)
        is_active: Whether session is currently active
        last_sync: Last successful file sync
        created_at: When session was created
        expires_at: When session token expires

    Example:
        >>> session = DevSession.objects.create(
        ...     user=request.user,
        ...     theme_name='my-custom-theme',
        ...     theme_path='/Users/dev/themes/my-custom-theme'
        ... )
        >>> session.token
        'abc123...'
    """

    token = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="Unique authentication token for this dev session",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dev_sessions",
        help_text="Staff user who created this session",
    )
    theme_name = models.CharField(max_length=100, help_text="Name of theme being developed")
    theme_path = models.CharField(
        max_length=500, blank=True, help_text="Local path to theme on developer's machine"
    )

    # Session state
    is_active = models.BooleanField(
        default=True, db_index=True, help_text="Whether session is currently active"
    )
    last_sync = models.DateTimeField(null=True, blank=True, help_text="Last successful file sync")
    last_activity = models.DateTimeField(auto_now=True, help_text="Last activity timestamp")

    # Sync state
    synced_files = models.JSONField(
        default=dict, blank=True, help_text="Map of synced files and their checksums"
    )

    # Session metadata
    client_info = models.JSONField(
        default=dict, blank=True, help_text="CLI version, OS, Node version, etc."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="When session token expires")

    class Meta:
        db_table = "design_dev_session"
        ordering = ["-created_at"]
        verbose_name = "Dev Session"
        verbose_name_plural = "Dev Sessions"
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["is_active", "-created_at"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"{self.theme_name} ({self.user.username}) - {status}"

    def __repr__(self):
        return f"<DevSession: {self.theme_name} by {self.user.username}>"

    def save(self, *args, **kwargs):
        # Generate token if not set
        if not self.token:
            import secrets

            self.token = secrets.token_hex(32)

        # Set expiry if not set (default 24 hours)
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)

        super().save(*args, **kwargs)

    def is_expired(self):
        """Check if session token has expired."""
        return timezone.now() > self.expires_at

    def is_valid(self):
        """Check if session is active and not expired."""
        return self.is_active and not self.is_expired()

    def refresh_expiry(self, hours=24):
        """Extend session expiry time."""
        self.expires_at = timezone.now() + timezone.timedelta(hours=hours)
        self.save(update_fields=["expires_at"])

    def deactivate(self):
        """Deactivate this session."""
        self.is_active = False
        self.save(update_fields=["is_active"])

    def update_sync(self, files_synced):
        """Update last sync time and synced files."""
        self.last_sync = timezone.now()
        self.synced_files.update(files_synced)
        self.save(update_fields=["last_sync", "synced_files", "last_activity"])


class PageTemplateConfig(models.Model):
    """Site-wide page template selections and configuration.

    Singleton model (like GlobalDesignSettings). Stores which checkout and
    product page template the merchant has chosen, plus per-template options
    stored as JSON.
    """

    BLOG_POST_TEMPLATE_CHOICES = [
        ("classic", _("Classic")),
        ("minimal", _("Minimal")),
        ("magazine", _("Magazine")),
        ("full_width", _("Full Width")),
    ]

    BLOG_LIST_TEMPLATE_CHOICES = [
        ("grid", _("Grid")),
        ("list", _("List")),
        ("magazine", _("Magazine")),
        ("minimal", _("Minimal")),
    ]

    CHECKOUT_TEMPLATE_CHOICES = [
        ("accordion", _("Accordion")),
        ("multi_step", _("Multi-Step")),
        ("single_page", _("Single Page")),
        ("express", _("Express")),
    ]

    PRODUCT_TEMPLATE_CHOICES = [
        ("classic", _("Classic")),
        ("full_width", _("Full Width")),
        ("gallery_focus", _("Gallery Focus")),
        ("digital", _("Digital")),
    ]

    CATEGORY_TEMPLATE_CHOICES = [
        ("grid", _("Grid")),
        ("list", _("List")),
        ("carousel", _("Carousel")),
        ("masonry", _("Masonry")),
        ("featured", _("Featured")),
        ("accordion", _("Accordion")),
    ]

    # Checkout template selection
    checkout_template = models.CharField(
        max_length=30,
        choices=CHECKOUT_TEMPLATE_CHOICES,
        default="accordion",
        verbose_name=_("Checkout Template"),
        help_text=_("The checkout page layout used for all customers."),
    )
    checkout_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Checkout Options"),
        help_text=_("Configuration options for the selected checkout template."),
    )
    checkout_trust_badges = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Checkout Trust Badges"),
        help_text=_("Configurable trust badges shown during checkout."),
    )

    # Product page template selection
    product_template = models.CharField(
        max_length=30,
        choices=PRODUCT_TEMPLATE_CHOICES,
        default="classic",
        verbose_name=_("Default Product Template"),
        help_text=_("The default product page layout. Individual products can override this."),
    )
    product_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Product Page Options"),
        help_text=_("Configuration options for the selected product template."),
    )
    product_trust_badges = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Product Trust Badges"),
        help_text=_("Trust badges shown on physical product pages."),
    )
    digital_trust_badges = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Digital Product Trust Badges"),
        help_text=_("Trust badges shown on digital product pages."),
    )

    # Category page template selection
    category_template = models.CharField(
        max_length=30,
        choices=CATEGORY_TEMPLATE_CHOICES,
        default="grid",
        verbose_name=_("Category Template"),
        help_text=_("The category page layout. Individual categories can override options."),
    )
    category_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Category Page Options"),
        help_text=_("Configuration options for the category page template."),
    )

    # Blog post template selection
    blog_post_template = models.CharField(
        max_length=30,
        choices=BLOG_POST_TEMPLATE_CHOICES,
        default="classic",
        verbose_name=_("Blog Post Template"),
        help_text=_("The default blog post detail layout. Individual posts can override this."),
    )
    blog_post_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Blog Post Options"),
        help_text=_("Configuration options for the blog post template."),
    )

    # Blog list template selection
    blog_list_template = models.CharField(
        max_length=30,
        choices=BLOG_LIST_TEMPLATE_CHOICES,
        default="grid",
        verbose_name=_("Blog List Template"),
        help_text=_("The blog listing page layout."),
    )
    blog_list_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Blog List Options"),
        help_text=_("Configuration options for the blog list template."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "design_page_template_config"
        verbose_name = _("Page Template Configuration")
        verbose_name_plural = _("Page Template Configuration")

    def __str__(self):
        return f"Template Config: Checkout={self.checkout_template}, Product={self.product_template}, Category={self.category_template}"

    def save(self, *args, **kwargs):
        # Enforce singleton
        if not self.pk and PageTemplateConfig.objects.exists():
            existing = PageTemplateConfig.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        """Get or create the singleton config instance."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
