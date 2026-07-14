"""
Models for header and footer builder with widget support
"""

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class HeaderTemplate(models.Model):
    """Header template with widget zones"""

    name = models.CharField(max_length=200, help_text=_("Internal name for this header"))
    slug = models.SlugField(unique=True, help_text=_("URL-friendly identifier"))
    description = models.TextField(blank=True)

    # Layout configuration - aligned with preset names
    layout_type = models.CharField(
        max_length=50,
        choices=[
            ("classic", _("Classic E-commerce")),
            ("boutique", _("Centered Boutique")),
            ("minimal", _("Minimal Startup")),
            ("mega", _("Mega Menu Store")),
            ("promotional", _("Promotional Marketing")),
            ("split", _("Split Navigation")),
            ("custom", _("Custom Layout")),
        ],
        default="classic",
    )

    # Sticky behavior
    is_sticky = models.BooleanField(
        default=False, help_text=_("Header sticks to top when scrolling")
    )
    sticky_offset = models.IntegerField(
        default=0, help_text=_("Pixels from top before sticky activates")
    )

    # Top bar (optional)
    has_top_bar = models.BooleanField(default=False)
    top_bar_content = models.JSONField(
        default=dict, blank=True, help_text=_("Top bar widget configuration")
    )

    # Notification zone (announcement bar above all other zones)
    enable_notification_zone = models.BooleanField(
        default=True, help_text=_("Show announcement bar above header zones")
    )
    notification_zone_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Notification zone display settings"),
        # Structure: {
        #   "display_mode": "scroll_horizontal",
        #   "scroll_speed": 20,
        #   "cycle_duration": 5,
        #   "dismissible": true,
        #   "pause_on_hover": true
        # }
    )

    # Zone overrides - stores ONLY merchant customizations that override theme CSS defaults
    # Theme CSS provides all base styling via .header-preset-{layout_type} classes
    zone_overrides = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Zone style overrides - only properties that differ from theme defaults"),
        # Structure: {
        #   "top-bar": {
        #     "background": "#custom-color",  // Only if merchant overrode this
        #     "height": 50,                   // Only if merchant changed from theme default
        #   }
        # }
        # Empty dict means use all theme defaults
    )

    # Zone layout configuration (which sub-zones exist per primary zone)
    zone_layouts = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Defines sub-zones for each primary zone"),
        # Structure: {
        #   "top-bar": ["left", "right"],
        #   "main-header": ["left", "center", "right"],
        #   "bottom-bar": ["full"]
        # }
    )

    # DEPRECATED: Old zones field (kept for migration)
    zones = models.JSONField(
        default=dict,
        help_text=_("DEPRECATED: Use primary_zones and zone_layouts instead"),
        blank=True,
    )

    # Responsive settings
    mobile_layout = models.CharField(
        max_length=50,
        choices=[
            ("hamburger", _("Hamburger Menu")),
            ("bottom_nav", _("Bottom Navigation")),
            ("slide_menu", _("Slide-out Menu")),
            ("fullscreen", _("Fullscreen Menu")),
        ],
        default="hamburger",
    )
    mobile_menu_position = models.CharField(
        max_length=10,
        choices=[
            ("left", _("Left")),
            ("right", _("Right")),
        ],
        default="right",
        help_text=_("Position of hamburger menu button on mobile"),
    )

    # Styling
    custom_css = models.TextField(blank=True)
    css_classes = models.CharField(max_length=200, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    # Preset system
    is_preset = models.BooleanField(
        default=False, help_text=_("Mark as a preset template that users can clone")
    )
    preset_category = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ("modern", _("Modern")),
            ("classic", _("Classic")),
            ("minimal", _("Minimal")),
            ("ecommerce", _("E-commerce")),
        ],
        help_text=_("Category for preset templates"),
    )
    preview_image = models.ImageField(
        upload_to="design/header_presets/",
        blank=True,
        null=True,
        help_text=_("Preview screenshot of this header template"),
    )
    source = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text='Source identifier (e.g., "theme:modern-dark", "platform")',
    )

    # Metadata
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_headers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Draft/Publish workflow
    draft_data = models.JSONField(
        default=dict, blank=True, help_text=_("Current draft state being edited in the builder")
    )
    published_data = models.JSONField(
        default=dict, blank=True, help_text=_("Published state shown on the frontend")
    )
    published_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the template was last published")
    )
    has_unpublished_changes = models.BooleanField(
        default=False, help_text=_("True if draft differs from published")
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_notification_zone_config(self):
        """Return notification zone config with defaults."""
        defaults = {
            "display_mode": "scroll_horizontal",
            "scroll_speed": 20,
            "cycle_duration": 5,
            "dismissible": True,
            "pause_on_hover": True,
        }
        config = self.notification_zone_config or {}
        return {**defaults, **config}

    def save(self, *args, **kwargs):
        # Ensure only one default
        if self.is_default:
            HeaderTemplate.objects.filter(is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )

        # Initialize zone_layouts if empty (defines structure, not styling)
        if not self.zone_layouts:
            self.zone_layouts = self.get_default_zone_layouts()

        # zone_overrides should remain empty by default - theme CSS handles styling

        super().save(*args, **kwargs)

    def get_default_zone_layouts(self):
        """Return default zone layouts based on layout_type.
        Defines the structural zones, not styling (styling comes from theme CSS).
        """
        layouts = {
            "classic": {"top-bar": ["left", "right"], "main-header": ["left", "center", "right"]},
            "boutique": {"top-bar": ["full"], "main-header": ["center"], "bottom-bar": ["full"]},
            "minimal": {"main-header": ["left", "right"]},
            "mega": {
                "top-bar": ["left", "right"],
                "main-header": ["left", "center", "right"],
                "mega-menu-bar": ["full"],
            },
            "promotional": {
                "top-bar": ["full"],
                "main-header": ["left", "center", "right"],
                "bottom-bar": ["full"],
            },
            "split": {"top-bar": ["left", "right"], "main-header": ["left", "center", "right"]},
            "custom": {"main-header": ["left", "center", "right"]},
        }
        return layouts.get(self.layout_type, layouts["classic"])

    def get_enabled_zones(self):
        """Return list of enabled primary zones for this layout_type.
        Used by frontend to know which zones to render.
        """
        zone_map = {
            "classic": ["top-bar", "main-header"],
            "boutique": ["top-bar", "main-header", "bottom-bar"],
            "minimal": ["main-header"],
            "mega": ["top-bar", "main-header", "mega-menu-bar"],
            "promotional": ["top-bar", "main-header", "bottom-bar"],
            "split": ["top-bar", "main-header"],
            "custom": ["main-header"],
        }
        return zone_map.get(self.layout_type, ["main-header"])

    def get_all_zones(self):
        """Get list of all zone names (primary_subzone format)"""
        zones = []
        for primary_zone, sub_zones in self.zone_layouts.items():
            for sub_zone in sub_zones:
                zones.append(f"{primary_zone}_{sub_zone}")
        return zones

    def get_zone_overrides(self, zone_name):
        """Get style overrides for a specific zone (merchant customizations only)"""
        return self.zone_overrides.get(zone_name, {})

    def set_zone_override(self, zone_name, property_name, value):
        """Set a single style override for a zone"""
        if zone_name not in self.zone_overrides:
            self.zone_overrides[zone_name] = {}
        self.zone_overrides[zone_name][property_name] = value
        self.save()

    def clear_zone_override(self, zone_name, property_name=None):
        """Clear override(s) to revert to theme defaults.
        If property_name is None, clears all overrides for the zone.
        """
        if zone_name in self.zone_overrides:
            if property_name:
                self.zone_overrides[zone_name].pop(property_name, None)
                # Remove zone dict if empty
                if not self.zone_overrides[zone_name]:
                    del self.zone_overrides[zone_name]
            else:
                del self.zone_overrides[zone_name]
            self.save()

    def publish(self, user=None):
        """Copy draft_data to published_data and sync to widget_placements"""
        self.published_data = self.draft_data.copy() if self.draft_data else {}
        self.published_at = timezone.now()
        self.has_unpublished_changes = False
        self.save()

        # Sync published_data to widget_placements for frontend rendering
        self._sync_widget_placements()

    def _sync_widget_placements(self):
        """Sync published_data zones to WidgetPlacement table for frontend rendering"""
        from django.db import transaction

        zones = self.published_data.get("zones", {})

        with transaction.atomic():
            # Get existing placements to preserve widget references
            existing_placements = {p.id: p for p in self.widget_placements.all()}

            # Track which placements we've updated
            updated_ids = set()

            for zone_name, widgets in zones.items():
                for idx, widget_data in enumerate(widgets):
                    placement_id = widget_data.get("id")
                    widget_id = widget_data.get("widget_id")

                    if placement_id and placement_id in existing_placements:
                        # Update existing placement
                        placement = existing_placements[placement_id]
                        placement.zone = zone_name
                        placement.order = idx
                        placement.override_config = widget_data.get("config", {})
                        placement.is_active = True
                        placement.save()
                        updated_ids.add(placement_id)
                    elif widget_id:
                        # Create new placement
                        try:
                            widget = Widget.objects.get(pk=widget_id)
                            WidgetPlacement.objects.create(
                                widget=widget,
                                header=self,
                                zone=zone_name,
                                order=idx,
                                override_config=widget_data.get("config", {}),
                                is_active=True,
                            )
                        except Widget.DoesNotExist:
                            pass

            # Deactivate placements that are no longer in published_data
            for placement_id, placement in existing_placements.items():
                if placement_id not in updated_ids:
                    placement.is_active = False
                    placement.save()

    def save_draft(self, data):
        """Save data as draft and mark as having unpublished changes"""
        self.draft_data = data
        self.has_unpublished_changes = True
        self.save()

    def discard_draft(self):
        """Revert draft_data back to published_data"""
        self.draft_data = self.published_data.copy() if self.published_data else {}
        self.has_unpublished_changes = False
        self.save()

    def get_live_data(self):
        """Get the published data for frontend rendering"""
        return self.published_data if self.published_data else self.draft_data

    def get_draft_data(self):
        """Get the draft data for builder editing"""
        return self.draft_data if self.draft_data else {}


class FooterTemplate(models.Model):
    """Footer template with widget zones"""

    name = models.CharField(max_length=200, help_text=_("Internal name for this footer"))
    slug = models.SlugField(unique=True, help_text=_("URL-friendly identifier"))
    description = models.TextField(blank=True)

    # Layout configuration
    layout_type = models.CharField(
        max_length=50,
        choices=[
            ("simple", _("Simple (Single Row)")),
            ("columns", _("Multi-Column")),
            ("stacked", _("Stacked Sections")),
            ("minimal", _("Minimal")),
            ("custom", _("Custom Layout")),
        ],
        default="columns",
    )

    # Column configuration (for multi-column layout)
    column_count = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text=_("Number of columns in footer"),
    )

    # Footer sections
    zones = models.JSONField(default=dict, help_text=_("Widget zones configuration"), blank=True)

    # Bottom bar (copyright, etc.)
    has_bottom_bar = models.BooleanField(default=True)
    bottom_bar_content = models.JSONField(
        default=dict, blank=True, help_text=_("Bottom bar widget configuration")
    )

    # Styling
    custom_css = models.TextField(blank=True)
    css_classes = models.CharField(max_length=200, blank=True)
    background_color = models.CharField(max_length=7, blank=True, help_text=_("Hex color code"))
    text_color = models.CharField(max_length=7, blank=True, help_text=_("Hex color code"))

    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    # Preset system
    is_preset = models.BooleanField(
        default=False, help_text=_("Mark as a preset template that users can clone")
    )
    preset_category = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ("modern", _("Modern")),
            ("classic", _("Classic")),
            ("minimal", _("Minimal")),
            ("ecommerce", _("E-commerce")),
        ],
        help_text=_("Category for preset templates"),
    )
    preview_image = models.ImageField(
        upload_to="design/footer_presets/",
        blank=True,
        null=True,
        help_text=_("Preview screenshot of this footer template"),
    )
    source = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text='Source identifier (e.g., "theme:modern-dark", "platform")',
    )

    # Metadata
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_footers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Draft/Publish workflow
    draft_data = models.JSONField(
        default=dict, blank=True, help_text=_("Current draft state being edited in the builder")
    )
    published_data = models.JSONField(
        default=dict, blank=True, help_text=_("Published state shown on the frontend")
    )
    published_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the template was last published")
    )
    has_unpublished_changes = models.BooleanField(
        default=False, help_text=_("True if draft differs from published")
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one default
        if self.is_default:
            FooterTemplate.objects.filter(is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )
        super().save(*args, **kwargs)

    def publish(self, user=None):
        """Copy draft_data to published_data and sync to widget_placements"""
        self.published_data = self.draft_data.copy() if self.draft_data else {}
        self.published_at = timezone.now()
        self.has_unpublished_changes = False
        self.save()

        # Sync published_data to widget_placements for frontend rendering
        self._sync_widget_placements()

    def _sync_widget_placements(self):
        """Sync published_data zones to WidgetPlacement table for frontend rendering"""
        from django.db import transaction

        zones = self.published_data.get("zones", {})

        with transaction.atomic():
            # Get existing placements to preserve widget references
            existing_placements = {p.id: p for p in self.widget_placements.all()}

            # Track which placements we've updated
            updated_ids = set()

            for zone_name, widgets in zones.items():
                for idx, widget_data in enumerate(widgets):
                    placement_id = widget_data.get("id")
                    widget_id = widget_data.get("widget_id")

                    if placement_id and placement_id in existing_placements:
                        # Update existing placement
                        placement = existing_placements[placement_id]
                        placement.zone = zone_name
                        placement.order = idx
                        placement.override_config = widget_data.get("config", {})
                        placement.is_active = True
                        placement.save()
                        updated_ids.add(placement_id)
                    elif widget_id:
                        # Create new placement
                        try:
                            widget = Widget.objects.get(pk=widget_id)
                            WidgetPlacement.objects.create(
                                widget=widget,
                                footer=self,
                                zone=zone_name,
                                order=idx,
                                override_config=widget_data.get("config", {}),
                                is_active=True,
                            )
                        except Widget.DoesNotExist:
                            pass

            # Deactivate placements that are no longer in published_data
            for placement_id, placement in existing_placements.items():
                if placement_id not in updated_ids:
                    placement.is_active = False
                    placement.save()

    def save_draft(self, data):
        """Save data as draft and mark as having unpublished changes"""
        self.draft_data = data
        self.has_unpublished_changes = True
        self.save()

    def discard_draft(self):
        """Revert draft_data back to published_data"""
        self.draft_data = self.published_data.copy() if self.published_data else {}
        self.has_unpublished_changes = False
        self.save()

    def get_live_data(self):
        """Get the published data for frontend rendering"""
        return self.published_data if self.published_data else self.draft_data

    def get_draft_data(self):
        """Get the draft data for builder editing"""
        return self.draft_data if self.draft_data else {}


class Widget(models.Model):
    """Reusable widget for headers and footers"""

    WIDGET_TYPES = [
        ("logo", _("Logo")),
        ("menu", _("Navigation Menu")),
        ("search", _("Search Bar")),
        ("cart", _("Mini Cart")),
        ("account", _("Account Menu")),
        ("language", _("Language Selector")),
        ("currency", _("Currency Selector")),
        ("social", _("Social Media Links")),
        ("newsletter", _("Newsletter Signup")),
        ("contact", _("Contact Information")),
        ("text", _("Text/HTML Block")),
        ("links", _("Link List")),
        ("payment", _("Payment Methods")),
        ("trust_badges", _("Trust Badges")),
        ("announcement", _("Announcement Bar")),
        ("loyalty_balance", _("Loyalty Points Balance")),
        ("loyalty_tier_badge", _("Loyalty Tier Badge")),
        ("site_variable", _("Site Variable")),
        ("custom", _("Custom Widget")),
    ]

    name = models.CharField(max_length=200, help_text=_("Widget name"))
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)

    # Configuration
    config = models.JSONField(default=dict, help_text=_("Widget configuration (varies by type)"))

    # Content (for text/custom widgets)
    content = models.TextField(blank=True, help_text=_("Widget content (HTML allowed)"))

    # Translations for widget config text by language code
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Translations for widget config text by language code"),
    )

    # Translatable config fields per widget type (simple top-level keys)
    TRANSLATABLE_CONFIG_FIELDS = {
        "newsletter": ["title", "description", "button_text", "placeholder"],
        "text": ["title"],
        "links": ["title"],
        "contact": ["title", "address", "hours"],
        "social": ["title"],
        "trust_badges": [],
        "cart": ["text"],
        "logo": ["tagline"],
        "search": ["placeholder"],
    }

    # Array fields that need indexed-key handling: "links.0.text", "badges.0.title"
    TRANSLATABLE_ARRAY_FIELDS = {
        "links": {"array_key": "links", "fields": ["text"]},
        "trust_badges": {"array_key": "badges", "fields": ["title", "description"]},
    }

    # Visibility rules
    show_on_mobile = models.BooleanField(default=True)
    show_on_tablet = models.BooleanField(default=True)
    show_on_desktop = models.BooleanField(default=True)

    # Advanced visibility
    visibility_rules = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Advanced visibility rules (pages, user groups, etc.)"),
    )

    # Styling
    custom_css = models.TextField(blank=True)
    css_classes = models.CharField(max_length=200, blank=True)

    # Cache settings
    cache_duration = models.IntegerField(
        default=300, help_text=_("Cache duration in seconds (0 = no cache)")
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["widget_type", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"

    def get_translated_config(self, language_code, base_config=None):
        """Overlay translated config values onto the given config dict."""
        config = (base_config or self.config or {}).copy()
        if not self.translations or not language_code:
            return config
        lang_data = self.translations.get(language_code)
        if not lang_data:
            return config
        for key, value in lang_data.items():
            if key.startswith("_"):
                continue
            if "." not in key:
                # Simple top-level config key
                if value:
                    config[key] = value
            else:
                # Indexed array field: "links.0.text" → config['links'][0]['text']
                parts = key.split(".")
                if len(parts) == 3:
                    array_key, idx_str, field = parts
                    try:
                        idx = int(idx_str)
                        if array_key in config and idx < len(config[array_key]):
                            config[array_key][idx][field] = value
                    except (ValueError, IndexError, TypeError):
                        pass
        return config

    def get_translated_content(self, language_code):
        """Get translated widget content (for text widgets)."""
        if not self.translations or not language_code:
            return self.content
        lang_data = self.translations.get(language_code, {})
        return lang_data.get("content", self.content)

    def get_template_path(self):
        """Get the template path for this widget type"""
        return f"design/widgets/{self.widget_type}.html"

    def get_css_url(self):
        """Get the CSS URL for this widget"""
        from django.conf import settings

        return f"{settings.STATIC_URL}design/css/widgets/{self.widget_type}.css"

    def get_js_url(self):
        """Get the JavaScript URL for this widget (if any)"""
        # Baked-in widgets don't have separate JS files
        return None

    def render(self, context=None):
        """Render the widget with given context"""
        from django.template.loader import render_to_string

        template_path = self.get_template_path()
        widget_context = {
            "widget": self,
            "config": self.config,
            "content": self.content,
        }

        # Populate menu_items for menu widgets
        if self.widget_type == "menu" and self.config.get("menu_id"):
            try:
                menu = Menu.objects.get(pk=self.config["menu_id"])
                widget_context["menu"] = menu
                widget_context["menu_items"] = menu.get_items()
            except Menu.DoesNotExist:
                widget_context["menu"] = None
                widget_context["menu_items"] = []

        if context:
            widget_context.update(context)

        try:
            return render_to_string(template_path, widget_context)
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Widget {self.name} render error: {e}")
            return f"<!-- Widget {self.name} could not be rendered -->"


class WidgetPlacement(models.Model):
    """Places widgets in specific zones of headers/footers"""

    # Widget reference
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name="placements")

    # Placement location (either header or footer)
    header = models.ForeignKey(
        HeaderTemplate,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="widget_placements",
    )
    footer = models.ForeignKey(
        FooterTemplate,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="widget_placements",
    )

    # Zone within the header/footer
    zone = models.CharField(
        max_length=50, help_text=_("Zone identifier (e.g., 'left', 'center', 'right', 'column_1')")
    )

    # Order within zone
    order = models.IntegerField(default=0, help_text=_("Order within the zone (lower = first)"))

    # Override settings
    override_config = models.JSONField(
        default=dict, blank=True, help_text=_("Override widget config for this placement")
    )

    # Status
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["zone", "order"]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(header__isnull=False, footer__isnull=True)
                    | models.Q(header__isnull=True, footer__isnull=False)
                ),
                name="placement_either_header_or_footer",
            )
        ]

    def __str__(self):
        location = self.header or self.footer
        return f"{self.widget.name} in {location} - {self.zone}"


