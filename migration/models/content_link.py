"""
ContentLink Model
Tracks discovered links in imported HTML content that need rewriting
from old WordPress/WooCommerce URLs to new Spwig URLs.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ContentLink(models.Model):
    """
    A link discovered in imported HTML content that points to the old
    source platform and may need rewriting to a Spwig URL.

    Created by ContentLinkProcessor during post-import scanning.
    Reviewed by the merchant in the migration wizard Step 6.
    """

    job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.CASCADE,
        related_name="content_links",
        help_text=_("Parent migration job"),
    )

    # Source object containing the link
    SOURCE_TYPES = [
        ("product_full_desc", _("Product - Full Description")),
        ("product_short_desc", _("Product - Short Description")),
        ("blog_post_content", _("Blog Post - Content")),
        ("category_description", _("Category - Description")),
    ]
    source_type = models.CharField(
        max_length=50, choices=SOURCE_TYPES, help_text=_("Which content field contains this link")
    )

    # Concrete FK references (one will be set based on source_type)
    source_product = models.ForeignKey(
        "catalog.Product",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="discovered_links",
    )
    source_blog_post = models.ForeignKey(
        "blog.BlogPost",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="discovered_links",
    )
    source_category = models.ForeignKey(
        "catalog.Category",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="discovered_links",
    )

    # Cached title for display without DB joins
    source_title = models.CharField(
        max_length=300, blank=True, help_text=_("Title of the source object (for display)")
    )

    # The link itself
    original_url = models.CharField(
        max_length=2000, help_text=_("Original URL found in the HTML content")
    )
    anchor_text = models.CharField(
        max_length=500, blank=True, help_text=_("Visible link text (anchor text)")
    )

    # Auto-suggested replacement
    suggested_url = models.CharField(
        max_length=2000, blank=True, help_text=_("Auto-suggested replacement URL")
    )

    MATCH_TYPES = [
        ("permalink", _("Stored Permalink Match")),
        ("slug_exact", _("Exact Slug Match")),
        ("external_id", _("External ID Match")),
        ("path_pattern", _("URL Path Pattern Match")),
        ("slug_fallback", _("Slug Fallback Match")),
        ("none", _("No Match Found")),
    ]
    match_type = models.CharField(
        max_length=20,
        choices=MATCH_TYPES,
        default="none",
        help_text=_("How the suggested URL was matched"),
    )

    TARGET_TYPES = [
        ("product", _("Product")),
        ("category", _("Category")),
        ("blog_post", _("Blog Post")),
        ("blog_category", _("Blog Category")),
        ("collection", _("Collection")),
        ("page", _("Page")),
        ("unknown", _("Unknown")),
    ]
    target_type = models.CharField(
        max_length=20,
        choices=TARGET_TYPES,
        default="unknown",
        help_text=_("Type of Spwig object the URL was matched to"),
    )
    target_id = models.IntegerField(
        null=True, blank=True, help_text=_("ID of the matched Spwig object")
    )

    # Confidence score (0.0 - 1.0)
    confidence = models.FloatField(
        default=0.0, help_text=_("Match confidence: 0.0 (no match) to 1.0 (exact match)")
    )

    # Review status
    STATUS_CHOICES = [
        ("pending", _("Pending Review")),
        ("approved", _("Approved")),
        ("modified", _("Modified by Merchant")),
        ("skipped", _("Skipped")),
        ("applied", _("Applied")),
        ("failed", _("Apply Failed")),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # Merchant override URL
    final_url = models.CharField(
        max_length=2000,
        blank=True,
        help_text=_("URL manually entered by merchant (overrides suggested_url)"),
    )

    error_message = models.TextField(blank=True, help_text=_("Error message if apply failed"))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["source_type", "source_title", "original_url"]
        verbose_name = _("Content Link")
        verbose_name_plural = _("Content Links")
        indexes = [
            models.Index(fields=["job", "status"]),
            models.Index(fields=["job", "source_type"]),
            models.Index(fields=["original_url"]),
        ]

    def __str__(self):
        status_icon = {
            "pending": "⏳",
            "approved": "✅",
            "modified": "✏️",
            "skipped": "⏭️",
            "applied": "✅",
            "failed": "❌",
        }.get(self.status, "")
        return f"{status_icon} {self.original_url} → {self.get_effective_url() or '?'}"

    def get_effective_url(self):
        """Return the URL that will be applied (merchant override or auto-suggested)."""
        return self.final_url or self.suggested_url

    @property
    def confidence_percent(self):
        """Return confidence as a percentage."""
        return int(self.confidence * 100)

    @property
    def confidence_class(self):
        """Return a CSS class based on confidence level."""
        if self.confidence >= 0.85:
            return "high"
        elif self.confidence >= 0.5:
            return "medium"
        elif self.confidence > 0:
            return "low"
        return "none"

    @property
    def source_object(self):
        """Return the source object (Product, BlogPost, or Category)."""
        if self.source_product_id:
            return self.source_product
        elif self.source_blog_post_id:
            return self.source_blog_post
        elif self.source_category_id:
            return self.source_category
        return None

    @property
    def source_object_id(self):
        """Return the ID of the source object."""
        return self.source_product_id or self.source_blog_post_id or self.source_category_id
