from django.db import models
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from djmoney import models as money_models
from pgvector.django import VectorField
import hashlib
import uuid


class SoftDeleteQuerySet(models.QuerySet):
    """Custom QuerySet for soft delete functionality"""

    def deleted(self):
        """Return only deleted objects"""
        return self.filter(is_deleted=True)

    def active(self):
        """Return only non-deleted objects"""
        return self.filter(is_deleted=False)

    def with_deleted(self):
        """Return all objects including deleted"""
        return self.all()

    def delete(self):
        """Soft delete all objects in the queryset"""
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all objects in the queryset"""
        return super().delete()

    def restore(self):
        """Restore all soft-deleted objects in the queryset"""
        return self.update(is_deleted=False, deleted_at=None, deleted_by=None)


class SoftDeleteManager(models.Manager):
    """Manager that filters out soft-deleted objects by default"""

    def get_queryset(self):
        """Return only non-deleted objects by default"""
        return SoftDeleteQuerySet(self.model, using=self._db).active()

    def deleted(self):
        """Return only deleted objects"""
        return self.get_queryset().deleted()

    def with_deleted(self):
        """Return all objects including deleted"""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def all_with_deleted(self):
        """Return all objects including deleted"""
        return self.with_deleted()


class SoftDeleteModel(models.Model):
    """
    Abstract base model that provides soft delete functionality.
    Instead of actually deleting objects, it marks them as deleted.
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_("Whether this object has been soft deleted")
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text=_("When this object was soft deleted")
    )

    deleted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_deleted',
        help_text=_("User who deleted this object")
    )

    # Managers
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes deleted objects

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, user=None):
        """
        Soft delete the object instead of actually deleting it.

        Args:
            user: The user performing the deletion (optional)
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])

    def hard_delete(self, using=None, keep_parents=False):
        """
        Actually delete the object from the database.
        Use with caution!
        """
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """
        Restore a soft-deleted object
        """
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])

    @property
    def is_active(self):
        """Check if the object is active (not deleted)"""
        return not self.is_deleted


class SiteSettings(models.Model):
    """
    Global site settings for the e-commerce platform.
    This should be a singleton model - only one instance should exist.
    """
    
    # Basic Site Information
    site_name = models.CharField(
        max_length=100,
        default="My E-commerce Store",
        help_text="The name of your store that appears in the header and emails"
    )

    site_tagline = models.CharField(
        max_length=200,
        blank=True,
        help_text="A short, catchy tagline for your store (e.g., 'Quality Products, Unbeatable Prices')"
    )

    site_url = models.URLField(
        default="https://example.com",
        validators=[URLValidator()],
        help_text="The main URL of your store (used in emails and links)"
    )
    
    site_description = models.TextField(
        blank=True,
        help_text="A brief description of your store (used for SEO and social media sharing)"
    )
    
    favicon = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='favicon_for_site',
        help_text="Select a favicon from the media library (recommended: 32x32 or 16x16 pixels, ICO, PNG, or SVG format)"
    )

    site_logo = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='site_logo_for_site',
        help_text=_("Select a logo from the media library. Recommended: PNG or SVG format. Horizontal logos work best (max 400px wide). SVG files scale perfectly to any size.")
    )

    # Contact Information
    admin_email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Primary admin email for system notifications and customer service"
    )
    
    support_email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        help_text="Customer support email (if different from admin email)"
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Store contact phone number"
    )
    
    # Business Address
    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Street address"
    )
    
    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Apartment, suite, etc."
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="City"
    )
    
    state_province = models.CharField(
        max_length=100,
        blank=True,
        help_text="State or Province"
    )
    
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="ZIP or Postal Code"
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        help_text="Country"
    )
    
    # Currency and Locale Settings
    # Note: Currency, language, and timezone choices are now dynamically populated via form
    # to leverage GeoIP data and comprehensive libraries (django-money, zoneinfo)
    # See core/utils/locale_helpers.py for helper functions

    default_currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Default currency for product prices and transactions."
    )

    default_language = models.CharField(
        max_length=10,
        default='en',
        help_text="Default language for the store interface and content."
    )

    default_timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="Default timezone for displaying dates and times."
    )

    # Multi-Currency Settings
    enable_multi_currency = models.BooleanField(
        default=False,
        verbose_name=_("Enable Multi-Currency"),
        help_text=_("Allow customers to view prices and checkout in different currencies. Requires exchange rate provider configuration.")
    )

    supported_currencies = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Supported Currencies"),
        help_text=_("List of currency codes enabled for customer selection (e.g., ['USD', 'EUR', 'GBP']). Leave empty to support all 308 currencies.")
    )

    CURRENCY_SELECTION_MODE_CHOICES = [
        ('auto', _('Automatic (GeoIP Detection)')),
        ('manual', _('Manual (Customer Choice Only)')),
        ('both', _('Both (Auto-detect with Manual Override)')),
    ]

    currency_selection_mode = models.CharField(
        max_length=10,
        choices=CURRENCY_SELECTION_MODE_CHOICES,
        default='both',
        verbose_name=_("Currency Selection Mode"),
        help_text=_("How customers select their preferred currency")
    )

    show_currency_switcher = models.BooleanField(
        default=True,
        verbose_name=_("Show Currency Switcher"),
        help_text=_("Display currency switcher widget in storefront (only when multi-currency is enabled)")
    )

    CURRENCY_SWITCHER_POSITION_CHOICES = [
        ('header', _('Header (Top Right)')),
        ('footer', _('Footer')),
        ('both', _('Both Header and Footer')),
        ('widget', _('Widget Area Only')),
    ]

    currency_switcher_position = models.CharField(
        max_length=10,
        choices=CURRENCY_SWITCHER_POSITION_CHOICES,
        default='header',
        verbose_name=_("Currency Switcher Position"),
        help_text=_("Where to display the currency switcher widget")
    )

    show_exchange_rate_info = models.BooleanField(
        default=False,
        verbose_name=_("Show Exchange Rate Information"),
        help_text=_("Display exchange rate and last update time to customers (transparency feature)")
    )

    enable_locale_formatting = models.BooleanField(
        default=True,
        verbose_name=_("Enable Locale-Aware Formatting"),
        help_text=_("Format currency amounts according to customer's locale (e.g., '$1,234.56' for US, '1.234,56 €' for Germany)")
    )

    # Exchange Rate Markup Settings
    exchange_rate_markup_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Enable Exchange Rate Markup"),
        help_text=_("Add a percentage markup to exchange rates to cover conversion fees and currency risk")
    )

    exchange_rate_markup_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Exchange Rate Markup Percentage"),
        help_text=_("Percentage to add to exchange rates (e.g., 2.50 for 2.5% markup). Only applied when markup is enabled.")
    )

    EXCHANGE_RATE_SELECTION_CHOICES = [
        ('primary', _('Always use primary provider rates')),
        ('latest', _('Use latest available rate from any provider')),
    ]

    exchange_rate_selection_strategy = models.CharField(
        max_length=10,
        choices=EXCHANGE_RATE_SELECTION_CHOICES,
        default='primary',
        verbose_name=_("Rate Selection Strategy"),
        help_text=_("When multiple providers are active: 'Primary' always uses rates from your primary provider (consistent pricing), 'Latest' uses the most recently synced rate from any active provider (freshest data).")
    )

    EXCHANGE_RATE_SYNC_INTERVAL_CHOICES = [
        ('realtime', _('Real-time (every 15 minutes)')),
        ('hourly', _('Hourly')),
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('manual_only', _('Manual Only (no auto-sync)')),
    ]

    exchange_rate_sync_interval = models.CharField(
        max_length=15,
        choices=EXCHANGE_RATE_SYNC_INTERVAL_CHOICES,
        default='daily',
        verbose_name=_("Exchange Rate Sync Interval"),
        help_text=_("How often to automatically sync exchange rates from providers. "
                    "'Manual Only' disables auto-sync; you control rates entirely via manual rates.")
    )

    MULTI_CURRENCY_CHECKOUT_MODE_CHOICES = [
        ('full', _('Full Multi-Currency (checkout in visitor currency)')),
        ('display_only', _('Display Only (show converted prices, charge in base currency)')),
    ]

    multi_currency_checkout_mode = models.CharField(
        max_length=15,
        choices=MULTI_CURRENCY_CHECKOUT_MODE_CHOICES,
        default='full',
        verbose_name=_("Multi-Currency Checkout Mode"),
        help_text=_(
            "Full: Customers browse and pay in their selected currency. "
            "Display Only: Prices shown in visitor's currency for browsing, "
            "but all payments are charged in your base currency with a transparent conversion notice."
        )
    )

    # Exchange Rate Provider (FK will be added in Week 2 when provider models are created)
    # default_exchange_rate_provider = models.ForeignKey(
    #     'multicurrency.ExchangeRateProvider',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='default_for_site',
    #     verbose_name=_("Default Exchange Rate Provider"),
    #     help_text=_("API provider for fetching exchange rates (Open Exchange Rates, Fixer.io, etc.)")
    # )

    # E-commerce Settings
    allow_guest_checkout = models.BooleanField(
        default=True,
        help_text="Allow customers to checkout without creating an account"
    )
    
    require_phone_for_checkout = models.BooleanField(
        default=False,
        help_text="Require phone number during checkout"
    )
    
    enable_inventory_tracking = models.BooleanField(
        default=True,
        help_text="Track product inventory and prevent overselling"
    )

    enable_multi_warehouse = models.BooleanField(
        default=False,
        help_text="Enable multi-warehouse inventory management. When disabled, all products use the main warehouse with simplified stock management."
    )

    auto_approve_reviews = models.BooleanField(
        default=False,
        help_text="Automatically approve product reviews without moderation"
    )

    # Account Creation Timing Settings
    ACCOUNT_CREATION_TIMING_CHOICES = [
        ('before_checkout', _('Before Checkout (Step 1) - Not Recommended')),
        ('during_checkout', _('During Checkout (Before Payment)')),
        ('post_purchase', _('After Purchase - Recommended')),
    ]

    account_creation_timing = models.CharField(
        max_length=20,
        choices=ACCOUNT_CREATION_TIMING_CHOICES,
        default='post_purchase',
        verbose_name=_("Account Creation Timing"),
        help_text=_(
            "When to prompt customers to create an account. "
            "'After Purchase' leverages post-purchase positive emotion for highest conversion. "
            "'During Checkout' creates account before payment. "
            "'Before Checkout' requires account upfront (not recommended - reduces conversion)."
        )
    )

    account_creation_message = models.TextField(
        default='',
        blank=True,
        verbose_name=_("Account Creation Message"),
        help_text=_(
            "Custom message explaining why creating an account is beneficial. "
            "Supports translations. "
            "Default: 'Create an account to track your order, save addresses, and enjoy faster checkout next time!'"
        )
    )

    show_social_auth_on_account_creation = models.BooleanField(
        default=True,
        verbose_name=_("Show Social Authentication Options"),
        help_text=_(
            "Display social login buttons (Google, Apple, Microsoft) during account creation "
            "if configured in OAuth Provider Settings."
        )
    )

    # Email Settings
    enable_order_confirmation_emails = models.BooleanField(
        default=True,
        help_text="Send order confirmation emails to customers"
    )
    
    enable_shipping_notification_emails = models.BooleanField(
        default=True,
        help_text="Send shipping notification emails to customers"
    )
    
    enable_low_stock_alerts = models.BooleanField(
        default=True,
        help_text="Send low stock alerts to admin email"
    )
    
    low_stock_threshold = models.PositiveIntegerField(
        default=10,
        help_text="Stock level at which to send low stock alerts"
    )

    # Email Delivery Mode
    EMAIL_DELIVERY_MODE_CHOICES = [
        ('live', _('Live - Deliver emails normally')),
        ('paused', _('Paused - Hold emails for later delivery')),
        ('log_only', _('Log Only - Record emails but never deliver')),
    ]

    email_delivery_mode = models.CharField(
        max_length=10,
        choices=EMAIL_DELIVERY_MODE_CHOICES,
        default='live',
        verbose_name=_("Email Delivery Mode"),
        help_text=_(
            "Controls how outgoing emails are handled. "
            "'Live' delivers normally. "
            "'Paused' holds emails until you switch back to Live. "
            "'Log Only' records emails in the outbox for review but never sends them."
        )
    )

    email_test_redirect_address = models.EmailField(
        blank=True,
        verbose_name=_("Test Redirect Email"),
        help_text=_(
            "When set, ALL outgoing emails are redirected to this address instead of the real recipient. "
            "Useful for testing email templates and flows. Leave blank to send to actual recipients."
        )
    )

    # Sandbox Whitelists (enforced by license system in sandbox/dev mode)
    sandbox_email_whitelist = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Sandbox Email Whitelist"),
        help_text=_(
            "In sandbox mode, only emails to these addresses will be delivered. "
            "All other emails are logged but never sent. "
            "The admin email is always included automatically. Maximum 10 addresses."
        )
    )

    sandbox_sms_whitelist = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Sandbox SMS Whitelist"),
        help_text=_(
            "In sandbox mode, only SMS messages to these phone numbers will be sent. "
            "All other messages are logged but never delivered. "
            "Use E.164 format (e.g., +1234567890). Maximum 5 numbers."
        )
    )

    # SEO Settings
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Default meta title for pages (60 characters max)"
    )
    
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Default meta description for pages (160 characters max)"
    )
    
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Default meta keywords for pages (comma-separated)"
    )
    
    # Social Media
    facebook_url = models.URLField(
        blank=True,
        help_text="Facebook page URL"
    )
    
    twitter_url = models.URLField(
        blank=True,
        help_text="Twitter profile URL"
    )
    
    instagram_url = models.URLField(
        blank=True,
        help_text="Instagram profile URL"
    )
    
    linkedin_url = models.URLField(
        blank=True,
        help_text="LinkedIn page URL"
    )
    
    # Maintenance
    maintenance_mode = models.BooleanField(
        default=False,
        help_text="Enable maintenance mode (site will show maintenance page)"
    )
    
    maintenance_message = models.TextField(
        blank=True,
        default="We are currently performing scheduled maintenance. Please check back soon.",
        help_text="Message to display during maintenance mode"
    )

    maintenance_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Maintenance Page"),
        help_text=_("Custom page displayed when maintenance mode is enabled. Edit this page in Page Builder to customize the maintenance experience.")
    )

    # Error Reporting
    error_reporting_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Enable Error Reporting"),
        help_text=_("Automatically send anonymized error reports to Spwig to help improve the platform. No personal data is ever transmitted.")
    )
    error_reporting_include_js = models.BooleanField(
        default=True,
        verbose_name=_("Include JavaScript Errors"),
        help_text=_("Also capture and report JavaScript errors from the storefront and admin interface.")
    )

    # Shipping Settings
    enable_shipping_labels = models.BooleanField(
        default=False,
        verbose_name=_("Enable Shipping Labels"),
        help_text="Enable API-based shipping label generation. When disabled, only manual tracking entry is available."
    )

    default_shipping_provider = models.ForeignKey(
        'shipping.ProviderAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_for_site',
        verbose_name=_("Default Shipping Provider"),
        help_text="Default API provider for shipping label generation (e.g., Easyship, ShipEngine)"
    )

    default_manual_carrier = models.ForeignKey(
        'shipping.CarrierPreset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_for_site',
        verbose_name=_("Default Manual Carrier"),
        help_text="Default carrier for manual tracking entry (e.g., DHL Express, FedEx)"
    )

    shipping_origin_country = models.CharField(
        max_length=2,
        default='US',
        verbose_name=_("Shipping Origin Country"),
        help_text="Two-letter country code (ISO 3166-1 alpha-2) for your primary shipping location"
    )

    # Unit System Settings
    WEIGHT_UNIT_CHOICES = [
        ('g', 'Grams (g)'),
        ('kg', 'Kilograms (kg)'),
        ('oz', 'Ounces (oz)'),
        ('lb', 'Pounds (lb)'),
    ]

    LENGTH_UNIT_CHOICES = [
        ('mm', 'Millimeters (mm)'),
        ('cm', 'Centimeters (cm)'),
        ('m', 'Meters (m)'),
        ('in', 'Inches (in)'),
        ('ft', 'Feet (ft)'),
    ]

    VOLUME_UNIT_CHOICES = [
        ('ml', 'Milliliters (ml)'),
        ('l', 'Liters (l)'),
        ('cl', 'Centiliters (cl)'),
        ('dl', 'Deciliters (dl)'),
        ('fl_oz', 'Fluid Ounces (fl oz)'),
        ('cup', 'Cups'),
        ('pt', 'Pints (pt)'),
        ('qt', 'Quarts (qt)'),
        ('gal', 'Gallons (gal)'),
    ]

    AREA_UNIT_CHOICES = [
        ('sq_mm', 'Square Millimeters (mm²)'),
        ('sq_cm', 'Square Centimeters (cm²)'),
        ('sq_m', 'Square Meters (m²)'),
        ('sq_in', 'Square Inches (in²)'),
        ('sq_ft', 'Square Feet (ft²)'),
        ('sq_yd', 'Square Yards (yd²)'),
    ]

    TEMPERATURE_UNIT_CHOICES = [
        ('c', 'Celsius (°C)'),
        ('f', 'Fahrenheit (°F)'),
        ('k', 'Kelvin (K)'),
    ]

    default_weight_unit = models.CharField(
        max_length=5,
        choices=WEIGHT_UNIT_CHOICES,
        default='kg',
        verbose_name=_("Default Weight Unit"),
        help_text="Unit of measurement for product weights in the admin interface"
    )

    default_length_unit = models.CharField(
        max_length=5,
        choices=LENGTH_UNIT_CHOICES,
        default='cm',
        verbose_name=_("Default Length Unit"),
        help_text="Unit of measurement for product dimensions (length, width, height) in the admin interface"
    )

    default_volume_unit = models.CharField(
        max_length=5,
        choices=VOLUME_UNIT_CHOICES,
        default='ml',
        verbose_name=_("Default Volume Unit"),
        help_text="Unit of measurement for liquid volumes and bulk products (e.g., beverages, oils, cleaning supplies)"
    )

    default_area_unit = models.CharField(
        max_length=5,
        choices=AREA_UNIT_CHOICES,
        default='sq_m',
        verbose_name=_("Default Area Unit"),
        help_text="Unit of measurement for area (e.g., flooring, fabric, wallpaper)"
    )

    default_temperature_unit = models.CharField(
        max_length=1,
        choices=TEMPERATURE_UNIT_CHOICES,
        default='c',
        verbose_name=_("Default Temperature Unit"),
        help_text="Unit of measurement for temperature (e.g., electronics, climate-controlled products)"
    )

    enable_unit_conversion = models.BooleanField(
        default=True,
        verbose_name=_("Enable Unit Conversion for Customers"),
        help_text="Automatically convert measurements for international customers based on their location (e.g., US customers see lb/in/°F, EU customers see kg/cm/°C)"
    )

    # Translations - JSON-based multilingual content
    # Structure: {
    #   "en": {
    #     "site_name": "My Store",
    #     "site_tagline": "Quality Products",
    #     "site_description": "...",
    #     "meta_title": "...",
    #     "meta_description": "...",
    #     "meta_keywords": "...",
    #     "maintenance_message": "..."
    #   },
    #   "es": { ... },
    #   ...
    # }
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text="Translations for site content (name, tagline, description, SEO fields) in different languages"
    )

    # Community / SSO Integration
    community_merchant_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Unique merchant identifier for community services (auto-generated on first use)"
    )

    community_client_secret = models.CharField(
        max_length=128,
        blank=True,
        help_text="Client secret for community SSO authentication (encrypted)"
    )

    community_registered_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this store was registered with community services"
    )

    # ============================================================================
    # Two-Factor Authentication Enforcement Settings
    # ============================================================================
    STAFF_2FA_ENFORCEMENT_CHOICES = [
        ('disabled', _('Optional - Staff can choose to enable 2FA')),
        ('recommended', _('Recommended - Prompt staff to enable 2FA')),
        ('required', _('Required - Staff must enable 2FA to access admin')),
    ]

    staff_2fa_enforcement = models.CharField(
        max_length=20,
        choices=STAFF_2FA_ENFORCEMENT_CHOICES,
        default='disabled',
        verbose_name=_("Staff 2FA Enforcement"),
        help_text=_("Control whether two-factor authentication is required for admin access")
    )

    staff_2fa_grace_period_days = models.PositiveIntegerField(
        default=7,
        verbose_name=_("2FA Setup Grace Period (Days)"),
        help_text=_("Days allowed for staff to set up 2FA after enforcement is enabled. Set to 0 for immediate enforcement.")
    )

    staff_2fa_enforcement_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("2FA Enforcement Start Date"),
        help_text=_("When 2FA enforcement was enabled. Used to calculate grace period expiration.")
    )

    allow_trusted_devices = models.BooleanField(
        default=True,
        verbose_name=_("Allow Trusted Devices"),
        help_text=_("Allow users to mark devices as trusted to skip 2FA for a period")
    )

    trusted_device_duration_days = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Trusted Device Duration (Days)"),
        help_text=_("How long a device stays trusted after 'Remember this device' is selected")
    )

    # ============================================================================
    # Admin SSO Settings
    # ============================================================================
    admin_sso_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Enable SSO for Admin Login"),
        help_text=_("Show enterprise SSO button on the admin login page")
    )
    admin_password_login_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Allow Password Login"),
        help_text=_("Allow password-based login on the admin page. Disable to enforce SSO-only access.")
    )

    # ============================================================================
    # Mobile App Security Settings
    # ============================================================================
    max_devices_per_user = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Maximum Devices Per User"),
        help_text=_("Maximum number of mobile devices each staff member can have registered simultaneously. "
                    "Set to 0 for unlimited devices.")
    )

    # ============================================================================
    # Page Assignments
    # ============================================================================
    # System page assignments (functional pages)
    home_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Home Page"),
        help_text=_("The main landing page of your store")
    )
    # Legal/policy page assignments
    privacy_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Privacy Policy Page"),
        help_text=_("Your store's privacy policy")
    )
    terms_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Terms of Use Page"),
        help_text=_("Your store's terms of service/use")
    )
    cookie_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Cookie Policy Page"),
        help_text=_("Your store's cookie policy")
    )
    shipping_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Shipping Information Page"),
        help_text=_("Shipping policies and delivery information")
    )
    returns_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Returns Policy Page"),
        help_text=_("Return and refund policies")
    )

    # ============================================================================
    # Cookie Consent Settings
    # ============================================================================
    cookie_consent_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Enable Cookie Consent Banner"),
        help_text=_("Show a GDPR-compliant cookie consent banner to visitors.")
    )

    COOKIE_BANNER_POSITION_CHOICES = [
        ('bottom', _('Bottom Bar')),
        ('bottom-left', _('Bottom Left')),
        ('bottom-right', _('Bottom Right')),
    ]

    cookie_banner_position = models.CharField(
        max_length=20,
        choices=COOKIE_BANNER_POSITION_CHOICES,
        default='bottom',
        verbose_name=_("Banner Position"),
        help_text=_("Where to display the cookie consent banner on screen.")
    )

    COOKIE_CONSENT_MODE_CHOICES = [
        ('simple', _('Simple — Accept / Reject only')),
        ('granular', _('Granular — Per-category control')),
    ]

    cookie_consent_mode = models.CharField(
        max_length=10,
        choices=COOKIE_CONSENT_MODE_CHOICES,
        default='granular',
        verbose_name=_("Consent Mode"),
        help_text=_("'Simple' shows Accept/Reject buttons only. "
                    "'Granular' adds a Manage Preferences option for per-category control.")
    )

    cookie_banner_title = models.CharField(
        max_length=200,
        default='',
        blank=True,
        verbose_name=_("Banner Title"),
        help_text=_("Short heading for the cookie banner. Supports translations.")
    )

    cookie_banner_text = models.TextField(
        default='',
        blank=True,
        verbose_name=_("Banner Description"),
        help_text=_("Main body text explaining cookie usage. Supports translations.")
    )

    cookie_analytics_description = models.TextField(
        default='',
        blank=True,
        verbose_name=_("Analytics Cookies Description"),
        help_text=_("Describe what analytics cookies do (shown in granular mode). Supports translations.")
    )

    cookie_marketing_description = models.TextField(
        default='',
        blank=True,
        verbose_name=_("Marketing Cookies Description"),
        help_text=_("Describe what marketing cookies do (shown in granular mode). Supports translations.")
    )

    cookie_functional_description = models.TextField(
        default='',
        blank=True,
        verbose_name=_("Functional Cookies Description"),
        help_text=_("Describe what functional cookies do (shown in granular mode). Supports translations.")
    )

    # Error pages
    error_404_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("404 Error Page"),
        help_text=_("Custom page for 'page not found' errors")
    )
    error_500_page = models.ForeignKey(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("500 Error Page"),
        help_text=_("Custom page for server errors")
    )

    # ============================================================================
    # Image Processing Settings
    # ============================================================================
    IMAGE_RESIZE_MODE_CHOICES = [
        ('cover', _('Cover - Fill dimensions (crops if needed)')),
        ('contain', _('Contain - Fit within dimensions')),
        ('pad', _('Pad - Fit and add padding (preserves all content)')),
    ]

    PADDING_COLOR_CHOICES = [
        ('transparent', _('Transparent')),
        ('white', _('White')),
        ('black', _('Black')),
    ]

    default_image_resize_mode = models.CharField(
        max_length=20,
        choices=IMAGE_RESIZE_MODE_CHOICES,
        default='cover',
        verbose_name=_("Default Image Resize Mode"),
        help_text=_("How images are resized when generating thumbnails. 'Cover' crops to fill dimensions, 'Contain' fits within dimensions, 'Pad' preserves all content with padding.")
    )

    default_padding_color = models.CharField(
        max_length=20,
        choices=PADDING_COLOR_CHOICES,
        default='transparent',
        verbose_name=_("Default Padding Color"),
        help_text=_("Background color for padding when using 'Pad' resize mode. Transparent works best for logos.")
    )

    logo_resize_mode = models.CharField(
        max_length=20,
        choices=IMAGE_RESIZE_MODE_CHOICES,
        default='pad',
        verbose_name=_("Logo Resize Mode"),
        help_text=_("How logos are resized. 'Pad' is recommended to preserve full logo content.")
    )

    logo_padding_color = models.CharField(
        max_length=20,
        choices=PADDING_COLOR_CHOICES,
        default='transparent',
        verbose_name=_("Logo Padding Color"),
        help_text=_("Background color for logo padding. Transparent preserves the logo background.")
    )

    # Communication Preferences Settings
    enable_double_opt_in = models.BooleanField(
        default=True,
        verbose_name=_("Enable Double Opt-In for Marketing Emails"),
        help_text=_("Require customers to verify their email address before receiving marketing communications (GDPR compliance)")
    )

    default_marketing_opt_in = models.BooleanField(
        default=False,
        verbose_name=_("Default Marketing Opt-In State"),
        help_text=_("Default opt-in state for marketing emails during registration (False = opt-out per GDPR best practices)")
    )

    preference_center_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Enable Customer Preference Center"),
        help_text=_("Allow customers to manage their communication preferences via account dashboard")
    )

    require_sms_verification = models.BooleanField(
        default=False,
        verbose_name=_("Require SMS Verification"),
        help_text=_("Send verification code before enabling SMS notifications (recommended for TCPA compliance)")
    )

    show_unsubscribe_reasons = models.BooleanField(
        default=True,
        verbose_name=_("Collect Unsubscribe Reasons"),
        help_text=_("Ask customers why they're unsubscribing (helps improve communication strategy)")
    )

    # Geocoder Service Settings
    geocoder_installation_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Geocoder Installation UUID"),
        help_text=_("Unique identifier for this installation used for geocoder service authentication")
    )

    # Installation tracking (for license grace period)
    installed_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Installation Date"),
        help_text=_("When this platform was first installed. Set automatically on first run.")
    )
    installation_fingerprint = models.CharField(
        max_length=64,
        blank=True,
        editable=False,
        verbose_name=_("Installation Fingerprint"),
        help_text=_("Tamper-detection hash of installation date.")
    )

    # ============================================================================
    # Inventory Intelligence Settings (used by Admin API inventory endpoints)
    # ============================================================================
    LOW_STOCK_ALERT_FREQUENCY_CHOICES = [
        ('realtime', _('Real-time (on each stock change)')),
        ('daily', _('Daily Digest')),
        ('weekly', _('Weekly Summary')),
    ]

    low_stock_alert_frequency = models.CharField(
        max_length=10,
        choices=LOW_STOCK_ALERT_FREQUENCY_CHOICES,
        default='daily',
        verbose_name=_("Low Stock Alert Frequency"),
        help_text=_("How often to send low stock alert notifications")
    )

    allow_backorders_by_default = models.BooleanField(
        default=False,
        verbose_name=_("Allow Backorders by Default"),
        help_text=_("Allow customers to order products even when out of stock (new products inherit this setting)")
    )

    default_reorder_lead_days = models.PositiveIntegerField(
        default=14,
        verbose_name=_("Default Reorder Lead Time (Days)"),
        help_text=_("Default number of days it takes to receive restock from supplier")
    )

    safety_stock_multiplier = models.FloatField(
        default=1.5,
        verbose_name=_("Safety Stock Multiplier"),
        help_text=_("Multiplier applied to velocity for safety stock calculation (e.g., 1.5 means 50%% buffer)")
    )

    velocity_calculation_window_days = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Velocity Calculation Window (Days)"),
        help_text=_("Number of days to look back when calculating product sales velocity")
    )

    # ============================================================================
    # Document / Invoice Settings (used by Admin API document generation)
    # ============================================================================
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Tax ID / VAT Number"),
        help_text=_("Business tax identification number shown on invoices")
    )

    invoice_footer_text = models.TextField(
        blank=True,
        verbose_name=_("Invoice Footer Text"),
        help_text=_("Custom text displayed at the bottom of generated invoices (e.g., payment terms, thank you message)")
    )

    packing_slip_footer_text = models.TextField(
        blank=True,
        verbose_name=_("Packing Slip Footer Text"),
        help_text=_("Custom text displayed at the bottom of packing slips (e.g., return instructions)")
    )

    document_logo_width = models.PositiveIntegerField(
        default=200,
        verbose_name=_("Document Logo Width (px)"),
        help_text=_("Width of the logo in generated PDF documents (invoices, packing slips). Height scales proportionally.")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return f"Site Settings for {self.site_name}"

    def clean(self):
        """
        Validate site settings fields.
        Prevents disabling multi-warehouse mode if multiple warehouses exist.
        """
        from django.core.exceptions import ValidationError
        from django.urls import reverse
        from django.utils.safestring import mark_safe
        from django.utils.html import escape

        super().clean()

        # Validate multi-warehouse disable attempt
        if not self.enable_multi_warehouse:
            # Import here to avoid circular imports
            from catalog.models import Warehouse

            # Get all active warehouses excluding the main warehouse
            non_main_warehouses = Warehouse.objects.filter(is_active=True).exclude(code='MAIN-WH')

            if non_main_warehouses.exists():
                # Check if any non-main warehouse has stock
                warehouses_with_stock = []
                affected_products = []  # Collect (product_id, product_name) tuples

                for warehouse in non_main_warehouses:
                    # Check if warehouse has any stock items with on_hand > 0
                    stock_items = warehouse.stock_items.filter(on_hand__gt=0).select_related('product')
                    if stock_items.exists():
                        warehouses_with_stock.append(warehouse)
                        # Collect affected products (avoid duplicates)
                        for item in stock_items[:20]:  # Limit per warehouse
                            if item.product_id not in [p[0] for p in affected_products]:
                                affected_products.append((item.product_id, item.product.name))

                if warehouses_with_stock:
                    # Build error message showing warehouses with stock
                    warehouse_details = []
                    for wh in warehouses_with_stock[:5]:  # Show max 5
                        stock_count = wh.stock_items.filter(on_hand__gt=0).count()
                        warehouse_details.append(f"{escape(wh.name)} ({escape(wh.code)}): {stock_count} product(s)")

                    warehouse_list = ', '.join(warehouse_details)

                    if len(warehouses_with_stock) > 5:
                        warehouse_list += f", ...and {len(warehouses_with_stock) - 5} more"

                    # Build product links HTML
                    product_links = []
                    for product_id, product_name in affected_products[:10]:
                        url = reverse('admin:catalog_product_change', args=[product_id])
                        product_links.append(
                            f'<a href="{url}" target="_blank" rel="noopener" '
                            f'style="color: var(--link-fg, #417690); text-decoration: underline;">'
                            f'{escape(product_name)}</a>'
                        )

                    products_html = ', '.join(product_links)
                    if len(affected_products) > 10:
                        products_html += f", ...and {len(affected_products) - 10} more products"

                    # Create rich error message with product links
                    error_msg = mark_safe(
                        f"Cannot disable multi-warehouse mode. "
                        f"{len(warehouses_with_stock)} warehouse(s) still have inventory: {warehouse_list}."
                        f"<br><br><strong>Affected Products:</strong> {products_html}"
                        f"<br><br>You must first consolidate all stock into the main warehouse (MAIN-WH) "
                        f"and delete or deactivate all other warehouses before disabling multi-warehouse mode."
                    )

                    raise ValidationError({
                        'enable_multi_warehouse': error_msg
                    })

                # Has non-main warehouses but no stock - still require deletion
                else:
                    warehouse_names = [f"{escape(wh.name)} ({escape(wh.code)})" for wh in non_main_warehouses[:5]]
                    warehouse_list = ', '.join(warehouse_names)

                    if non_main_warehouses.count() > 5:
                        warehouse_list += f", ...and {non_main_warehouses.count() - 5} more"

                    raise ValidationError({
                        'enable_multi_warehouse': (
                            f"Cannot disable multi-warehouse mode. "
                            f"{non_main_warehouses.count()} warehouse(s) still exist: {warehouse_list}. "
                            f"Please delete or deactivate all warehouses except the main warehouse (MAIN-WH) "
                            f"before disabling multi-warehouse mode."
                        )
                    })

        # Validate account creation timing constraints
        if hasattr(self, 'account_creation_timing') and hasattr(self, 'allow_guest_checkout'):
            if self.account_creation_timing == 'post_purchase' and not self.allow_guest_checkout:
                raise ValidationError({
                    'account_creation_timing': _(
                        "Post-purchase account creation requires 'Allow Guest Checkout' to be enabled. "
                        "Enable guest checkout or choose a different account creation timing."
                    )
                })

        # Validate multi-currency disable attempt
        if not self.enable_multi_currency:
            from orders.models import Order

            # Check if any orders were placed in a non-default currency
            multi_currency_orders = Order.objects.exclude(
                customer_currency__in=['', None, self.default_currency]
            )

            if multi_currency_orders.exists():
                order_count = multi_currency_orders.count()
                currencies_used = [
                    c for c in multi_currency_orders.values_list('customer_currency', flat=True)
                    .distinct()[:5]
                    if c
                ]
                currencies_str = ', '.join(currencies_used)
                if multi_currency_orders.values('customer_currency').distinct().count() > 5:
                    currencies_str += ', ...'

                raise ValidationError({
                    'enable_multi_currency': mark_safe(
                        f"Cannot disable multi-currency. "
                        f"{order_count} order(s) have been processed in foreign currencies "
                        f"({currencies_str}). "
                        f"These orders permanently retain their currency and exchange rate data."
                        f"<br><br>Multi-currency cannot be disabled once orders exist in "
                        f"multiple currencies."
                    )
                })

        # Validate multi-currency enablement prerequisites
        if self.enable_multi_currency:
            from exchange_rates.models import ExchangeRateProviderAccount, ManualExchangeRate
            from django.contrib.sites.models import Site

            site = Site.objects.get(pk=1)
            active_providers = ExchangeRateProviderAccount.objects.filter(
                site=site,
                is_active=True
            )
            has_manual_rates = ManualExchangeRate.objects.filter(
                site=site,
                is_active=True
            ).exists()

            if not active_providers.exists() and not has_manual_rates:
                raise ValidationError({
                    'enable_multi_currency': _(
                        "Cannot enable multi-currency without at least one active exchange rate source. "
                        "Please configure an exchange rate provider or add manual exchange rates "
                        "in the Exchange Rate settings, then return here to enable multi-currency."
                    )
                })

            # If strategy is 'primary', validate a primary provider exists
            # (only relevant when using provider-based rates)
            if self.exchange_rate_selection_strategy == 'primary' and active_providers.exists():
                if not active_providers.filter(is_primary=True).exists():
                    raise ValidationError({
                        'exchange_rate_selection_strategy': _(
                            "Rate selection strategy is set to 'Primary Provider' but no provider "
                            "is marked as primary. Either set a provider as primary or change the "
                            "strategy to 'Latest Available Rate'."
                        )
                    })

            # Validate supported_currencies has at least 2 currencies if specified
            if self.supported_currencies and len(self.supported_currencies) < 2:
                raise ValidationError({
                    'supported_currencies': _(
                        "When multi-currency is enabled, please include at least 2 currencies "
                        "(your base currency plus at least one additional currency)."
                    )
                })

            # Validate default_currency is in supported_currencies if list is non-empty
            if self.supported_currencies and self.default_currency not in self.supported_currencies:
                raise ValidationError({
                    'supported_currencies': _(
                        "Your default currency (%(default)s) must be included in the supported currencies list."
                    ) % {'default': self.default_currency}
                })

    def compute_installation_fingerprint(self):
        """Compute HMAC of installation date using SECRET_KEY to detect tampering."""
        import hmac
        import hashlib
        from django.conf import settings
        if not self.installed_at:
            return ''
        payload = f"{self.installed_at.isoformat()}:{self.pk}:{self.geocoder_installation_uuid}"
        return hmac.new(
            settings.SECRET_KEY.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    def verify_installation_fingerprint(self):
        """Returns True if the stored fingerprint matches the computed one."""
        import hmac as hmac_mod
        if not self.installed_at or not self.installation_fingerprint:
            return False
        return hmac_mod.compare_digest(
            self.installation_fingerprint,
            self.compute_installation_fingerprint()
        )

    def stamp_installation_date(self):
        """Set installed_at if not already set and compute fingerprint."""
        if not self.installed_at:
            self.installed_at = timezone.now()
            self.installation_fingerprint = self.compute_installation_fingerprint()
            SiteSettings.objects.filter(pk=self.pk).update(
                installed_at=self.installed_at,
                installation_fingerprint=self.installation_fingerprint,
            )

    def save(self, *args, **kwargs):
        """
        Ensure only one instance of SiteSettings exists (singleton pattern)
        """
        # Call clean() to run validation unless explicitly skipped
        if not kwargs.pop('skip_validation', False):
            self.full_clean()

        if not self.pk and SiteSettings.objects.exists():
            # If trying to create a new instance but one already exists, update the existing one
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        elif not self.pk:
            # If this is the first instance, force ID to 1
            self.pk = 1

        # Auto-compute installation fingerprint if installed_at is set but fingerprint is empty
        if self.installed_at and not self.installation_fingerprint:
            self.installation_fingerprint = self.compute_installation_fingerprint()

        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """
        Get the current site settings instance, creating one if it doesn't exist
        """
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    @classmethod
    def get_installation_uuid(cls):
        """
        Get the installation UUID for geocoder service authentication.
        Creates the settings instance if it doesn't exist and returns the UUID.
        """
        settings = cls.get_settings()
        return str(settings.geocoder_installation_uuid)

    @property
    def effective_account_creation_message(self):
        """Get account creation message in current language with fallback"""
        from django.utils.translation import get_language

        default = _("Create an account to track your order, save addresses, and enjoy faster checkout next time!")

        if not self.account_creation_message:
            return default

        current_lang = get_language()
        # Check translations JSONField for non-primary language
        if current_lang and current_lang != 'en':
            translated = (self.translations or {}).get(current_lang, {})
            if isinstance(translated, dict):
                text = translated.get('account_creation_message', '')
                if text:
                    return text
        # Fall back to TextField value (primary/default language)
        return self.account_creation_message or default

    def get_full_address(self):
        """
        Return the full formatted address
        """
        address_parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state_province,
            self.postal_code,
            self.country
        ]
        return ', '.join([part for part in address_parts if part])
    
    def get_support_email(self):
        """
        Return support email if set, otherwise return admin email
        """
        return self.support_email if self.support_email else self.admin_email

    def get_page_for_role(self, role):
        """
        Get the assigned page for a specific role, with fallback to default.

        Args:
            role: The page role (e.g., 'home', 'privacy', 'terms', etc.)

        Returns:
            Page instance if found and published, None otherwise
        """
        # Map role names to field names
        role_field_mapping = {
            'home': 'home_page',
            'privacy': 'privacy_page',
            'terms': 'terms_page',
            'cookie': 'cookie_page',
            'shipping': 'shipping_page',
            'returns': 'returns_page',
            '404': 'error_404_page',
            '500': 'error_500_page',
        }

        # Get the field name for this role
        page_field = role_field_mapping.get(role, f'{role}_page')

        # Get the assigned page
        assigned = getattr(self, page_field, None)
        if assigned and assigned.status == 'published':
            return assigned

        # Fallback: Find default page for this type
        from page_builder.models import Page

        # Map role to page_type
        role_to_page_type = {
            'home': 'home',
            'cart': 'cart',
            'checkout': 'checkout',
            'privacy': 'custom',
            'terms': 'custom',
            'cookie': 'custom',
            'shipping': 'custom',
            'returns': 'custom',
            'account': 'custom',
            '404': 'custom',
            '500': 'custom',
        }
        page_type = role_to_page_type.get(role, role)

        return Page.objects.filter(
            page_type=page_type,
            is_default_for_type=True,
            status='published'
        ).first()

    def get_legal_pages(self):
        """
        Get all assigned legal pages for footer display.

        Returns:
            Dictionary with role names and their assigned pages (if published)
        """
        legal_roles = ['privacy', 'terms', 'cookie', 'shipping', 'returns']
        return {
            role: self.get_page_for_role(role)
            for role in legal_roles
        }

    def get_cookie_consent_context(self, language_code='en'):
        """
        Return resolved cookie consent data for the active language,
        ready for use in the cookie banner template.
        """
        def resolve(field_name):
            # Check translations JSONField for non-primary language
            if language_code and language_code != 'en':
                translated = (self.translations or {}).get(language_code, {})
                if isinstance(translated, dict):
                    text = translated.get(field_name, '')
                    if text:
                        return text
            # Fall back to CharField value (primary/default language)
            return getattr(self, field_name, '') or ''

        policy_url = ''
        if self.cookie_page:
            from django.urls import reverse
            try:
                policy_url = reverse('page_builder:page_detail', kwargs={'slug': self.cookie_page.slug})
            except Exception:
                policy_url = ''

        return {
            'enabled': self.cookie_consent_enabled,
            'position': self.cookie_banner_position,
            'mode': self.cookie_consent_mode,
            'title': resolve('cookie_banner_title'),
            'text': resolve('cookie_banner_text'),
            'analytics_desc': resolve('cookie_analytics_description'),
            'marketing_desc': resolve('cookie_marketing_description'),
            'functional_desc': resolve('cookie_functional_description'),
            'policy_url': policy_url,
        }

    def get_favicon_url(self):
        """
        Return favicon URL if set, otherwise return None
        """
        if not self.favicon:
            return None
        # Prefer original file, fall back to webp
        if self.favicon.original_file:
            return self.favicon.original_file.url
        elif self.favicon.webp_file:
            return self.favicon.webp_file.url
        return None

    def get_site_logo_url(self, size=None):
        """
        Return site logo URL at specified size.

        Args:
            size: Optional size preset ('header', 'footer', 'email', 'square', or 'original')
                  If None or 'original', returns the original/webp file.

        Returns:
            URL string or None
        """
        if not self.site_logo:
            return None

        # SVG files don't need thumbnails - return original
        if self.site_logo.mime_type == 'image/svg+xml':
            if self.site_logo.original_file:
                return self.site_logo.original_file.url
            return None

        # For raster images, try to get appropriate thumbnail
        if size and size != 'original':
            size_mapping = {
                'header': 'logo_header',
                'footer': 'logo_footer',
                'email': 'logo_email',
                'square': 'logo_square',
            }
            preset_name = size_mapping.get(size)
            if preset_name:
                thumbnail_url = self.site_logo.get_thumbnail(preset_name)
                if thumbnail_url:
                    return thumbnail_url

        # Fallback to webp or original
        if self.site_logo.webp_file:
            return self.site_logo.webp_file.url
        elif self.site_logo.original_file:
            return self.site_logo.original_file.url
        return None


class LicenseStatus(models.Model):
    """
    Virtual model for license status admin interface.
    This is a proxy/unmanaged model used only for displaying license status in Django admin.
    No database table is created for this model.
    """

    class Meta:
        managed = False  # Don't create database table
        verbose_name = _('License Status')
        verbose_name_plural = _('License Status')
        app_label = 'core'

    def __str__(self):
        return "Platform License Status"


class LicenseAcceptanceRecord(models.Model):
    """
    Audit trail for Software License Agreement acceptances.
    Records each time a merchant accepts (or re-accepts) the license.
    """

    license_version = models.CharField(
        max_length=20,
        verbose_name=_("License Version"),
    )
    software_version = models.CharField(
        max_length=20,
        verbose_name=_("Software Version"),
    )
    accepted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Accepted At"),
    )
    accepted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Accepted By"),
    )
    accepted_by_email = models.EmailField(
        blank=True,
        verbose_name=_("Accepted By Email"),
    )
    accepted_via = models.CharField(
        max_length=20,
        verbose_name=_("Acceptance Method"),
        help_text=_("How the license was accepted: web, cli, or env"),
    )
    installation_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_("Installation ID"),
    )
    license_checksum = models.CharField(
        max_length=74,
        verbose_name=_("License Checksum"),
        help_text=_("SHA-256 checksum of the accepted LICENSE.txt"),
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address"),
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name=_("Is Current"),
        help_text=_("Whether this is the most recent acceptance record"),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
    )

    class Meta:
        verbose_name = _('License Acceptance Record')
        verbose_name_plural = _('License Acceptance Records')
        ordering = ['-accepted_at']

    def __str__(self):
        return f"License v{self.license_version} accepted at {self.accepted_at}"


# Import SupportedCurrency model
from core.supported_currency_model import SupportedCurrency  # noqa: E402, F401


# ============================================================================
# License Revocation Tracking
# ============================================================================

class LicenseRevocation(models.Model):
    """
    Tracks when a license revocation is detected during periodic refresh.

    When the update server reports that a license has been deactivated or
    expired, a revocation record is created with a grace period. The shop
    continues operating during the grace period, showing a warning banner
    in the admin dashboard. After grace expires, the license is treated
    as invalid.

    If a subsequent refresh confirms the license is valid again (e.g.
    merchant renewed), all revocation records are deleted.
    """
    detected_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)
    grace_expires_at = models.DateTimeField(
        help_text="Shop continues operating until this date"
    )
    acknowledged = models.BooleanField(
        default=False,
        help_text="Merchant dismissed the warning banner"
    )

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f"Revocation: {self.reason} (grace until {self.grace_expires_at})"

    @property
    def is_in_grace_period(self):
        return timezone.now() < self.grace_expires_at

    @property
    def grace_days_remaining(self):
        remaining = (self.grace_expires_at - timezone.now()).days
        return max(0, remaining)


# ============================================================================
# Help System Models
# ============================================================================

class HelpCategory(models.Model):
    """Help topic categories for organization"""

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    icon = models.CharField(
        max_length=50,
        help_text=_("Font Awesome icon class (e.g., 'fa-box')"),
        verbose_name=_("Icon")
    )
    order = models.IntegerField(default=0, verbose_name=_("Display Order"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    translations = models.JSONField(
        default=dict, blank=True,
        help_text=_("Translated name/description by language code, e.g. {'es': {'name': '...'}}"),
        verbose_name=_("Translations")
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _("Help Category")
        verbose_name_plural = _("Help Categories")

    def __str__(self):
        return self.name


class HelpTopic(models.Model):
    """Individual help topics/articles"""

    # Identity
    slug = models.SlugField(
        unique=True,
        help_text=_("Unique identifier (e.g., 'catalog__products-create')"),
        verbose_name=_("Slug")
    )
    category = models.ForeignKey(
        HelpCategory,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name=_("Category")
    )

    # Content
    title_i18n_key = models.CharField(
        max_length=200,
        help_text=_("Translation key for title (e.g., 'help.catalog.products_create.title')"),
        verbose_name=_("Title i18n Key")
    )
    content_markdown = models.TextField(
        help_text=_("Markdown content with {% trans %} tags for translations"),
        verbose_name=_("Content (Markdown)")
    )

    # Version awareness
    component = models.CharField(
        max_length=50,
        help_text=_("Component name (e.g., 'catalog', 'shipping')"),
        verbose_name=_("Component")
    )
    min_version = models.CharField(
        max_length=20,
        blank=True,
        help_text=_("Minimum component version (e.g., '1.8.0')"),
        verbose_name=_("Minimum Version")
    )
    max_version = models.CharField(
        max_length=20,
        blank=True,
        help_text=_("Maximum component version (e.g., '2.0.0')"),
        verbose_name=_("Maximum Version")
    )

    # Metadata
    keywords = models.JSONField(
        default=list,
        help_text=_("Search keywords (JSON array)"),
        verbose_name=_("Keywords")
    )
    related_topics = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='related_to',
        verbose_name=_("Related Topics")
    )
    url_patterns = models.JSONField(
        default=list,
        help_text=_("URL regex patterns where this help is contextual (JSON array)"),
        verbose_name=_("URL Patterns")
    )

    # Statistics
    view_count = models.IntegerField(
        default=0,
        verbose_name=_("View Count")
    )
    helpful_count = models.IntegerField(
        default=0,
        verbose_name=_("Helpful Count")
    )
    not_helpful_count = models.IntegerField(
        default=0,
        verbose_name=_("Not Helpful Count")
    )

    # Admin
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    is_published = models.BooleanField(
        default=True,
        help_text=_("Only published topics are visible to users"),
        verbose_name=_("Published")
    )
    translations = models.JSONField(
        default=dict, blank=True,
        help_text=_("Translated content by language code, e.g. {'es': {'title': '...', 'content': '...'}}"),
        verbose_name=_("Translations")
    )

    class Meta:
        ordering = ['component', 'category', 'slug']
        verbose_name = _("Help Topic")
        verbose_name_plural = _("Help Topics")
        indexes = [
            models.Index(fields=['component', 'is_published']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.component}: {self.slug}"

    @property
    def helpfulness_percentage(self):
        """Calculate percentage of helpful feedback"""
        total = self.helpful_count + self.not_helpful_count
        if total == 0:
            return None
        return (self.helpful_count / total) * 100


class HelpFeedback(models.Model):
    """User feedback on help topics"""

    topic = models.ForeignKey(
        HelpTopic,
        on_delete=models.CASCADE,
        related_name='feedback',
        verbose_name=_("Topic")
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    helpful = models.BooleanField(
        help_text=_("True = helpful, False = not helpful"),
        verbose_name=_("Helpful")
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("Comment")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Help Feedback")
        verbose_name_plural = _("Help Feedback")

    def __str__(self):
        helpful_text = _("helpful") if self.helpful else _("not helpful")
        return f"{self.topic.slug} - {helpful_text}"


class HelpView(models.Model):
    """Anonymous telemetry for help usage (opt-in)"""

    topic = models.ForeignKey(
        HelpTopic,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name=_("Topic")
    )
    session_id = models.CharField(
        max_length=100,
        help_text=_("Anonymous session identifier"),
        verbose_name=_("Session ID")
    )
    viewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Viewed At")
    )
    context_url = models.CharField(
        max_length=500,
        blank=True,
        help_text=_("URL where help was opened from"),
        verbose_name=_("Context URL")
    )

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = _("Help View")
        verbose_name_plural = _("Help Views")
        indexes = [
            models.Index(fields=['topic', 'viewed_at']),
        ]

    def __str__(self):
        return f"{self.topic.slug} - {self.viewed_at}"


class HelpSearchIndex(models.Model):
    """
    Vector search index for help topics with semantic embeddings.
    Stores document chunks with embeddings for fast similarity search.
    """

    # Relationship
    topic = models.ForeignKey(
        HelpTopic,
        on_delete=models.CASCADE,
        related_name='search_chunks',
        verbose_name=_("Help Topic"),
        db_index=True
    )

    # Language tracking
    language = models.CharField(
        max_length=10,
        default='en',
        verbose_name=_("Language Code"),
        help_text=_("ISO language code (e.g., 'en', 'es', 'zh-hans')"),
        db_index=True
    )

    # Content chunks
    chunk_text = models.TextField(
        verbose_name=_("Chunk Text"),
        help_text=_("Text segment from help topic (512 chars with 50 char overlap)")
    )
    chunk_position = models.PositiveIntegerField(
        verbose_name=_("Chunk Position"),
        help_text=_("Sequential position of this chunk in the document (0-indexed)")
    )

    # Vector embedding (384 dimensions for all-MiniLM-L6-v2)
    embedding = VectorField(
        dimensions=384,
        verbose_name=_("Embedding Vector"),
        help_text=_("384-dimensional embedding from sentence-transformers")
    )

    # Metadata for ranking
    is_title_chunk = models.BooleanField(
        default=False,
        verbose_name=_("Is Title Chunk"),
        help_text=_("True if this chunk contains the topic title")
    )
    contains_keywords = models.BooleanField(
        default=False,
        verbose_name=_("Contains Keywords"),
        help_text=_("True if this chunk contains topic keywords")
    )

    # Timestamps
    indexed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Indexed At"),
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        ordering = ['topic', 'language', 'chunk_position']
        verbose_name = _("Help Search Index")
        verbose_name_plural = _("Help Search Indexes")
        indexes = [
            models.Index(fields=['topic', 'language']),
            models.Index(fields=['language', 'indexed_at']),
        ]

    def __str__(self):
        return f"{self.topic.slug} [{self.language}] chunk {self.chunk_position}"


class APIToken(models.Model):
    """
    API Token model for external integrations and services

    Merchants can generate API tokens for various purposes:
    - Help System documentation discovery
    - External integrations
    - Third-party service authentication
    - Webhook callbacks
    """

    TOKEN_TYPE_HELP_SYSTEM = 'help_system'
    TOKEN_TYPE_INTEGRATION = 'integration'
    TOKEN_TYPE_WEBHOOK = 'webhook'
    TOKEN_TYPE_CUSTOM = 'custom'
    TOKEN_TYPE_SYNC = 'sync'

    TOKEN_TYPE_CHOICES = [
        (TOKEN_TYPE_HELP_SYSTEM, _('Help System')),
        (TOKEN_TYPE_INTEGRATION, _('External Integration')),
        (TOKEN_TYPE_WEBHOOK, _('Webhook')),
        (TOKEN_TYPE_CUSTOM, _('Custom')),
        (TOKEN_TYPE_SYNC, _('Instance Sync')),
    ]

    name = models.CharField(
        max_length=200,
        help_text=_("Descriptive name for this token (e.g., 'Help System API', 'Zapier Integration')"),
        verbose_name=_("Name")
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text=_("The actual API token (auto-generated)"),
        verbose_name=_("Token")
    )

    token_type = models.CharField(
        max_length=50,
        choices=TOKEN_TYPE_CHOICES,
        default=TOKEN_TYPE_CUSTOM,
        help_text=_("Type/purpose of this token"),
        verbose_name=_("Token Type")
    )

    description = models.TextField(
        blank=True,
        help_text=_("Optional description of what this token is used for"),
        verbose_name=_("Description")
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this token is currently active and can be used"),
        verbose_name=_("Active")
    )

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_api_tokens',
        help_text=_("User who created this token"),
        verbose_name=_("Created By")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When this token was last used"),
        verbose_name=_("Last Used At")
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When this token expires (leave empty for no expiration)"),
        verbose_name=_("Expires At")
    )

    # Optional IP restrictions
    allowed_ips = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of allowed IP addresses (empty = allow all)"),
        verbose_name=_("Allowed IPs")
    )

    # Usage tracking
    usage_count = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of times this token has been used"),
        verbose_name=_("Usage Count")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("API Token")
        verbose_name_plural = _("API Tokens")
        indexes = [
            models.Index(fields=['token', 'is_active']),
            models.Index(fields=['token_type', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.token_type})"

    @property
    def is_expired(self):
        """Check if token has expired"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        """Check if token is currently valid (active and not expired)"""
        return self.is_active and not self.is_expired

    def record_usage(self, ip_address=None):
        """
        Record token usage and update last_used_at timestamp

        Args:
            ip_address: Optional IP address of the request
        """
        self.usage_count += 1
        self.last_used_at = timezone.now()
        self.save(update_fields=['usage_count', 'last_used_at'])

    def mask_token(self):
        """Return masked version of token for display"""
        if len(self.token) <= 8:
            return '****'
        return f"{self.token[:4]}...{self.token[-4:]}"


# ============================================================================
# Platform Secrets Model
# ============================================================================

class PlatformSecrets(models.Model):
    """
    Stores platform service secrets issued by the Spwig license server.
    This is a singleton model - only one instance should exist.

    Secrets are issued per-installation by the license server and used for:
    - GeoIP service JWT authentication
    - Push notification service JWT authentication
    - SSO/Community service JWT authentication

    These secrets should NEVER be stored in .env or distributed with the package.
    They are fetched from the license server during license activation.
    """

    # Service JWT Secrets (64-char hex strings, issued by license server)
    geoip_jwt_secret = models.CharField(
        max_length=128,
        blank=True,
        help_text=_("JWT secret for GeoIP service authentication")
    )

    push_jwt_secret = models.CharField(
        max_length=128,
        blank=True,
        help_text=_("JWT secret for Push notification service authentication")
    )

    sso_jwt_secret = models.CharField(
        max_length=128,
        blank=True,
        help_text=_("JWT secret for SSO/Community service authentication")
    )

    # License server credentials for refreshing secrets
    installation_uuid = models.UUIDField(
        null=True,
        blank=True,
        help_text=_("Installation UUID assigned by license server")
    )

    license_server_token = models.TextField(
        blank=True,
        help_text=_("Current access token for license server API")
    )

    license_server_refresh_token = models.TextField(
        blank=True,
        help_text=_("Refresh token for license server API")
    )

    token_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the current access token expires")
    )

    # Timestamps
    secrets_fetched_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When secrets were last fetched from license server")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Platform Secrets")
        verbose_name_plural = _("Platform Secrets")

    def __str__(self):
        if self.installation_uuid:
            return f"Platform Secrets (Installation: {self.installation_uuid})"
        return "Platform Secrets (Not initialized)"

    def save(self, *args, **kwargs):
        """
        Ensure only one instance of PlatformSecrets exists (singleton pattern)
        """
        if not self.pk and PlatformSecrets.objects.exists():
            # If trying to create a new instance but one already exists, update the existing one
            existing = PlatformSecrets.objects.first()
            self.pk = existing.pk
        elif not self.pk:
            # If this is the first instance, force ID to 1
            self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_secrets(cls):
        """
        Get the current platform secrets instance, creating one if it doesn't exist.
        Returns None for secrets if not yet initialized.
        """
        secrets, created = cls.objects.get_or_create(pk=1)
        return secrets

    @property
    def is_initialized(self):
        """Check if secrets have been fetched from license server"""
        return bool(self.geoip_jwt_secret and self.push_jwt_secret and self.sso_jwt_secret)

    @property
    def needs_token_refresh(self):
        """Check if the license server token needs refreshing"""
        if not self.token_expires_at:
            return True
        # Refresh if token expires in less than 5 minutes
        from datetime import timedelta
        return timezone.now() >= self.token_expires_at - timedelta(minutes=5)

    def get_geoip_secret(self):
        """Get GeoIP JWT secret, falling back to env if not initialized"""
        if self.geoip_jwt_secret:
            return self.geoip_jwt_secret
        import os
        return os.environ.get('GEOIP_JWT_SECRET_KEY', '')

    def get_push_secret(self):
        """Get Push JWT secret, falling back to env if not initialized"""
        if self.push_jwt_secret:
            return self.push_jwt_secret
        import os
        return os.environ.get('PUSH_JWT_SECRET_KEY', '')

    def get_sso_secret(self):
        """Get SSO JWT secret, falling back to env if not initialized"""
        if self.sso_jwt_secret:
            return self.sso_jwt_secret
        import os
        return os.environ.get('SSO_REGISTRATION_SECRET', '')


class TrustedDevice(models.Model):
    """
    Stores trusted devices for 2FA "Remember this device" functionality.

    When a user authenticates via 2FA and checks "Remember this device",
    a secure token is stored to allow skipping 2FA for future logins
    from the same device until expiration.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='trusted_devices',
        verbose_name=_("User")
    )

    # Token stored as SHA-256 hash only (raw token goes to cookie)
    device_token_hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name=_("Device Token Hash"),
        help_text=_("SHA-256 hash of the secure token stored in cookie")
    )

    device_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Device Name"),
        help_text=_("Human-readable device identifier (derived from user agent)")
    )

    user_agent = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("User Agent"),
        help_text=_("Browser/device user agent string")
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address"),
        help_text=_("IP address when device was trusted (audit only)")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
        help_text=_("When this trusted device designation expires")
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Used At")
    )

    is_revoked = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Revoked")
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Revoked At")
    )

    revoked_reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Revocation Reason")
    )

    class Meta:
        verbose_name = _("Trusted Device")
        verbose_name_plural = _("Trusted Devices")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_revoked']),
            models.Index(fields=['device_token_hash', 'is_revoked']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.device_name or 'Unknown Device'}"

    @property
    def is_valid(self):
        """Check if the trusted device is still valid."""
        if self.is_revoked:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True

    def revoke(self, reason=''):
        """Revoke this trusted device."""
        self.is_revoked = True
        self.revoked_at = timezone.now()
        self.revoked_reason = reason
        self.save(update_fields=['is_revoked', 'revoked_at', 'revoked_reason'])

    def record_usage(self, ip_address=None):
        """Record that this trusted device was used."""
        self.last_used_at = timezone.now()
        update_fields = ['last_used_at']
        if ip_address:
            self.ip_address = ip_address
            update_fields.append('ip_address')
        self.save(update_fields=update_fields)

    # Alias for compatibility with mobile API
    update_last_used = record_usage

    @classmethod
    def generate_token(cls):
        """Generate a cryptographically secure device token."""
        import secrets
        return secrets.token_urlsafe(48)

    @classmethod
    def hash_token(cls, token):
        """Hash a token using SHA-256."""
        import hashlib
        return hashlib.sha256(token.encode()).hexdigest()

    @classmethod
    def create_trusted_device(cls, user, request, duration_days=30):
        """
        Create a new trusted device entry.

        Returns:
            tuple: (TrustedDevice instance, raw_token for cookie)
        """
        raw_token = cls.generate_token()
        token_hash = cls.hash_token(raw_token)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        ip_address = cls._get_client_ip(request)
        device_name = cls._parse_device_name(user_agent)

        device = cls.objects.create(
            user=user,
            device_token_hash=token_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            device_name=device_name,
            expires_at=timezone.now() + timezone.timedelta(days=duration_days)
        )

        return device, raw_token

    @classmethod
    def validate_token(cls, user, raw_token):
        """
        Validate a raw token and return the trusted device if valid.

        Returns:
            TrustedDevice or None
        """
        token_hash = cls.hash_token(raw_token)

        try:
            device = cls.objects.get(
                user=user,
                device_token_hash=token_hash,
                is_revoked=False
            )
            if device.is_valid:
                device.record_usage()
                return device
        except cls.DoesNotExist:
            pass

        return None

    @classmethod
    def _get_client_ip(cls, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    @classmethod
    def _parse_device_name(cls, user_agent):
        """Parse a human-readable device name from user agent."""
        if not user_agent:
            return 'Unknown Device'

        # Detect browser
        browser = 'Unknown Browser'
        if 'Firefox' in user_agent:
            browser = 'Firefox'
        elif 'Edg/' in user_agent:
            browser = 'Edge'
        elif 'Chrome' in user_agent:
            browser = 'Chrome'
        elif 'Safari' in user_agent:
            browser = 'Safari'
        elif 'Opera' in user_agent or 'OPR/' in user_agent:
            browser = 'Opera'

        # Detect OS
        os_name = 'Unknown OS'
        if 'iPhone' in user_agent:
            os_name = 'iPhone'
        elif 'iPad' in user_agent:
            os_name = 'iPad'
        elif 'Android' in user_agent:
            os_name = 'Android'
        elif 'Windows' in user_agent:
            os_name = 'Windows'
        elif 'Mac OS' in user_agent or 'Macintosh' in user_agent:
            os_name = 'macOS'
        elif 'Linux' in user_agent:
            os_name = 'Linux'

        return f"{browser} on {os_name}"

    @classmethod
    def revoke_all_for_user(cls, user, reason='User requested'):
        """Revoke all trusted devices for a user."""
        return cls.objects.filter(user=user, is_revoked=False).update(
            is_revoked=True,
            revoked_at=timezone.now(),
            revoked_reason=reason
        )

    @classmethod
    def cleanup_expired(cls):
        """Delete expired trusted devices older than 30 days past expiration."""
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=30)
        return cls.objects.filter(expires_at__lt=cutoff).delete()

    @classmethod
    def is_device_trusted(cls, user, device_id):
        """
        Check if a device is trusted for a user (mobile API compatibility).

        Uses the same hashing mechanism as web tokens - the device_id is hashed
        and looked up in device_token_hash.

        Args:
            user: The user to check
            device_id: The device identifier from mobile app

        Returns:
            TrustedDevice or None if not trusted
        """
        return cls.validate_token(user, device_id)

    @classmethod
    def trust_device(cls, user, device_id, device_name='', ip_address=None, trust_days=None):
        """
        Trust a device for a user (mobile API).

        Args:
            user: The user to trust the device for
            device_id: The device identifier from mobile app
            device_name: Human-readable device name (e.g., "iPhone 15 Pro")
            ip_address: IP address when trusting
            trust_days: Number of days to trust (defaults to 30)

        Returns:
            TrustedDevice instance
        """
        from django.conf import settings

        if trust_days is None:
            mobile_settings = getattr(settings, 'MOBILE_API_SETTINGS', {})
            trust_days = mobile_settings.get('DEVICE_TRUST_DAYS', 30)

        token_hash = cls.hash_token(device_id)
        now = timezone.now()
        expires_at = now + timezone.timedelta(days=trust_days)

        # Update or create trusted device
        device, created = cls.objects.update_or_create(
            user=user,
            device_token_hash=token_hash,
            defaults={
                'device_name': device_name,
                'ip_address': ip_address,
                'expires_at': expires_at,
                'is_revoked': False,
                'revoked_at': None,
                'revoked_reason': '',
                'last_used_at': now,
            }
        )

        return device


