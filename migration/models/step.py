"""
MigrationStep Model
Tracks individual steps within a migration job (products, customers, orders, etc.)
Used for savepoint management and granular rollback.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MigrationStep(models.Model):
    """
    Tracks individual steps within a migration job.
    Each step represents importing one data type (e.g., products, customers).
    Used for transaction savepoint management.
    """
    job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.CASCADE,
        related_name='steps',
        help_text=_("Parent migration job")
    )

    STEP_TYPES = [
        ('categories', _('Categories')),
        ('brands', _('Brands')),
        ('products', _('Products')),
        ('product_images', _('Product Images')),
        ('product_variants', _('Product Variants')),
        ('customers', _('Customers')),
        ('customer_addresses', _('Customer Addresses')),
        ('orders', _('Orders')),
        ('order_items', _('Order Items')),
        ('reviews', _('Reviews')),
        ('coupons', _('Coupons')),
        ('blog', _('Blog')),
        ('shipping_zones', _('Shipping Zones')),
        ('tax_rates', _('Tax Rates')),
        ('link_rewriting', _('Link Rewriting')),
        ('affiliates', _('Affiliates')),
        ('commissions', _('Commissions')),
        ('payouts', _('Payouts')),
    ]
    step_type = models.CharField(
        max_length=30,
        choices=STEP_TYPES,
        help_text=_("Type of data being imported in this step")
    )

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('running', _('Running')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('skipped', _('Skipped')),
        ('rolled_back', _('Rolled Back')),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )

    # Transaction Management
    savepoint_id = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Database savepoint ID for this step")
    )

    # Statistics
    items_total = models.IntegerField(
        default=0,
        help_text=_("Total items to import in this step")
    )
    items_imported = models.IntegerField(
        default=0,
        help_text=_("Items successfully imported")
    )
    items_skipped = models.IntegerField(
        default=0,
        help_text=_("Items skipped (duplicates, validation failures)")
    )
    items_failed = models.IntegerField(
        default=0,
        help_text=_("Items that failed to import")
    )

    # Timing
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When this step started")
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When this step completed")
    )
    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Duration of this step in seconds")
    )

    # Error Tracking
    error_message = models.TextField(
        blank=True,
        help_text=_("Error message if step failed")
    )
    error_count = models.IntegerField(
        default=0,
        help_text=_("Number of errors encountered in this step")
    )
    warning_count = models.IntegerField(
        default=0,
        help_text=_("Number of warnings encountered in this step")
    )

    # Progress Details
    current_item = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Currently processing item (for progress display)")
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Migration Step')
        verbose_name_plural = _('Migration Steps')
        unique_together = ['job', 'step_type']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['step_type']),
        ]

    def __str__(self):
        return f"{self.job} - {self.get_step_type_display()} ({self.status})"

    @property
    def progress_percent(self):
        """Calculate progress percentage for this step"""
        if self.items_total == 0:
            return 0
        processed = self.items_imported + self.items_skipped + self.items_failed
        return min(100, round((processed / self.items_total) * 100, 2))

    @property
    def success_rate(self):
        """Calculate success rate for this step"""
        if self.items_total == 0:
            return 0
        return round((self.items_imported / self.items_total) * 100, 2)

    def start(self):
        """Mark this step as started"""
        self.status = 'running'
        self.started_at = timezone.now()
        self.save()

    def complete(self):
        """Mark this step as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()

        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())

        self.save()

    def fail(self, error_message):
        """Mark this step as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.completed_at = timezone.now()

        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())

        self.save()

    def increment_imported(self):
        """Increment imported count"""
        self.items_imported += 1
        self.save(update_fields=['items_imported'])

    def increment_skipped(self):
        """Increment skipped count"""
        self.items_skipped += 1
        self.save(update_fields=['items_skipped'])

    def increment_failed(self):
        """Increment failed count"""
        self.items_failed += 1
        self.save(update_fields=['items_failed'])

    def update_current_item(self, item_name):
        """Update the currently processing item"""
        self.current_item = item_name
        self.save(update_fields=['current_item'])
