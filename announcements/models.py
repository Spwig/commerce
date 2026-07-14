from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


class Announcement(models.Model):
    """
    Merchant-managed announcements for display in header/footer widgets.
    Supports modal popups with images, direct links, and visibility rules.
    """

    LINK_TYPE_CHOICES = [
        ("none", _("No Link")),
        ("product", _("Product")),
        ("category", _("Category")),
        ("blog_post", _("Blog Post")),
        ("page", _("Page")),
        ("custom_url", _("Custom URL")),
    ]

    IMAGE_DISPLAY_CHOICES = [
        ("banner", _("Banner Image (above content)")),
        ("background", _("Background Image (with overlay)")),
    ]

    # Content fields - CKEditor 'announcement_basic' (bold, italic, fontColor)
    title = models.TextField(
        help_text=_("Announcement title - supports basic styling (bold, italic, color)")
    )
    body = models.TextField(blank=True, help_text=_("Optional detailed content for modal display"))

    # Image
    image = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        help_text=_("Optional image for modal display"),
    )
    image_display_mode = models.CharField(
        max_length=20,
        choices=IMAGE_DISPLAY_CHOICES,
        default="banner",
        help_text=_("How to display the image in the modal"),
    )
    image_overlay_opacity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.50,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_(
            "Overlay opacity when image is used as background (0 = transparent, 1 = opaque)"
        ),
    )

    # Link configuration
    link_type = models.CharField(
        max_length=20,
        choices=LINK_TYPE_CHOICES,
        default="none",
        help_text=_("Type of link for this announcement"),
    )
    product_reference = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        help_text=_("Product to link to"),
    )
    category_reference = models.ForeignKey(
        "catalog.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        help_text=_("Category to link to"),
    )
    blog_post_reference = models.ForeignKey(
        "blog.BlogPost",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        help_text=_("Blog post to link to"),
    )
    page_reference = models.ForeignKey(
        "page_builder.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        help_text=_("Page to link to"),
    )
    custom_url = models.CharField(
        max_length=500, blank=True, help_text=_("Custom URL for the link")
    )
    link_text = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text=_('Button text for modal link, e.g. "Shop Now"'),
    )

    # Display behavior
    show_modal = models.BooleanField(
        default=False,
        help_text=_(
            "If enabled, clicking the announcement opens a modal with full content. "
            "If disabled, clicking navigates directly to the link URL."
        ),
    )

    # Status & scheduling
    is_enabled = models.BooleanField(
        default=True, help_text=_("Enable or disable this announcement")
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Announcement will automatically stop displaying after this date/time. Leave blank for no expiry."
        ),
    )
    priority = models.IntegerField(
        default=0, help_text=_("Lower number = higher priority (displayed first)")
    )

    # Visibility rules (advanced conditional display)
    visibility_rules = models.ManyToManyField(
        "page_builder.RuleGroup",
        blank=True,
        related_name="announcements",
        help_text=_("Visibility rules for conditional display"),
    )

    # Translations (merchant content translation system)
    translations = models.JSONField(
        default=dict, blank=True, help_text=_("Translations for announcement content")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "-created_at"]
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")
        indexes = [
            models.Index(fields=["is_enabled", "priority", "expires_at"]),
        ]

    def __str__(self):
        return strip_tags(self.title)[:80]

    def is_expired(self):
        """Check if this announcement has expired."""
        if self.expires_at is None:
            return False
        return timezone.now() > self.expires_at

    def is_visible(self):
        """Check if this announcement should be displayed (enabled and not expired)."""
        return self.is_enabled and not self.is_expired()

    def get_resolved_url(self):
        """Resolve the link URL based on link_type and references."""
        if self.link_type == "product" and self.product_reference:
            return self.product_reference.get_absolute_url()
        elif self.link_type == "category" and self.category_reference:
            return self.category_reference.get_absolute_url()
        elif self.link_type == "blog_post" and self.blog_post_reference:
            return self.blog_post_reference.get_absolute_url()
        elif self.link_type == "page" and self.page_reference:
            return self.page_reference.get_absolute_url()
        elif self.link_type == "custom_url" and self.custom_url:
            return self.custom_url
        return None