class ErrorReport(models.Model):
    """
    Local buffer for error reports before batch transmission to Spwig.
    Records are deleted after successful transmission or aged out.
    """

    ERROR_TYPES = [
        ('python', 'Python Exception'),
        ('javascript', 'JavaScript Error'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('held', 'Held for Review'),
    ]

    error_type = models.CharField(max_length=20, choices=ERROR_TYPES, db_index=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True
    )
    fingerprint = models.CharField(
        max_length=64,
        db_index=True,
        help_text="SHA-256 hash of exception_type + location for dedup",
    )
    occurrence_count = models.PositiveIntegerField(default=1)
    error_data = models.JSONField(help_text="Sanitized error details")
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    merchant_notes = models.TextField(blank=True)
    submitted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='submitted_error_reports',
    )

    class Meta:
        verbose_name = _("Error Report")
        verbose_name_plural = _("Error Reports")
        ordering = ['-last_seen']
        indexes = [
            models.Index(fields=['status', '-last_seen']),
            models.Index(fields=['fingerprint', 'status']),
        ]

    def __str__(self):
        exc_type = self.error_data.get('exception_type', 'Unknown') if self.error_data else 'Unknown'
        return f"{self.get_error_type_display()}: {exc_type} ({self.occurrence_count}x)"

    @staticmethod
    def compute_fingerprint(exception_type, traceback_or_stack=''):
        """Generate a dedup fingerprint from the exception type and last frame."""
        last_frame = ''
        if traceback_or_stack:
            lines = traceback_or_stack.strip().splitlines()
            for line in reversed(lines):
                stripped = line.strip()
                if stripped.startswith('File ') or stripped.startswith('at '):
                    last_frame = stripped
                    break
        raw = f"{exception_type}:{last_frame}"
        return hashlib.sha256(raw.encode()).hexdigest()


