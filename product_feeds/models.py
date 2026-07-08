from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


class FeedProviderAccount(models.Model):
    """
    Merchant's connection to a product feed provider component.
    Pattern follows exchange_rates/models.py ExchangeRateProviderAccount.
    """
    site = models.ForeignKey(
        'sites.Site',
        on_delete=models.CASCADE,
        verbose_name=_("Site"),
        help_text=_("Site this feed provider account belongs to")
    )

    component = models.ForeignKey(
        'component_updates.ComponentRegistry',
        on_delete=models.PROTECT,
        limit_choices_to={'component_type': 'product_feed_provider'},
        related_name='feed_provider_accounts',
        verbose_name=_("Provider Component"),
        help_text=_("Product feed provider component from update system")
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Account Name"),
        help_text=_("Friendly name for this feed configuration (e.g., 'Google Shopping - US')")
    )

    credentials = models.BinaryField(
        blank=True,
        null=True,
        verbose_name=_("Encrypted Credentials"),
        help_text=_("Encrypted API credentials for this provider")
    )

    config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Feed Configuration"),
        help_text=_("Feed configuration including attribute mapping and product filters")
    )
    # Config structure:
    # {
    #     "sync_interval": "daily",  # hourly, daily, weekly, manual
    #     "format_preference": "xml",  # xml, csv, json
    #     "include_variants": true,
    #     "product_filter": {
    #         "status": ["published"],
    #         "categories": [1, 2, 3],
    #         "brands": [1, 2],
    #         "in_stock_only": true
    #     },
    #     "attribute_mapping": {
    #         "google_product_category": "category.google_id",
    #         "condition": "new",
    #         "custom_label_0": "attributes.season"
    #     },
    #     "exclude_products": [5, 10, 15],
    #     "target_country": "US",
    #     "content_language": "en"
    # }

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this feed is active and should be synced")
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary Feed"),
        help_text=_("Mark as primary feed for this provider type")
    )

    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Priority"),
        help_text=_("Sort order when displaying feeds (lower = first)")
    )

    # Sync tracking
    SYNC_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('syncing', _('Syncing')),
        ('success', _('Success')),
        ('error', _('Error')),
    ]
    sync_status = models.CharField(
        max_length=20,
        choices=SYNC_STATUS_CHOICES,
        default='pending',
        verbose_name=_("Sync Status")
    )

    last_sync_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Sync At"),
        help_text=_("When feed was last successfully synced")
    )

    next_sync_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Next Sync At"),
        help_text=_("When next scheduled sync should occur")
    )

    sync_error_message = models.TextField(
        blank=True,
        verbose_name=_("Sync Error Message"),
        help_text=_("Error message from last sync attempt")
    )

    last_error_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Error At"),
        help_text=_("When last error occurred")
    )

    # Feed statistics
    products_in_feed = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Products in Feed"),
        help_text=_("Number of products in the current feed")
    )

    # Hosted feed URL (for providers that fetch from URL)
    feed_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Feed URL"),
        help_text=_("URL where feed is hosted for provider to fetch")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Feed Provider Account")
        verbose_name_plural = _("Feed Provider Accounts")
        ordering = ['-is_primary', '-is_active', 'priority', 'name']
        indexes = [
            models.Index(fields=['site', 'is_active']),
            models.Index(fields=['priority']),
            models.Index(fields=['is_primary']),
            models.Index(fields=['sync_status']),
            models.Index(fields=['next_sync_at']),
        ]
        constraints = [
            # Unique name per site and component
            models.UniqueConstraint(
                fields=['site', 'component', 'name'],
                name='unique_feed_account_per_site_component'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.component.name})"

    def get_provider_instance(self):
        """Get initialized provider instance"""
        from product_feeds.providers.registry import ProviderRegistry
        from product_feeds.utils.encryption import decrypt_credentials

        provider_class = ProviderRegistry.get_provider(self.component.slug)
        if not provider_class:
            raise ValueError(f"Provider {self.component.slug} not found in registry")

        # Decrypt credentials and pass to provider
        credentials = decrypt_credentials(self.credentials) if self.credentials else {}
        return provider_class(credentials=credentials, config=self.config)

    def calculate_next_sync(self):
        """Calculate next sync time based on config interval"""
        interval = self.config.get('sync_interval', 'daily')
        now = timezone.now()

        interval_mapping = {
            'hourly': timedelta(hours=1),
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'manual': None,
        }

        delta = interval_mapping.get(interval)
        if delta:
            self.next_sync_at = now + delta
        else:
            self.next_sync_at = None

    @property
    def sync_interval_display(self):
        """Human-readable sync interval"""
        interval = self.config.get('sync_interval', 'daily')
        return {
            'hourly': _('Every Hour'),
            'daily': _('Once Daily'),
            'weekly': _('Once Weekly'),
            'manual': _('Manual Only'),
        }.get(interval, interval)