class Menu(models.Model):
    """Navigation menu structure"""

    name = models.CharField(max_length=200, help_text=_("Menu name"))
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    # Menu location/purpose
    location = models.CharField(
        max_length=50,
        choices=[
            ("primary", _("Primary Navigation")),
            ("secondary", _("Secondary Navigation")),
            ("footer", _("Footer Menu")),
            ("mobile", _("Mobile Menu")),
            ("account", _("Account Menu")),
            ("custom", _("Custom Menu")),
        ],
        default="primary",
    )

    # Display settings
    display_type = models.CharField(
        max_length=50,
        choices=[
            ("horizontal", _("Horizontal")),
            ("vertical", _("Vertical")),
            ("dropdown", _("Dropdown")),
            ("mega", _("Mega Menu")),
            ("accordion", _("Accordion")),
        ],
        default="horizontal",
    )

    # Styling
    custom_css = models.TextField(blank=True)
    css_classes = models.CharField(max_length=200, blank=True)

    # Global styling for all menu items
    global_style = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Global styling configuration for all menu items"),
        # Structure: {
        #   "item_spacing": "16px",
        #   "font_family": "",
        #   "default_text_color": "#333",
        #   "default_hover_color": "#0066cc",
        #   "divider_color": "#e5e7eb",
        #   "dropdown_background": "#ffffff",
        #   "dropdown_shadow": "0 4px 6px rgba(0,0,0,0.1)"
        # }
    )

    # Mobile menu configuration
    mobile_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Mobile menu behavior configuration"),
        # Structure: {
        #   "breakpoint": 768,
        #   "display_mode": "hamburger" | "bottom_nav" | "slide",
        #   "animation": "slide_left" | "slide_right" | "fade",
        #   "show_back_button": true,
        #   "show_close_button": true
        # }
    )

    # Translations for menu name/description
    translations = models.JSONField(
        default=dict, blank=True, help_text=_("Translations for menu-level content")
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["location", "name"]
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        return f"{self.name} ({self.get_location_display()})"

    def get_items(self):
        """Get top-level menu items"""
        return self.items.filter(parent=None, is_active=True).order_by("order")

    def get_all_items_tree(self):
        """Get all items as a nested tree structure for the builder"""

        def build_tree(parent=None):
            items = self.items.filter(parent=parent).order_by("order")
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "url": item.url,
                    "resolved_url": item.get_resolved_url(),
                    "resolved_title": item.get_resolved_title(),
                    "item_type": item.item_type,
                    "target": item.target,
                    "icon": item.icon,
                    "badge_text": item.badge_text,
                    "badge_color": item.badge_color,
                    "style_config": item.style_config,
                    "widget_config": item.widget_config,
                    "visibility_rules": item.visibility_rules,
                    "css_classes": item.css_classes,
                    "is_active": item.is_active,
                    "children": build_tree(item),
                    "has_children": item.has_children(),
                }
                for item in items
            ]

        return build_tree()