class BugReport(models.Model):
    """
    User-submitted bug report, stored locally before transmission to Spwig.
    """

    CATEGORY_CHOICES = [
        ('ui_visual', _('UI/Visual Issue')),
        ('functionality', _('Functionality Broken')),
        ('performance', _('Performance')),
        ('data', _('Data Issue')),
        ('other', _('Other')),
    ]
    SEVERITY_CHOICES = [
        ('minor', _('Minor Annoyance')),
        ('significant', _('Significant Issue')),
        ('blocking', _('Blocking Issue')),
    ]
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('failed', _('Failed')),
    ]

    # Step 1 data
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(
        help_text=_("What were you doing when you noticed the bug?"),
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)

    # Step 2 data (consent-based browser data)
    browser_data = models.JSONField(
        default=dict, blank=True,
        help_text=_("Consented browser data: console logs, URL, user agent, breadcrumbs"),
    )
    consent_flags = models.JSONField(
        default=dict, blank=True,
        help_text=_("Which data collection toggles were enabled"),
    )

    # Step 3 data (optional contact)
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_consent = models.BooleanField(
        default=False,
        help_text=_("Is it okay to contact you?"),
    )

    # Metadata
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending',
    )
    submitted_by = models.ForeignKey(
        get_user_model(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name='bug_reports',
    )
    page_url = models.URLField(blank=True, max_length=500)
    admin_section = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Bug Report")
        verbose_name_plural = _("Bug Reports")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_category_display()}: {self.description[:60]}"


