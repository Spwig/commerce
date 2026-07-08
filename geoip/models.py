"""
GeoIP Models for caching and storing location data
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
import json


class GeoLocation(models.Model):
    """
    Cached geo-location data for IP addresses
    """
    ip_address = models.GenericIPAddressField(unique=True, db_index=True)
    ip_prefix = models.CharField(max_length=50, db_index=True, help_text="IP prefix for cache grouping (/24 for IPv4, /48 for IPv6)")

    # Location data
    country_code = models.CharField(max_length=2, blank=True, db_index=True)
    country_name = models.CharField(max_length=100, blank=True)
    region_code = models.CharField(max_length=10, blank=True)
    region_name = models.CharField(max_length=100, blank=True)
    city_name = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Coordinates
    latitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])

    # Network info
    asn = models.CharField(max_length=50, blank=True, help_text="Autonomous System Number")
    isp = models.CharField(max_length=200, blank=True, help_text="Internet Service Provider")

    # Meta information
    source = models.CharField(max_length=50, default='unknown', help_text="Data source (e.g., maxmind, dbip, ip2location)")
    confidence = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    is_proxy = models.BooleanField(default=False)
    is_vpn = models.BooleanField(default=False)
    is_tor = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)

    # Timestamps
    resolved_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Geo Location")
        verbose_name_plural = _("Geo Locations")
        ordering = ['-resolved_at']
        indexes = [
            models.Index(fields=['ip_prefix', 'country_code']),
            models.Index(fields=['resolved_at', 'expires_at']),
        ]

    def __str__(self):
        return f"{self.ip_address} → {self.country_code or 'Unknown'}"

    @property
    def is_expired(self):
        """Check if this cache entry has expired"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'ip': self.ip_address,
            'country': self.country_code,
            'country_name': self.country_name,
            'region': self.region_code,
            'region_name': self.region_name,
            'city': self.city_name,
            'postal_code': self.postal_code,
            'lat': self.latitude,
            'lon': self.longitude,
            'asn': self.asn,
            'isp': self.isp,
            'source': self.source,
            'confidence': self.confidence,
            'is_proxy': self.is_proxy,
            'is_vpn': self.is_vpn,
            'is_tor': self.is_tor,
            'is_mobile': self.is_mobile,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
        }


class CountryMapping(models.Model):
    """
    Mapping of countries to currencies, languages, and other settings
    """
    country_code = models.CharField(max_length=2, unique=True, db_index=True)
    country_name = models.CharField(max_length=100)

    # Currency
    default_currency = models.CharField(max_length=3, default='USD')
    accepted_currencies = ArrayField(
        models.CharField(max_length=3),
        default=list,
        blank=True,
        help_text="List of accepted currencies for this country"
    )

    # Language
    default_language = models.CharField(max_length=10, default='en', help_text="Default language code (e.g., en, es, fr, zh-hans)")
    supported_languages = ArrayField(
        models.CharField(max_length=10),
        default=list,
        blank=True,
        help_text="List of supported languages"
    )

    # Regional settings
    timezone = models.CharField(max_length=50, blank=True)
    date_format = models.CharField(max_length=20, default='MM/DD/YYYY')
    uses_metric = models.BooleanField(default=True)

    # Tax and shipping
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Default tax rate %")
    is_eu_member = models.BooleanField(default=False)
    requires_vat = models.BooleanField(default=False)
    shipping_zone = models.CharField(max_length=50, blank=True, help_text="Shipping zone identifier")

    # Feature flags
    supports_cod = models.BooleanField(default=False, help_text="Supports Cash on Delivery")
    blocked_payment_methods = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )

    # Custom rules (JSON)
    custom_rules = models.JSONField(default=dict, blank=True, help_text="Custom business rules for this country")

    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Country Mapping")
        verbose_name_plural = _("Country Mappings")
        ordering = ['country_code']

    def __str__(self):
        return f"{self.country_code} - {self.country_name}"

    def get_currency_display(self):
        """Get currency with symbol"""
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'CAD': 'C$',
            'AUD': 'A$',
        }
        return f"{self.default_currency} {currency_symbols.get(self.default_currency, '')}"


