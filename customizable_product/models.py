import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class ProductDesignConfig(models.Model):
    """Master configuration linking a customizable product to its visual design editor."""

    EDITOR_MODE_CHOICES = [
        ("canvas", _("Canvas Editor")),
        ("simple", _("Simple Form")),
    ]

    product = models.OneToOneField(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="design_config",
        limit_choices_to={"product_type": "customizable"},
        verbose_name=_("Product"),
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Enable Visual Editor"),
        help_text=_("When enabled, customers see the visual design editor on the product page."),
    )
    editor_mode = models.CharField(
        max_length=20,
        choices=EDITOR_MODE_CHOICES,
        default="canvas",
        verbose_name=_("Editor Mode"),
        help_text=_(
            "Canvas: full visual editor with Fabric.js. Simple: traditional form fields only."
        ),
    )

    # Feature toggles
    allow_image_upload = models.BooleanField(
        default=True,
        verbose_name=_("Allow Image Upload"),
        help_text=_("Allow customers to upload their own images."),
    )
    allow_text = models.BooleanField(
        default=True,
        verbose_name=_("Allow Text"),
        help_text=_("Allow customers to add text elements."),
    )
    allow_clipart = models.BooleanField(
        default=True,
        verbose_name=_("Allow Clipart"),
        help_text=_("Allow customers to use clipart from the asset library."),
    )

    # Upload restrictions
    max_uploads_per_surface = models.IntegerField(
        default=5,
        verbose_name=_("Max Uploads Per Surface"),
        help_text=_("Maximum number of uploaded images allowed per design surface."),
    )
    max_upload_size_mb = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
        verbose_name=_("Max Upload Size (MB)"),
    )
    allowed_upload_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Allowed Upload Types"),
        help_text=_('File extensions allowed for upload. e.g. ["jpg", "png", "svg"]'),
    )

    # Pricing
    base_design_fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        blank=True,
        verbose_name=_("Base Design Fee"),
        help_text=_("Flat fee added when any customization is applied."),
    )
    per_surface_fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        blank=True,
        verbose_name=_("Per Surface Fee"),
        help_text=_("Additional fee for each design surface used beyond the first."),
    )
    per_upload_fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        blank=True,
        verbose_name=_("Per Upload Fee"),
        help_text=_("Fee charged for each customer-uploaded image."),
    )
    per_text_fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        blank=True,
        verbose_name=_("Per Text Fee"),
        help_text=_("Fee charged for each text element added."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Design Configuration")
        verbose_name_plural = _("Product Design Configurations")

    def __str__(self):
        return f"Design Config: {self.product.name}"


class ProductSurface(models.Model):
    """A designable area/face of a product (e.g., Front, Back, Left Sleeve)."""

    UNIT_CHOICES = [
        ("mm", _("Millimeters")),
        ("in", _("Inches")),
        ("px", _("Pixels")),
    ]

    design_config = models.ForeignKey(
        ProductDesignConfig,
        on_delete=models.CASCADE,
        related_name="surfaces",
        verbose_name=_("Design Configuration"),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Surface Name"),
        help_text=_('e.g. "Front", "Back", "Left Sleeve"'),
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name=_("Slug"),
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
    )

    # Mockup image
    mockup_image = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="surface_mockups",
        verbose_name=_("Mockup Image"),
        help_text=_("Product photo showing this surface/angle."),
    )

    # Physical design area dimensions
    dimension_unit = models.CharField(
        max_length=5,
        choices=UNIT_CHOICES,
        default="mm",
        verbose_name=_("Dimension Unit"),
    )
    width = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=200,
        verbose_name=_("Design Area Width"),
        help_text=_("Width of the printable/designable area."),
    )
    height = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=200,
        verbose_name=_("Design Area Height"),
        help_text=_("Height of the printable/designable area."),
    )

    # Position of design area on mockup image (percentage-based for responsive rendering)
    area_x_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=25,
        verbose_name=_("Zone X Position (%)"),
        help_text=_(
            "Horizontal position of design zone on the mockup image, as percentage from left."
        ),
    )
    area_y_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=15,
        verbose_name=_("Zone Y Position (%)"),
        help_text=_(
            "Vertical position of design zone on the mockup image, as percentage from top."
        ),
    )
    area_width_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50,
        verbose_name=_("Zone Width (%)"),
        help_text=_("Width of design zone on the mockup image, as percentage of image width."),
    )
    area_height_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=70,
        verbose_name=_("Zone Height (%)"),
        help_text=_("Height of design zone on the mockup image, as percentage of image height."),
    )

    # Print requirements
    min_dpi = models.IntegerField(
        default=150,
        verbose_name=_("Minimum DPI"),
        help_text=_("Minimum dots-per-inch for acceptable print quality."),
    )
    recommended_dpi = models.IntegerField(
        default=300,
        verbose_name=_("Recommended DPI"),
        help_text=_("Recommended dots-per-inch for optimal print quality."),
    )
    bleed_mm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_("Bleed (mm)"),
        help_text=_("Extra margin outside design area for printing bleed."),
    )

    # Color restrictions
    max_colors = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Max Colors"),
        help_text=_(
            "Maximum number of colors allowed (for screen printing). Leave blank for unlimited."
        ),
    )
    background_color = models.CharField(
        max_length=20,
        default="#ffffff",
        verbose_name=_("Background Color"),
        help_text=_("Default background color for the design canvas."),
    )

    # Per-surface feature overrides (None = inherit from ProductDesignConfig)
    allow_text = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Allow Text"),
        help_text=_("Override: allow text on this surface. Blank = inherit from config."),
    )
    allow_image_upload = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Allow Image Upload"),
        help_text=_("Override: allow image uploads on this surface. Blank = inherit from config."),
    )
    allow_clipart = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Allow Clipart"),
        help_text=_("Override: allow clipart on this surface. Blank = inherit from config."),
    )
    max_elements = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Max Design Elements"),
        help_text=_("Maximum total design elements on this surface. Blank = no limit."),
    )

    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Enabled"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Surface")
        verbose_name_plural = _("Product Surfaces")
        ordering = ["sort_order", "name"]
        unique_together = [("design_config", "slug")]

    def __str__(self):
        return f"{self.design_config.product.name} - {self.name}"

    def get_effective_allow_text(self):
        """Return resolved allow_text: surface override or config fallback."""
        if self.allow_text is not None:
            return self.allow_text
        return self.design_config.allow_text

    def get_effective_allow_image_upload(self):
        """Return resolved allow_image_upload: surface override or config fallback."""
        if self.allow_image_upload is not None:
            return self.allow_image_upload
        return self.design_config.allow_image_upload

    def get_effective_allow_clipart(self):
        """Return resolved allow_clipart: surface override or config fallback."""
        if self.allow_clipart is not None:
            return self.allow_clipart
        return self.design_config.allow_clipart


