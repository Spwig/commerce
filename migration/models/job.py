"""
MigrationJob Model
Tracks complete migration jobs from start to finish with transaction-based rollback support.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import uuid

User = get_user_model()


class MigrationJob(models.Model):
    """
    Tracks a complete migration job from start to finish.
    Supports transaction-based rollback.
    """
    # Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='migration_jobs',
        help_text=_("User who initiated this migration")
    )

    # Platform & Method
    PLATFORM_CHOICES = [
        ('woocommerce', _('WooCommerce')),
        ('shopify', _('Shopify')),
        ('magento', _('Magento')),
        ('csv', _('CSV Files')),
    ]
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        help_text=_("Source e-commerce platform")
    )

    METHOD_CHOICES = [
        ('api', _('REST API')),
        ('csv', _('CSV Upload')),
        ('database', _('Direct Database')),
    ]
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        help_text=_("Migration method used")
    )

    # Connection Configuration (encrypted JSON)
    # Example: {"store_url": "...", "consumer_key": "...", "consumer_secret": "..."}
    connection_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Connection configuration (API keys, URLs, etc.)")
    )

    # Migration Settings - What to Import
    import_products = models.BooleanField(default=True)
    import_categories = models.BooleanField(default=True)
    import_customers = models.BooleanField(default=True)
    import_orders = models.BooleanField(default=True)
    import_reviews = models.BooleanField(default=True)
    import_coupons = models.BooleanField(default=True)
    import_shipping_zones = models.BooleanField(default=False)
    import_tax_rates = models.BooleanField(default=False)
    import_blog = models.BooleanField(
        default=False,
        help_text=_("Import blog posts, categories, and tags from WordPress")
    )
    import_affiliates = models.BooleanField(
        default=False,
        help_text=_("Import affiliate data via Spwig Migration Bridge plugin")
    )

    # Status Tracking
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('connecting', _('Testing Connection')),
        ('previewing', _('Previewing Data')),
        ('running', _('Importing')),
        ('paused', _('Paused')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('rolling_back', _('Rolling Back')),
        ('rolled_back', _('Rolled Back')),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )

    # Transaction Control for Rollback
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Transaction ID for rollback tracking")
    )
    can_rollback = models.BooleanField(
        default=True,
        help_text=_("Whether this migration can be rolled back")
    )
    rollback_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Deadline for manual rollback (24 hours after completion)")
    )

    # Progress Tracking
    current_step = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Current import step being processed")
    )
    progress_percent = models.IntegerField(
        default=0,
        help_text=_("Overall progress percentage (0-100)")
    )

    # Statistics - Products
    products_total = models.IntegerField(default=0)
    products_imported = models.IntegerField(default=0)
    products_skipped = models.IntegerField(default=0)
    products_failed = models.IntegerField(default=0)

    # Statistics - Categories
    categories_total = models.IntegerField(default=0)
    categories_imported = models.IntegerField(default=0)
    categories_skipped = models.IntegerField(default=0)
    categories_failed = models.IntegerField(default=0)

    # Statistics - Customers
    customers_total = models.IntegerField(default=0)
    customers_imported = models.IntegerField(default=0)
    customers_skipped = models.IntegerField(default=0)
    customers_failed = models.IntegerField(default=0)

    # Statistics - Orders
    orders_total = models.IntegerField(default=0)
    orders_imported = models.IntegerField(default=0)
    orders_skipped = models.IntegerField(default=0)
    orders_failed = models.IntegerField(default=0)

    # Statistics - Reviews
    reviews_total = models.IntegerField(default=0)
    reviews_imported = models.IntegerField(default=0)
    reviews_skipped = models.IntegerField(default=0)
    reviews_failed = models.IntegerField(default=0)

    # Statistics - Coupons
    coupons_total = models.IntegerField(default=0)
    coupons_imported = models.IntegerField(default=0)
    coupons_skipped = models.IntegerField(default=0)
    coupons_failed = models.IntegerField(default=0)

    # Statistics - Product Variants
    variants_total = models.IntegerField(default=0)
    variants_imported = models.IntegerField(default=0)
    variants_skipped = models.IntegerField(default=0)
    variants_failed = models.IntegerField(default=0)

    # Statistics - Blog Posts
    blog_posts_total = models.IntegerField(default=0)
    blog_posts_imported = models.IntegerField(default=0)
    blog_posts_skipped = models.IntegerField(default=0)
    blog_posts_failed = models.IntegerField(default=0)

    # Statistics - Blog Categories
    blog_categories_total = models.IntegerField(default=0)
    blog_categories_imported = models.IntegerField(default=0)
    blog_categories_skipped = models.IntegerField(default=0)
    blog_categories_failed = models.IntegerField(default=0)

    # Statistics - Blog Tags
    blog_tags_total = models.IntegerField(default=0)
    blog_tags_imported = models.IntegerField(default=0)
    blog_tags_skipped = models.IntegerField(default=0)
    blog_tags_failed = models.IntegerField(default=0)

    # Statistics - Media/Images
    media_total = models.IntegerField(default=0)
    media_imported = models.IntegerField(default=0)
    media_skipped = models.IntegerField(default=0)
    media_failed = models.IntegerField(default=0)

    # Statistics - Affiliates
    affiliates_total = models.IntegerField(default=0)
    affiliates_imported = models.IntegerField(default=0)
    affiliates_skipped = models.IntegerField(default=0)
    affiliates_failed = models.IntegerField(default=0)

    # Statistics - Commissions
    commissions_total = models.IntegerField(default=0)
    commissions_imported = models.IntegerField(default=0)
    commissions_skipped = models.IntegerField(default=0)
    commissions_failed = models.IntegerField(default=0)

    # Statistics - Payouts
    payouts_total = models.IntegerField(default=0)
    payouts_imported = models.IntegerField(default=0)
    payouts_skipped = models.IntegerField(default=0)
    payouts_failed = models.IntegerField(default=0)

    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Total migration duration in seconds")
    )

    # Logs (cached summaries for quick access)
    error_summary = models.TextField(
        blank=True,
        help_text=_("Summary of errors encountered")
    )
    warning_summary = models.TextField(
        blank=True,
        help_text=_("Summary of warnings encountered")
    )

    # Report Generation
    report_file = models.FileField(
        upload_to='migration_reports/',
        null=True,
        blank=True,
        help_text=_("Generated migration report (CSV/PDF)")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Migration Job')
        verbose_name_plural = _('Migration Jobs')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_by', '-created_at']),
            models.Index(fields=['platform', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_platform_display()} Migration - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_rollbackable(self):
        """Check if this migration can be rolled back"""
        if not self.can_rollback:
            return False
        if self.status != 'completed':
            return False
        if self.rollback_deadline and timezone.now() > self.rollback_deadline:
            return False
        return True

    @property
    def total_items(self):
        """Total items across all data types"""
        return (
            self.products_total +
            self.categories_total +
            self.customers_total +
            self.orders_total +
            self.reviews_total +
            self.coupons_total +
            self.variants_total +
            self.blog_posts_total +
            self.blog_categories_total +
            self.blog_tags_total +
            self.media_total
        )

    @property
    def total_imported(self):
        """Total successfully imported items"""
        return (
            self.products_imported +
            self.categories_imported +
            self.customers_imported +
            self.orders_imported +
            self.reviews_imported +
            self.coupons_imported +
            self.variants_imported +
            self.blog_posts_imported +
            self.blog_categories_imported +
            self.blog_tags_imported +
            self.media_imported
        )

    @property
    def total_failed(self):
        """Total failed imports"""
        return (
            self.products_failed +
            self.categories_failed +
            self.customers_failed +
            self.orders_failed +
            self.reviews_failed +
            self.coupons_failed +
            self.variants_failed +
            self.blog_posts_failed +
            self.blog_categories_failed +
            self.blog_tags_failed +
            self.media_failed
        )

    @property
    def total_skipped(self):
        """Total skipped items"""
        return (
            self.products_skipped +
            self.categories_skipped +
            self.customers_skipped +
            self.orders_skipped +
            self.reviews_skipped +
            self.coupons_skipped +
            self.variants_skipped +
            self.blog_posts_skipped +
            self.blog_categories_skipped +
            self.blog_tags_skipped +
            self.media_skipped
        )

    @property
    def success_rate(self):
        """Calculate success rate as percentage"""
        if self.total_items == 0:
            return 0
        return round((self.total_imported / self.total_items) * 100, 2)

    def update_progress(self, step, percent):
        """Update current progress"""
        self.current_step = step
        self.progress_percent = min(100, max(0, percent))  # Clamp to 0-100
        self.save(update_fields=['current_step', 'progress_percent'])

    def mark_completed(self):
        """Mark migration as completed and set rollback deadline"""
        self.status = 'completed'
        self.completed_at = timezone.now()

        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())

        # Set rollback deadline to 24 hours from now
        self.rollback_deadline = timezone.now() + timedelta(hours=24)
        self.progress_percent = 100
        self.save()

    def mark_failed(self, error_message):
        """Mark migration as failed"""
        self.status = 'failed'
        self.completed_at = timezone.now()

        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())

        self.error_summary = error_message
        self.can_rollback = False  # Failed migrations auto-rollback
        self.save()

    def start_migration(self):
        """Mark migration as started"""
        self.status = 'running'
        self.started_at = timezone.now()
        self.save()