User = get_user_model()


class CookieConsentLog(models.Model):
    """
    Server-side audit trail for cookie consent decisions.

    Required for GDPR Article 7(1) compliance — controllers must be able to
    demonstrate that consent was given. Each record captures what the visitor
    consented to, when, and from which IP/browser.
    """

    ACTION_CHOICES = [
        ('accept_all', _('Accept All')),
        ('reject_all', _('Reject All')),
        ('save_preferences', _('Save Preferences')),
    ]

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Timestamp'),
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        db_index=True,
        verbose_name=_('Action'),
    )

    consent_data = models.JSONField(
        verbose_name=_('Consent Data'),
        help_text=_('Full consent payload: necessary, analytics, marketing, functional'),
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP Address'),
    )

    user_agent = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name=_('User Agent'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cookie_consent_logs',
        verbose_name=_('User'),
    )

    session_key = models.CharField(
        max_length=40,
        blank=True,
        default='',
        verbose_name=_('Session Key'),
        help_text=_('Session key for anonymous visitors'),
    )

    class Meta:
        verbose_name = _('Cookie Consent Log')
        verbose_name_plural = _('Cookie Consent Logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'], name='consent_log_time'),
            models.Index(fields=['user', '-timestamp'], name='consent_log_user_time'),
            models.Index(fields=['session_key', '-timestamp'], name='consent_log_sess_time'),
        ]

    def __str__(self):
        who = self.user.email if self.user_id else self.ip_address or 'anonymous'
        return f"{self.get_action_display()} — {who} @ {self.timestamp:%Y-%m-%d %H:%M}"