class DesignTemplate(models.Model):
    """Pre-made design template that merchants create for customers to start from."""

    design_config = models.ForeignKey(
        ProductDesignConfig,
        on_delete=models.CASCADE,
        related_name="templates",
        verbose_name=_("Design Configuration"),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Template Name"),
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_("Slug"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Category"),
        help_text=_('e.g. "Birthday", "Business", "Holiday"'),
    )

    # The template design data (Fabric.js canvas state per surface)
    design_data = models.JSONField(
        default=dict,
        verbose_name=_("Design Data"),
        help_text=_("Full Fabric.js canvas state for each surface."),
    )

    # Preview thumbnail
    thumbnail = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="template_thumbnails",
        verbose_name=_("Thumbnail"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Design Template")
        verbose_name_plural = _("Design Templates")
        ordering = ["sort_order", "name"]
        unique_together = [("design_config", "slug")]

    def __str__(self):
        return self.name


class DesignTemplateElement(models.Model):
    """Individual element within a design template, with lock controls."""

    ELEMENT_TYPE_CHOICES = [
        ("text", _("Text")),
        ("image", _("Image")),
        ("clipart", _("Clipart")),
    ]

    template = models.ForeignKey(
        DesignTemplate,
        on_delete=models.CASCADE,
        related_name="elements",
        verbose_name=_("Template"),
    )
    surface = models.ForeignKey(
        ProductSurface,
        on_delete=models.CASCADE,
        related_name="template_elements",
        verbose_name=_("Surface"),
    )
    element_type = models.CharField(
        max_length=20,
        choices=ELEMENT_TYPE_CHOICES,
        verbose_name=_("Element Type"),
    )

    # Element data (position, size, rotation, content - Fabric.js object properties)
    element_data = models.JSONField(
        default=dict,
        verbose_name=_("Element Data"),
        help_text=_("Fabric.js object properties (position, size, rotation, content)."),
    )

    # Lock controls - which properties customers cannot change
    is_locked_position = models.BooleanField(
        default=False,
        verbose_name=_("Lock Position"),
        help_text=_("Prevent customers from moving this element."),
    )
    is_locked_size = models.BooleanField(
        default=False,
        verbose_name=_("Lock Size"),
        help_text=_("Prevent customers from resizing this element."),
    )
    is_locked_content = models.BooleanField(
        default=False,
        verbose_name=_("Lock Content"),
        help_text=_("Prevent customers from editing text or replacing the image."),
    )
    is_locked_delete = models.BooleanField(
        default=False,
        verbose_name=_("Lock Delete"),
        help_text=_("Prevent customers from removing this element."),
    )
    is_locked_rotation = models.BooleanField(
        default=False,
        verbose_name=_("Lock Rotation"),
        help_text=_("Prevent customers from rotating this element."),
    )

    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
        help_text=_("Z-order for layering elements."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Design Template Element")
        verbose_name_plural = _("Design Template Elements")
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.template.name} - {self.get_element_type_display()} on {self.surface.name}"


class ClipartCategory(models.Model):
    """Category for organizing merchant-provided clipart assets."""

    name = models.CharField(
        max_length=100,
        verbose_name=_("Category Name"),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Slug"),
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Icon"),
        help_text=_("CSS icon class (e.g. Font Awesome class)."),
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Clipart Category")
        verbose_name_plural = _("Clipart Categories")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class ClipartAsset(models.Model):
    """Individual clipart/icon/graphic that merchants provide for customers."""

    SCOPE_CHOICES = [
        ("global", _("Available to All Products")),
        ("product", _("Specific Product Only")),
    ]

    category = models.ForeignKey(
        ClipartCategory,
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name=_("Category"),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
    )
    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="clipart_usages",
        verbose_name=_("Image Asset"),
        help_text=_("PNG or SVG file for the clipart."),
    )
    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default="global",
        verbose_name=_("Scope"),
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clipart_assets",
        verbose_name=_("Product"),
        help_text=_("Only set when scope is 'Specific Product Only'."),
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_('Searchable tags for this clipart. e.g. ["star", "decoration", "gold"]'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Clipart Asset")
        verbose_name_plural = _("Clipart Assets")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class CustomFont(models.Model):
    """Custom font uploaded by merchant for use in the design editor."""

    name = models.CharField(
        max_length=100,
        verbose_name=_("Font Name"),
        help_text=_("Display name shown in the font picker."),
    )
    family = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Font Family"),
        help_text=_("CSS font-family name used in the editor."),
    )

    # Font files (at least regular is required for custom fonts)
    regular = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name=_("Regular"),
        help_text=_("WOFF2 or TTF file for regular weight."),
    )
    bold = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name=_("Bold"),
        help_text=_("WOFF2 or TTF file for bold weight."),
    )
    italic = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name=_("Italic"),
        help_text=_("WOFF2 or TTF file for italic style."),
    )
    bold_italic = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name=_("Bold Italic"),
        help_text=_("WOFF2 or TTF file for bold italic style."),
    )

    is_system_font = models.BooleanField(
        default=False,
        verbose_name=_("System Font"),
        help_text=_("If true, this font is pre-installed and no file upload is needed."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Custom Font")
        verbose_name_plural = _("Custom Fonts")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class SavedDesign(models.Model):
    """Customer's saved design for later editing or reuse."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_designs",
        verbose_name=_("User"),
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="saved_designs",
        verbose_name=_("Product"),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Design Name"),
    )
    design_data = models.JSONField(
        default=dict,
        verbose_name=_("Design Data"),
        help_text=_("Full Fabric.js canvas state per surface."),
    )
    thumbnails = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Thumbnails"),
        help_text=_('Per-surface thumbnail MediaAsset IDs. e.g. {"front": 123, "back": 456}'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Saved Design")
        verbose_name_plural = _("Saved Designs")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.name} ({self.product.name})"


class DesignDraft(models.Model):
    """Temporary design storage during the cart/checkout flow."""

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("Token"),
        help_text=_("Unique reference used by the cart system."),
    )
    session_key = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_("Session Key"),
        help_text=_("Session key for anonymous users."),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="design_drafts",
        verbose_name=_("User"),
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="design_drafts",
        verbose_name=_("Product"),
    )
    design_data = models.JSONField(
        default=dict,
        verbose_name=_("Design Data"),
    )
    thumbnails = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Thumbnails"),
        help_text=_("Per-surface thumbnail MediaAsset IDs."),
    )
    pricing_breakdown = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Pricing Breakdown"),
        help_text=_("Calculated price components for this design."),
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
        help_text=_("Auto-cleanup after this datetime."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Design Draft")
        verbose_name_plural = _("Design Drafts")
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["session_key"]),
        ]

    def __str__(self):
        return f"Draft {self.token} ({self.product.name})"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)


class DesignSnapshot(models.Model):
    """Immutable snapshot of a design at the time of order placement for fulfillment."""

    order_item = models.OneToOneField(
        "orders.OrderItem",
        on_delete=models.CASCADE,
        related_name="design_snapshot",
        verbose_name=_("Order Item"),
    )
    design_data = models.JSONField(
        default=dict,
        verbose_name=_("Design Data"),
        help_text=_("Frozen design state at time of order."),
    )
    rendered_images = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Rendered Images"),
        help_text=_('Per-surface preview MediaAsset IDs. e.g. {"front": 123}'),
    )
    fulfillment_files = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Fulfillment Files"),
        help_text=_("High-resolution composite MediaAsset IDs for printing."),
    )
    is_rendered = models.BooleanField(
        default=False,
        verbose_name=_("Rendered"),
        help_text=_("Whether high-resolution fulfillment files have been generated."),
    )
    render_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Render Completed At"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Design Snapshot")
        verbose_name_plural = _("Design Snapshots")

    def __str__(self):
        return f"Snapshot for Order Item #{self.order_item_id}"