class GeoIPProvider(models.Model):
    """
    Configuration for GeoIP data providers
    """
    PROVIDER_CHOICES = [
        ('spwig', 'Spwig GeoIP (Default)'),
        ('maxmind', 'MaxMind GeoLite2'),
        ('dbip', 'DB-IP Lite'),
        ('ip2location', 'IP2Location LITE'),
        ('edge_header', 'CDN Edge Headers'),
        ('browser_hint', 'Browser Hints'),
        ('custom', 'Custom Provider'),
    ]

    name = models.CharField(max_length=100)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Lower number = higher priority")

    # Configuration
    config = models.JSONField(default=dict, help_text="Provider-specific configuration")

    # Database files
    database_path = models.CharField(max_length=500, blank=True)
    database_url = models.URLField(blank=True, help_text="URL to download database")
    license_key = models.CharField(max_length=200, blank=True)

    # Update tracking
    last_update = models.DateTimeField(null=True, blank=True)
    next_update = models.DateTimeField(null=True, blank=True)
    database_version = models.CharField(max_length=50, blank=True)

    # Statistics
    total_lookups = models.BigIntegerField(default=0)
    successful_lookups = models.BigIntegerField(default=0)
    failed_lookups = models.BigIntegerField(default=0)
    average_response_ms = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("GeoIP Provider")
        verbose_name_plural = _("GeoIP Providers")
        ordering = ['priority', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

    @property
    def accuracy_rate(self):
        """Calculate accuracy rate"""
        if self.total_lookups == 0:
            return 0.0
        return (self.successful_lookups / self.total_lookups) * 100


class VisitorLocation(models.Model):
    """
    Track visitor locations for analytics and feedback
    """
    session_key = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()

    # Resolved location
    resolved_country = models.CharField(max_length=2, blank=True)
    resolved_region = models.CharField(max_length=100, blank=True)
    resolved_city = models.CharField(max_length=100, blank=True)

    # User corrections
    actual_country = models.CharField(max_length=2, blank=True)
    actual_region = models.CharField(max_length=100, blank=True)
    actual_city = models.CharField(max_length=100, blank=True)

    # Selected preferences
    selected_currency = models.CharField(max_length=3, blank=True)
    selected_language = models.CharField(max_length=10, blank=True)

    # UTM tracking for marketing attribution
    referrer_url = models.URLField(max_length=2048, blank=True, help_text="Referrer URL from HTTP header")
    utm_source = models.CharField(max_length=255, blank=True, db_index=True, help_text="Campaign source (e.g., google, newsletter)")
    utm_medium = models.CharField(max_length=255, blank=True, db_index=True, help_text="Campaign medium (e.g., cpc, email, social)")
    utm_campaign = models.CharField(max_length=255, blank=True, db_index=True, help_text="Campaign name (e.g., summer_sale)")
    utm_term = models.CharField(max_length=255, blank=True, help_text="Paid keywords")
    utm_content = models.CharField(max_length=255, blank=True, help_text="Content variation (e.g., A/B test)")

    # Device detection
    DEVICE_TYPE_CHOICES = [
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('unknown', 'Unknown'),
    ]
    device_type = models.CharField(
        max_length=10,
        choices=DEVICE_TYPE_CHOICES,
        default='unknown',
        db_index=True,
        help_text="Device type detected from user agent"
    )

    # Metadata
    user_agent = models.TextField(blank=True)
    accept_language = models.CharField(max_length=200, blank=True)
    timezone_offset = models.IntegerField(null=True, blank=True, help_text="Minutes offset from UTC")

    # Bot / automation detection
    is_bot = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Detected as bot, crawler, or headless browser"
    )
    is_admin_traffic = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Traffic originated from admin/staff pages"
    )

    # Tracking
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    page_views = models.IntegerField(default=1)

    class Meta:
        verbose_name = _("Visitor Location")
        verbose_name_plural = _("Visitor Locations")
        ordering = ['-last_seen']
        indexes = [
            models.Index(fields=['resolved_country', 'first_seen']),
            models.Index(fields=['utm_source', 'utm_medium', 'utm_campaign']),
            models.Index(fields=['utm_campaign', 'first_seen']),
            models.Index(fields=['device_type', 'first_seen']),
            models.Index(fields=['is_bot', 'first_seen']),
            models.Index(fields=['is_admin_traffic', 'first_seen']),
        ]

    def __str__(self):
        return f"{self.session_key} - {self.resolved_country or 'Unknown'}"

    @property
    def was_corrected(self):
        """Check if user corrected the location"""
        return bool(self.actual_country and self.actual_country != self.resolved_country)