class SeedVersion(models.Model):
    """
    Tracks which seed data versions have been applied.
    Used by the seed orchestrator to skip seeds that are already current.
    """
    seed_name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text=_('Unique identifier for this seed'),
    )
    version = models.PositiveIntegerField(
        default=1,
        help_text=_('Integer version. Increment when seed data changes.'),
    )
    applied_at = models.DateTimeField(
        auto_now=True,
    )
    record_count = models.PositiveIntegerField(
        default=0,
        help_text=_('Number of records created/updated by last run'),
    )

    class Meta:
        verbose_name = _('Seed Version')
        verbose_name_plural = _('Seed Versions')

    def __str__(self):
        return f"{self.seed_name} v{self.version}"


class SalesBellEvent(models.Model):
    """
    Append-only event log for the Spwig Sales Bell (Pi dashboard).
    Only used on spwig.com (SPWIG_IS_HQ=True).
    """
    EVENT_TYPES = [
        ('sale', 'Sale'),
        ('refund', 'Refund'),
        ('developer_signup', 'Developer Signup'),
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, db_index=True)
    subtype = models.CharField(max_length=30, blank=True)  # license, marketplace, dev_license
    name = models.CharField(max_length=100, blank=True)
    product = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='EUR')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type}: {self.product or self.name} ({self.amount})"

    @classmethod
    def log_sale(cls, order, subtype='license'):
        """Log a sale event from an Order."""
        # Extract raw Decimal from Money objects (MoneyField returns Money, not Decimal)
        raw_amount = order.amount_paid or order.total
        if hasattr(raw_amount, 'amount'):
            raw_amount = raw_amount.amount
        return cls.objects.create(
            event_type='sale',
            subtype=subtype,
            name=getattr(order, 'customer_name', '') or order.billing_name or '',
            product=cls._get_product_name(order, subtype),
            amount=raw_amount,
            currency=getattr(order, 'currency_code', 'EUR') or 'EUR',
        )

    @classmethod
    def log_refund(cls, refund_transaction):
        """Log a refund event from a PaymentTransaction."""
        raw_amount = refund_transaction.amount
        if hasattr(raw_amount, 'amount'):
            raw_amount = raw_amount.amount
        return cls.objects.create(
            event_type='refund',
            name=refund_transaction.customer_name or '',
            product=str(refund_transaction.order) if refund_transaction.order else '',
            amount=raw_amount,
            currency=str(refund_transaction.amount_currency) if refund_transaction.amount_currency else 'EUR',
        )

    @classmethod
    def log_developer_signup(cls, profile):
        """Log a developer signup event."""
        return cls.objects.create(
            event_type='developer_signup',
            name=profile.display_name or profile.developer_slug,
        )

    @classmethod
    def _get_product_name(cls, order, subtype):
        """Extract a readable product name from an order."""
        try:
            first_item = order.items.first()
            if first_item:
                return first_item.product_name or str(first_item)
        except Exception:
            pass
        return f"{'License' if subtype == 'license' else 'Marketplace'} Purchase"