class ProductFeed(models.Model):
    """
    Generated feed content cache.
    Stores the actual feed data for download or provider fetch.
    """
    account = models.ForeignKey(
        FeedProviderAccount,
        on_delete=models.CASCADE,
        related_name='feeds',
        verbose_name=_("Provider Account")
    )

    FORMAT_CHOICES = [
        ('xml', 'XML'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
    ]
    feed_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        verbose_name=_("Feed Format")
    )

    # Feed content - for smaller feeds stored in DB
    content = models.TextField(
        blank=True,
        verbose_name=_("Feed Content"),
        help_text=_("Feed content for smaller feeds")
    )

    # For larger feeds, store file path
    file_path = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("File Path"),
        help_text=_("File path for large feeds stored on disk")
    )

    # Metadata
    file_size = models.PositiveIntegerField(
        default=0,
        verbose_name=_("File Size"),
        help_text=_("Size in bytes")
    )

    product_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Product Count"),
        help_text=_("Number of products in this feed")
    )

    # Timestamps
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Generated At")
    )

    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
        help_text=_("When this cached feed expires")
    )

    # Validation results and statistics
    stats = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Statistics"),
        help_text=_("Feed statistics and validation results")
    )
    # Stats structure:
    # {
    #     "products_included": 1000,
    #     "products_excluded": 50,
    #     "products_with_errors": 5,
    #     "warnings": ["10 products missing GTIN"],
    #     "errors": [],
    #     "validation_passed": true
    # }

    # Download tracking
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Download Count")
    )

    last_downloaded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Downloaded At")
    )

    class Meta:
        verbose_name = _("Product Feed")
        verbose_name_plural = _("Product Feeds")
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['account', '-generated_at']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.account.name} - {self.feed_format.upper()} ({self.generated_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def is_expired(self):
        """Check if feed has expired"""
        return timezone.now() > self.expires_at

    @property
    def has_file(self):
        """Check if feed content is stored in file"""
        return bool(self.file_path)

    def get_content(self):
        """Get feed content from DB or file"""
        if self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                return ''
        return self.content

    def get_content_type(self):
        """Get MIME content type for feed format"""
        content_types = {
            'xml': 'application/xml',
            'csv': 'text/csv',
            'json': 'application/json',
        }
        return content_types.get(self.feed_format, 'text/plain')

    def increment_download(self):
        """Track download"""
        self.download_count += 1
        self.last_downloaded_at = timezone.now()
        self.save(update_fields=['download_count', 'last_downloaded_at'])


class FeedSyncLog(models.Model):
    """
    Audit log for feed sync operations.
    Tracks every sync attempt with detailed results.
    """
    account = models.ForeignKey(
        FeedProviderAccount,
        on_delete=models.CASCADE,
        related_name='sync_logs',
        verbose_name=_("Provider Account")
    )

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('running', _('Running')),
        ('success', _('Success')),
        ('partial', _('Partial Success')),
        ('failed', _('Failed')),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Status")
    )

    # Timing
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Started At")
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Completed At")
    )

    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Duration (seconds)")
    )

    # Statistics
    products_synced = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Products Synced")
    )

    products_failed = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Products Failed")
    )

    products_skipped = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Products Skipped")
    )

    # Error tracking
    error_message = models.TextField(
        blank=True,
        verbose_name=_("Error Message")
    )

    error_details = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Error Details"),
        help_text=_("Detailed error information, including per-product errors")
    )
    # Error details structure:
    # {
    #     "product_errors": [
    #         {"product_id": 123, "sku": "ABC", "error": "Missing required field: title"}
    #     ],
    #     "api_errors": [...],
    #     "validation_errors": [...]
    # }

    # Reference to generated feed (if successful)
    feed = models.ForeignKey(
        ProductFeed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sync_logs',
        verbose_name=_("Generated Feed")
    )

    # Sync type
    SYNC_TYPE_CHOICES = [
        ('full', _('Full Sync')),
        ('incremental', _('Incremental')),
        ('manual', _('Manual')),
        ('scheduled', _('Scheduled')),
    ]
    sync_type = models.CharField(
        max_length=20,
        choices=SYNC_TYPE_CHOICES,
        default='full',
        verbose_name=_("Sync Type")
    )

    class Meta:
        verbose_name = _("Feed Sync Log")
        verbose_name_plural = _("Feed Sync Logs")
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['account', '-started_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.account.name} - {self.status} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"

    def complete(self, status='success', error_message=''):
        """Mark sync as complete"""
        self.status = status
        self.completed_at = timezone.now()
        self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
        if error_message:
            self.error_message = error_message
        self.save()

    @property
    def total_products(self):
        """Total products processed"""
        return self.products_synced + self.products_failed + self.products_skipped

    @property
    def duration_display(self):
        """Return human-readable duration string"""
        if self.duration_seconds is None:
            return None
        if self.duration_seconds < 60:
            return f"{self.duration_seconds}s"
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        if self.duration_seconds < 3600:
            return f"{minutes}m {seconds}s"
        hours = self.duration_seconds // 3600
        remaining_minutes = (self.duration_seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"

    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        total = self.total_products
        if total == 0:
            return 0
        return round((self.products_synced / total) * 100, 1)