class MenuItem(models.Model):
    """Individual menu item"""

    # Item type choices
    ITEM_TYPE_CHOICES = [
        ("link", _("Standard Link")),
        ("page", _("Page Link")),
        ("category", _("Category Link")),
        ("category_tree", _("Dynamic Categories")),
        ("custom_url", _("Custom URL")),
        ("divider", _("Divider")),
        ("header", _("Section Header")),
        ("widget", _("Widget Item")),
    ]

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    # Item type for different link sources
    item_type = models.CharField(
        max_length=30, choices=ITEM_TYPE_CHOICES, default="link", help_text=_("Type of menu item")
    )

    # Content
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Display title (auto-populated from reference if empty)"),
    )
    url = models.CharField(
        max_length=500, blank=True, help_text=_("URL or path (for link/custom_url types)")
    )

    # Dynamic link references
    page_reference = models.ForeignKey(
        "page_builder.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="menu_items",
        help_text=_("Page to link to (when item_type is 'page')"),
    )
    category_reference = models.ForeignKey(
        "catalog.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="menu_items",
        help_text=_("Category to link to (when item_type is 'category')"),
    )

    # Link target
    target = models.CharField(
        max_length=20,
        choices=[
            ("_self", _("Same Window")),
            ("_blank", _("New Window")),
        ],
        default="_self",
    )

    # Icon (optional) - FontAwesome class
    icon = models.CharField(
        max_length=100, blank=True, help_text=_("FontAwesome icon class (e.g., 'fas fa-home')")
    )

    # Badge (optional)
    badge_text = models.CharField(max_length=20, blank=True, help_text=_("e.g., 'NEW', 'SALE'"))
    badge_color = models.CharField(
        max_length=20, blank=True, help_text=_("Badge color (hex or CSS color name)")
    )

    # Styling configuration
    style_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Styling configuration for this menu item"),
        # Structure: {
        #   "text_color": "#333333",
        #   "hover_color": "#0066cc",
        #   "background": "",
        #   "hover_background": "",
        #   "font_weight": "normal",
        #   "font_size": "",
        #   "icon_color": "",
        #   "icon_size": "",
        #   "padding": "",
        #   "border_radius": ""
        # }
    )

    # Widget configuration (for widget items like login/logout, cart, account)
    widget_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Widget configuration (when item_type is 'widget')"),
        # Structure: {
        #   "widget_type": "login_toggle" | "cart_mini" | "account_dropdown" | "search" | "wishlist",
        #   "display_mode": "inline" | "dropdown",
        #   "show_count": true,
        #   "show_label": true
        # }
    )

    # Tree configuration (for category_tree items - auto-populating category menus)
    tree_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Configuration for dynamic category tree (when item_type is 'category_tree')"),
        # Structure: {
        #   "root_category_id": null,  // null means all top-level categories
        #   "max_depth": 3,            // How many levels deep to show
        #   "sort_by": "name",         // "name", "-name", "order", "product_count"
        #   "show_empty": true,        // Show categories with no products
        #   "show_product_count": false // Show product count next to category name
        # }
    )

    # Mega menu content (for mega menu items)
    mega_menu_content = models.JSONField(
        default=dict, blank=True, help_text=_("Configuration for mega menu layout")
    )

    # Visibility rules per item
    visibility_rules = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Visibility rules for this menu item"),
        # Structure: [
        #   {"type": "device", "value": ["mobile", "tablet"]},
        #   {"type": "user_status", "value": "logged_in"},
        #   {"type": "user_group", "value": ["wholesale", "vip"]}
        # ]
    )

    # Translations for title
    translations = models.JSONField(
        default=dict, blank=True, help_text=_("Translations for menu item title")
    )

    # Order and visibility
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # CSS
    css_classes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return self.get_resolved_title() or f"MenuItem {self.pk}"

    def get_resolved_url(self):
        """Get the actual URL based on item_type and references"""
        if self.item_type == "page" and self.page_reference:
            return self.page_reference.get_absolute_url()
        elif self.item_type == "category" and self.category_reference:
            return self.category_reference.get_absolute_url()
        elif self.item_type in ("divider", "header", "category_tree") or self.item_type == "widget":
            return "#"
        return self.url or "#"

    def get_category_tree_items(self):
        """
        Get the dynamic category tree for category_tree type items.
        Returns a list of category dicts with nested children.
        """
        if self.item_type != "category_tree":
            return []

        try:
            from catalog.models import Category
        except ImportError:
            return []

        config = self.tree_config or {}
        root_category_id = config.get("root_category_id")
        max_depth = config.get("max_depth", 3)
        sort_by = config.get("sort_by", "name")
        show_empty = config.get("show_empty", True)
        show_product_count = config.get("show_product_count", False)

        # Build sort order
        if sort_by == "-name":
            order_by = "-name"
        elif sort_by == "order":
            order_by = "order"
        elif sort_by == "product_count":
            order_by = "-product_count"
        else:
            order_by = "name"

        def build_tree(parent_category=None, current_depth=1):
            if current_depth > max_depth:
                return []

            # Get categories at this level
            if parent_category is None:
                if root_category_id:
                    # Start from a specific category's children
                    try:
                        root = Category.objects.get(pk=root_category_id)
                        categories = root.children.filter(is_active=True)
                    except Category.DoesNotExist:
                        categories = Category.objects.filter(parent=None, is_active=True)
                else:
                    # All top-level categories
                    categories = Category.objects.filter(parent=None, is_active=True)
            else:
                categories = parent_category.children.filter(is_active=True)

            # Filter empty categories if needed
            if not show_empty:
                categories = categories.annotate(
                    product_count=models.Count(
                        "products", filter=models.Q(products__is_active=True)
                    )
                ).filter(product_count__gt=0)

            # Apply sorting
            if sort_by == "product_count":
                categories = categories.annotate(
                    product_count=models.Count(
                        "products", filter=models.Q(products__is_active=True)
                    )
                ).order_by(order_by)
            else:
                categories = categories.order_by(order_by)

            result = []
            for cat in categories:
                item = {
                    "id": cat.id,
                    "name": cat.name,
                    "url": cat.get_absolute_url(),
                    "children": build_tree(cat, current_depth + 1)
                    if current_depth < max_depth
                    else [],
                }
                if show_product_count:
                    item["product_count"] = cat.products.filter(is_active=True).count()
                result.append(item)

            return result

        return build_tree()

    def get_resolved_title(self):
        """Get title from reference if not explicitly set"""
        if self.title:
            return self.title
        if self.item_type == "page" and self.page_reference:
            return self.page_reference.title
        elif self.item_type == "category" and self.category_reference:
            return self.category_reference.name
        elif self.item_type == "divider":
            return "---"
        return self.title or ""

    def get_children(self):
        """Get child menu items"""
        return self.children.filter(is_active=True).order_by("order")

    def has_children(self):
        """Check if this item has active children"""
        return self.children.filter(is_active=True).exists()

    def should_show_for_device(self, device_type):
        """Check if item should be shown for a specific device"""
        if not self.visibility_rules:
            return True
        for rule in self.visibility_rules:
            if rule.get("type") == "device":
                allowed_devices = rule.get("value", [])
                if allowed_devices and device_type not in allowed_devices:
                    return False
        return True

    def should_show_for_user(self, user):
        """Check if item should be shown for a specific user"""
        if not self.visibility_rules:
            return True
        for rule in self.visibility_rules:
            if rule.get("type") == "user_status":
                required_status = rule.get("value")
                if (
                    required_status == "logged_in"
                    and not user.is_authenticated
                    or required_status == "logged_out"
                    and user.is_authenticated
                ):
                    return False
        return True