class BusinessRule(models.Model):
    """
    Business rules based on geo-location
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Lower number = higher priority")

    # Conditions (JSON)
    conditions = models.JSONField(
        default=dict,
        help_text="""
        Example: {
            "country_in": ["US", "CA"],
            "region_not_in": ["Quebec"],
            "is_mobile": true
        }
        """
    )

    # Actions (JSON)
    actions = models.JSONField(
        default=dict,
        help_text="""
        Example: {
            "set_currency": "USD",
            "show_banner": true,
            "redirect_to": "/us-store"
        }
        """
    )

    # Tracking
    times_triggered = models.BigIntegerField(default=0)
    last_triggered = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Business Rule")
        verbose_name_plural = _("Business Rules")
        ordering = ['priority', 'name']

    def __str__(self):
        return self.name

    def evaluate(self, location_data):
        """
        Evaluate if this rule applies to the given location data
        Returns True if all conditions match
        """
        if not self.is_active:
            return False

        for key, value in self.conditions.items():
            if key == 'country_in' and location_data.get('country') not in value:
                return False
            elif key == 'country_not_in' and location_data.get('country') in value:
                return False
            elif key == 'region_in' and location_data.get('region') not in value:
                return False
            elif key == 'region_not_in' and location_data.get('region') in value:
                return False
            elif key == 'is_mobile' and location_data.get('is_mobile') != value:
                return False
            elif key == 'is_vpn' and location_data.get('is_vpn') != value:
                return False

        return True


class PageView(models.Model):
    """
    Individual page view events for per-URL analytics.
    Tracks every page navigation from both headless (API) and direct (middleware) sources.
    """
    SOURCE_CHOICES = [
        ('headless', 'Headless Frontend'),
        ('middleware', 'Direct Django'),
    ]

    visitor = models.ForeignKey(
        VisitorLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='page_view_set',
    )
    session_key = models.CharField(max_length=100, db_index=True)
    url = models.CharField(max_length=2048, help_text="Full URL as sent by frontend")
    url_path = models.CharField(
        max_length=500,
        db_index=True,
        help_text="Normalized path without locale prefix or query params (e.g., /pricing)"
    )
    referrer = models.URLField(max_length=2048, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_entry_page = models.BooleanField(default=False, db_index=True)
    is_exit_page = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False, db_index=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='middleware')

    class Meta:
        verbose_name = _("Page View")
        verbose_name_plural = _("Page Views")
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['url_path', 'timestamp']),
            models.Index(fields=['session_key', 'timestamp']),
            models.Index(fields=['is_bot', 'timestamp']),
            models.Index(fields=['is_entry_page', 'url_path']),
        ]

    def __str__(self):
        return f"{self.url_path} @ {self.timestamp:%Y-%m-%d %H:%M}"


class DailyPageStats(models.Model):
    """
    Pre-aggregated daily statistics per page URL.
    Populated by the aggregate_daily_page_stats Celery task.
    """
    date = models.DateField(db_index=True)
    url_path = models.CharField(max_length=500, db_index=True)
    views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    bot_views = models.PositiveIntegerField(default=0)
    entries = models.PositiveIntegerField(default=0, help_text="Times this was the landing page")

    class Meta:
        verbose_name = _("Daily Page Stats")
        verbose_name_plural = _("Daily Page Stats")
        ordering = ['-date', '-views']
        constraints = [
            models.UniqueConstraint(fields=['date', 'url_path'], name='unique_daily_page_stats'),
        ]

    def __str__(self):
        return f"{self.url_path} on {self.date} ({self.views} views)"


class DailyTrafficStats(models.Model):
    """
    Global daily traffic summary.
    Populated by the aggregate_daily_page_stats Celery task.
    """
    date = models.DateField(unique=True, db_index=True)
    total_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    bot_views = models.PositiveIntegerField(default=0)
    new_visitors = models.PositiveIntegerField(default=0)
    returning_visitors = models.PositiveIntegerField(default=0)
    desktop_views = models.PositiveIntegerField(default=0)
    mobile_views = models.PositiveIntegerField(default=0)
    tablet_views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Daily Traffic Stats")
        verbose_name_plural = _("Daily Traffic Stats")
        ordering = ['-date']

    def __str__(self):
        return f"{self.date}: {self.total_views} views, {self.unique_visitors} visitors"