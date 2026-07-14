import logging
import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries import countries
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

logger = logging.getLogger(__name__)

User = get_user_model()


class ShippingCountry(models.Model):
    """
    Countries the merchant ships to.

    This model defines which countries the merchant accepts orders from and ships to.
    It's used to filter available payment methods and shipping options at checkout.

    Future: Can be associated with specific warehouses to define source-destination mapping.
    """

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="shipping_countries", verbose_name=_("site")
    )

    country_code = models.CharField(
        max_length=2,
        verbose_name=_("country code"),
        help_text=_("ISO 3166-1 alpha-2 country code (e.g., US, GB, SG)"),
    )

    # Future Phase 2: warehouse-to-destination mapping
    source_warehouse = models.ForeignKey(
        "catalog.Warehouse",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="destination_countries",
        verbose_name=_("source warehouse"),
        help_text=_("Warehouse that services this destination country (optional)"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text=_("Whether shipping to this country is currently enabled"),
    )

    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_("priority"),
        help_text=_(
            "Routing priority when multiple warehouses can service this country (lower = higher priority)"
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        unique_together = [["site", "country_code"]]
        ordering = ["priority", "country_code"]
        verbose_name = _("shipping country")
        verbose_name_plural = _("shipping countries")
        indexes = [
            models.Index(fields=["site", "is_active"]),
            models.Index(fields=["country_code", "is_active"]),
        ]

    def __str__(self):
        country_name = countries.name(self.country_code)
        return f"{country_name} ({self.country_code})"

    def save(self, *args, **kwargs):
        # Ensure country_code is uppercase
        if self.country_code:
            self.country_code = self.country_code.upper()
        super().save(*args, **kwargs)


class CountryWarehouseFallback(models.Model):
    """
    Ordered fallback warehouse chain for countries.

    When the primary warehouse (source_warehouse) is out of stock,
    the system checks fallback warehouses in priority order.

    Example:
    - Australia primary: Sydney Warehouse
    - Fallback 1: Singapore Warehouse (priority 0)
    - Fallback 2: China Warehouse (priority 1)
    """

    country = models.ForeignKey(
        ShippingCountry,
        on_delete=models.CASCADE,
        related_name="warehouse_fallbacks",
        verbose_name=_("shipping country"),
    )
    warehouse = models.ForeignKey(
        "catalog.Warehouse",
        on_delete=models.CASCADE,
        related_name="fallback_for_countries",
        verbose_name=_("warehouse"),
    )
    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_("priority"),
        help_text=_("Lower number = higher priority (0 = first fallback)"),
    )

    # Optional: Extended delivery message when using this fallback
    extended_delivery_message = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("extended delivery message"),
        help_text=_(
            'Message shown when fulfilled from fallback (e.g., "Ships from Singapore - extended delivery")'
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("country warehouse fallback")
        verbose_name_plural = _("country warehouse fallbacks")
        ordering = ["country", "priority"]
        unique_together = ["country", "warehouse"]
        indexes = [
            models.Index(fields=["country", "priority"]),
        ]

    def __str__(self):
        return f"{self.country.country_code} → {self.warehouse.name} (priority {self.priority})"


class CarrierPreset(models.Model):
    """
    Manual shipping carriers (DHL, FedEx, UPS, etc.)
    Admins can create custom carriers or use pre-shipped ones
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=128, verbose_name=_("carrier name"), help_text=_("Display name for this carrier")
    )

    slug = models.SlugField(
        max_length=128, unique=True, verbose_name=_("slug"), help_text=_("URL-safe identifier")
    )

    tracking_url_template = models.URLField(
        blank=True,
        verbose_name=_("tracking URL template"),
        help_text=_(
            "URL template with {tracking_number} placeholder. Example: https://dhl.com/track/{tracking_number}"
        ),
    )

    country_of_operation = CountryField(
        blank=True,
        null=True,
        verbose_name=_("country of operation"),
        help_text=_("Primary country where this carrier operates"),
    )

    logo = models.FileField(
        upload_to="shipping/carrier_logos/",
        blank=True,
        null=True,
        verbose_name=_("logo"),
        help_text=_("Carrier logo (SVG or WebP, 200x200px, transparent background)"),
    )

    description = models.TextField(
        blank=True, verbose_name=_("description"), help_text=_("Optional carrier description")
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("is default carrier"),
        help_text=_("Use this carrier as default for manual shipments"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text=_("Whether this carrier is available for selection"),
    )

    is_system = models.BooleanField(
        default=False,
        verbose_name=_("is system preset"),
        help_text=_("Pre-shipped carrier (cannot be deleted)"),
    )

    tracking_url_template_override = models.URLField(
        blank=True,
        max_length=500,
        verbose_name=_("tracking URL override"),
        help_text=_(
            "Override the system tracking URL template. Use {tracking_number} as placeholder. Leave empty to use system default."
        ),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_carriers",
        verbose_name=_("created by"),
    )

    class Meta:
        ordering = ["country_of_operation", "name"]
        verbose_name = _("carrier preset")
        verbose_name_plural = _("carrier presets")
        indexes = [
            models.Index(fields=["is_active", "name"]),
            models.Index(fields=["is_default"]),
            models.Index(fields=["country_of_operation", "is_active"]),
        ]

    def __str__(self):
        return self.name

    def logo_with_fallback(self):
        """Get logo URL or Font Awesome fallback icon"""
        if self.logo:
            return {"type": "image", "url": self.logo.url}
        return {"type": "icon", "class": "fas fa-shipping-fast"}

    def get_tracking_url_template(self):
        """Get effective tracking URL template (override or system default)"""
        if self.tracking_url_template_override:
            return self.tracking_url_template_override
        return self.tracking_url_template

    def has_url_override(self):
        """Check if carrier has custom URL override"""
        return bool(self.tracking_url_template_override)

    def get_url_status(self):
        """Get URL status for display"""
        if self.has_url_override():
            return {"type": "override", "display": _("Custom URL"), "badge_class": "badge-info"}
        return {"type": "system", "display": _("System URL"), "badge_class": "badge-secondary"}

    def save(self, *args, **kwargs):
        # Ensure only one default carrier
        if self.is_default:
            CarrierPreset.objects.filter(is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )
        super().save(*args, **kwargs)


class ShippingPackage(models.Model):
    """
    Predefined packaging sizes for shipping calculations.
    Merchants define standard boxes/envelopes they use for shipping.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=100,
        verbose_name=_("package name"),
        help_text=_('Package identifier (e.g., "Small Box", "Padded Envelope")'),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
        help_text=_("Optional package description or usage notes"),
    )

    # Internal dimensions (stored in cm)
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("length (cm)"),
        help_text=_("Internal length in centimeters"),
    )

    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("width (cm)"),
        help_text=_("Internal width in centimeters"),
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("height (cm)"),
        help_text=_("Internal height in centimeters"),
    )

    # Material thickness
    wall_thickness = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.5"),
        verbose_name=_("wall thickness (cm)"),
        help_text=_(
            "Package material thickness in centimeters (default 0.5cm for standard cardboard). Used to calculate external dimensions for shipping carriers."
        ),
    )

    # Weight constraints (stored in kg)
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_("maximum weight (kg)"),
        help_text=_("Maximum capacity in kilograms"),
    )

    tare_weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=Decimal("0.000"),
        verbose_name=_("package weight (kg)"),
        help_text=_("Empty package weight (tare) in kilograms - added to shipment weight"),
    )

    # Costing
    cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("package cost"),
        help_text=_("Cost per package if applicable"),
    )

    # Selection preference
    priority = models.IntegerField(
        default=0,
        verbose_name=_("priority"),
        help_text=_("Selection preference for auto-packing (higher = preferred)"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text=_("Whether this package is available for use"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        ordering = ["-priority", "name"]
        verbose_name = _("shipping package")
        verbose_name_plural = _("shipping packages")
        indexes = [
            models.Index(fields=["is_active", "-priority"]),
            models.Index(fields=["max_weight"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.length}×{self.width}×{self.height}cm)"

    def get_volume(self):
        """Calculate internal volume in cubic centimeters"""
        if not all([self.length, self.width, self.height]):
            return None
        return self.length * self.width * self.height

    def get_volume_liters(self):
        """Calculate internal volume in liters"""
        volume = self.get_volume()
        if volume is None:
            return None
        return volume / 1000

    def get_external_dimensions(self):
        """
        Calculate external dimensions from internal dimensions + wall thickness.

        Shipping carriers typically use external dimensions for:
        - Dimensional weight calculations
        - Shipping cost determination
        - Size-based surcharges

        Returns:
            dict: External dimensions with keys 'length', 'width', 'height' in cm,
                  or None if dimensions are not yet set
        """
        if not all([self.length, self.width, self.height, self.wall_thickness]):
            return None

        thickness_adjustment = self.wall_thickness * 2  # Both sides
        return {
            "length": self.length + thickness_adjustment,
            "width": self.width + thickness_adjustment,
            "height": self.height + thickness_adjustment,
        }

    def get_external_volume(self):
        """Calculate external volume in cubic centimeters"""
        dims = self.get_external_dimensions()
        if dims is None:
            return None
        return dims["length"] * dims["width"] * dims["height"]

    def fits_item(self, length, width, height):
        """
        Check if an item with given dimensions fits in this package.
        Tries all possible orientations.

        Args:
            length, width, height: Item dimensions in cm

        Returns:
            bool: True if item fits, False otherwise
        """
        # Check if package dimensions are set
        if not all([self.length, self.width, self.height]):
            return False

        # Get all permutations of item dimensions
        item_dims = sorted([length, width, height])
        package_dims = sorted([self.length, self.width, self.height])

        # Check if item fits in any orientation
        return all(item <= pkg for item, pkg in zip(item_dims, package_dims, strict=True))

    def can_hold_weight(self, weight):
        """
        Check if package can hold the specified weight.

        Args:
            weight: Weight in kg

        Returns:
            bool: True if package can hold the weight
        """
        return weight <= self.max_weight


class ProviderAccount(models.Model):
    """
    API provider connections (Easyship, ShipEngine, NinjaVan, etc.)
    Stores encrypted credentials and configuration
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to ComponentRegistry (shipping_provider type)
    component = models.ForeignKey(
        "component_updates.ComponentRegistry",
        on_delete=models.CASCADE,
        limit_choices_to={"component_type": "shipping_provider"},
        related_name="provider_accounts",
        verbose_name=_("component"),
        help_text=_("Installed shipping provider component"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipping_providers",
        verbose_name=_("user"),
        help_text=_("User who owns this provider account"),
    )

    display_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("display name"),
        help_text=_('Friendly name for this connection (e.g., "My Easyship Account")'),
    )

    # Encrypted credentials (API keys, secrets, tokens)
    credentials_encrypted = models.JSONField(
        default=dict,
        verbose_name=_("credentials"),
        help_text=_("Encrypted API credentials (never stored in plain text)"),
    )

    # Provider-specific settings and capabilities
    settings = models.JSONField(
        default=dict, verbose_name=_("settings"), help_text=_("Provider-specific configuration")
    )

    # Signup affiliate link (optional)
    signup_url = models.URLField(
        blank=True,
        verbose_name=_("signup URL"),
        help_text=_("Link for merchants to create provider account (may be affiliate link)"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text=_("Whether this provider connection is active"),
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("is default"),
        help_text=_("Use this provider as default for API shipments"),
    )

    # Connection health
    last_tested_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("last tested at"),
        help_text=_("Last successful connection test"),
    )

    connection_status = models.CharField(
        max_length=20,
        choices=[
            ("unknown", _("Unknown")),
            ("connected", _("Connected")),
            ("error", _("Connection Error")),
        ],
        default="unknown",
        verbose_name=_("connection status"),
    )

    connection_error = models.TextField(
        blank=True, verbose_name=_("connection error"), help_text=_("Last connection error message")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("provider account")
        verbose_name_plural = _("provider accounts")
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["is_default"]),
        ]

    def __str__(self):
        name = self.display_name or self.component.name
        return f"{name} ({self.user.username})"

    def save(self, *args, **kwargs):
        # Ensure only one default provider per user
        if self.is_default:
            ProviderAccount.objects.filter(user=self.user, is_default=True).exclude(
                pk=self.pk
            ).update(is_default=False)
        super().save(*args, **kwargs)


class Shipment(models.Model):
    """
    Individual shipment associated with an order
    Can be manual (CarrierPreset) or API (ProviderAccount)
    """

    STATUS_CHOICES = [
        ("created", _("Created - Shipment record created")),
        ("labeled", _("Labeled - Label purchased")),
        ("in_transit", _("In Transit - Package is moving")),
        ("out_for_delivery", _("Out for Delivery")),
        ("delivered", _("Delivered - Successfully delivered")),
        ("exception", _("Exception - Delivery issue")),
        ("returned", _("Returned - Returned to sender")),
        ("canceled", _("Canceled - Shipment canceled")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Order relationship
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="shipments",
        verbose_name=_("order"),
        help_text=_("Order associated with this shipment"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipments",
        verbose_name=_("user"),
        help_text=_("User who created this shipment"),
    )

    # Provider (manual OR API, not both)
    carrier_preset = models.ForeignKey(
        CarrierPreset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipments",
        verbose_name=_("manual carrier"),
        help_text=_("Manual carrier preset (for manual tracking)"),
    )

    provider_account = models.ForeignKey(
        ProviderAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipments",
        verbose_name=_("API provider"),
        help_text=_("API provider account (for automated labels)"),
    )

    # Shipping details
    origin_country = models.CharField(
        max_length=2,
        verbose_name=_("origin country"),
        help_text=_("ISO 3166-1 alpha-2 country code"),
    )

    dest_country = models.CharField(
        max_length=2,
        verbose_name=_("destination country"),
        help_text=_("ISO 3166-1 alpha-2 country code"),
    )

    # Package dimensions
    packages = models.JSONField(
        default=list,
        verbose_name=_("packages"),
        help_text=_("Array of {weight_g, length_cm, width_cm, height_cm}"),
    )

    # Service level (e.g., 'express', 'standard', 'economy')
    service_level = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("service level"),
        help_text=_("Shipping service type"),
    )

    # Pricing mode used
    pricing_mode_used = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_("pricing mode"),
        help_text=_("flat|free_over_x|free_domestic|carrier_quote"),
    )

    # Costs (using MoneyField)
    shipping_cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("shipping cost"),
        help_text=_("Cost charged to customer"),
    )

    carrier_cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("carrier cost"),
        help_text=_("Cost from carrier/provider"),
    )

    # Tracking
    tracking_id = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
        verbose_name=_("tracking number"),
        help_text=_("Carrier tracking number"),
    )

    label_url = models.URLField(
        blank=True, verbose_name=_("label URL"), help_text=_("Download URL for shipping label")
    )

    # Document URLs (Phase 6: Document Generation)
    # Using TextField to support large data URIs (base64-encoded PDFs)
    packing_slip_url = models.TextField(
        blank=True,
        verbose_name=_("packing slip URL"),
        help_text=_("Download URL or data URI for packing slip document"),
    )

    commercial_invoice_url = models.TextField(
        blank=True,
        verbose_name=_("commercial invoice URL"),
        help_text=_("Download URL or data URI for commercial invoice document"),
    )

    customs_form_url = models.TextField(
        blank=True,
        verbose_name=_("customs form URL"),
        help_text=_("Download URL or data URI for customs declaration form (CN22/CN23)"),
    )

    # Status
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default="created",
        db_index=True,
        verbose_name=_("status"),
    )

    # Provider-specific metadata
    provider_reference = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("provider reference"),
        help_text=_("Provider's internal shipment ID"),
    )

    provider_meta = models.JSONField(
        default=dict,
        verbose_name=_("provider metadata"),
        help_text=_("Additional provider-specific data"),
    )

    # Audit trail
    audit_log = models.JSONField(
        default=list,
        verbose_name=_("audit log"),
        help_text=_("Compact event trail for BI and support"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("shipment")
        verbose_name_plural = _("shipments")
        indexes = [
            models.Index(fields=["order", "-created_at"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["tracking_id"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        provider = self.carrier_preset or (
            self.provider_account.display_name if self.provider_account else "Unknown"
        )
        return f"Shipment for Order {self.order.order_number} via {provider}"

    @property
    def is_manual(self):
        """Check if this is a manual shipment"""
        return self.carrier_preset is not None

    @property
    def is_api(self):
        """Check if this is an API shipment"""
        return self.provider_account is not None

    def get_tracking_url(self):
        """Generate tracking URL based on provider"""
        if not self.tracking_id:
            return None

        # Use effective URL (override or system default)
        if self.carrier_preset:
            url_template = self.carrier_preset.get_tracking_url_template()
            if url_template:
                return url_template.format(tracking_number=self.tracking_id)

        # API providers handle tracking URLs via their SDK
        return None


class TrackingEvent(models.Model):
    """
    Tracking events/checkpoints for a shipment
    """

    STATUS_CHOICES = [
        ("info_received", _("Info Received")),
        ("in_transit", _("In Transit")),
        ("out_for_delivery", _("Out for Delivery")),
        ("delivered", _("Delivered")),
        ("exception", _("Exception")),
        ("returned", _("Returned")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="tracking_events",
        verbose_name=_("shipment"),
    )

    status = models.CharField(max_length=64, choices=STATUS_CHOICES, verbose_name=_("status"))

    description = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_("description"),
        help_text=_("Human-readable event description"),
    )

    location = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("location"),
        help_text=_("Event location (city, state, country)"),
    )

    occurred_at = models.DateTimeField(
        verbose_name=_("occurred at"), help_text=_("When this event occurred")
    )

    raw = models.JSONField(
        default=dict, verbose_name=_("raw data"), help_text=_("Raw event data from provider")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        ordering = ["-occurred_at"]
        verbose_name = _("tracking event")
        verbose_name_plural = _("tracking events")
        indexes = [
            models.Index(fields=["shipment", "-occurred_at"]),
        ]

    def __str__(self):
        return f"{self.get_status_display()} - {self.occurred_at.strftime('%Y-%m-%d %H:%M')}"


class WebhookLog(models.Model):
    """
    Log of inbound webhooks from shipping providers
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    provider_key = models.CharField(
        max_length=64,
        verbose_name=_("provider key"),
        help_text=_("Provider slug that sent the webhook"),
    )

    endpoint = models.CharField(
        max_length=128, verbose_name=_("endpoint"), help_text=_("Webhook endpoint path")
    )

    payload = models.JSONField(verbose_name=_("payload"), help_text=_("Webhook payload data"))

    headers = models.JSONField(verbose_name=_("headers"), help_text=_("HTTP headers"))

    status_code = models.IntegerField(
        null=True, verbose_name=_("status code"), help_text=_("HTTP response status code")
    )

    processing_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", _("Pending")),
            ("processed", _("Processed")),
            ("failed", _("Failed")),
        ],
        default="pending",
        verbose_name=_("processing status"),
    )

    error_message = models.TextField(blank=True, verbose_name=_("error message"))

    received_at = models.DateTimeField(auto_now_add=True, verbose_name=_("received at"))
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("processed at"))

    class Meta:
        ordering = ["-received_at"]
        verbose_name = _("webhook log")
        verbose_name_plural = _("webhook logs")
        indexes = [
            models.Index(fields=["provider_key", "-received_at"]),
            models.Index(fields=["processing_status"]),
        ]

    def __str__(self):
        return f"{self.provider_key} webhook at {self.received_at.strftime('%Y-%m-%d %H:%M')}"


class ShippingZone(models.Model):
    """
    Geographic shipping zones for rate calculation and rule assignment.

    Zones define geographic areas (countries, states, postal codes) where
    specific shipping methods and rates apply. Multiple shipping methods
    can be assigned to a zone.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200,
        verbose_name=_("zone name"),
        help_text=_(
            'Display name for this shipping zone (e.g., "North America", "EU Member States")'
        ),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
        help_text=_("Optional description of what this zone covers"),
    )

    # Geographic coverage
    countries = models.JSONField(
        default=list,
        verbose_name=_("countries"),
        help_text=_(
            'List of ISO 3166-1 alpha-2 country codes (e.g., ["US", "CA", "MX"]). Empty list = all countries.'
        ),
    )

    states = models.JSONField(
        default=dict,
        verbose_name=_("states"),
        help_text=_(
            'Dict mapping country codes to state/province codes. Example: {"US": ["CA", "NY", "TX"], "CA": ["ON", "BC"]}'
        ),
    )

    postal_code_patterns = models.JSONField(
        default=list,
        verbose_name=_("postal code patterns"),
        help_text=_(
            'List of regex patterns for postal/zip codes. Example: ["^90[0-9]{3}$", "^91[0-9]{3}$"] for LA area codes'
        ),
    )

    # Priority and status
    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_("priority"),
        help_text=_(
            "Zone priority (0 = highest). When an address matches multiple zones, the highest priority zone is used."
        ),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text=_("Whether this zone is currently active"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_shipping_zones",
        verbose_name=_("created by"),
    )

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = _("shipping zone")
        verbose_name_plural = _("shipping zones")
        indexes = [
            models.Index(fields=["is_active", "priority"]),
            models.Index(fields=["priority"]),
        ]

    def __str__(self):
        return self.name

    def _normalize_country_code(self, country):
        """
        Normalize country to ISO 3166-1 alpha-2 code.
        Handles both full country names and ISO codes.

        Args:
            country: Country name (e.g., "Singapore") or ISO code (e.g., "SG")

        Returns:
            str: ISO 3166-1 alpha-2 country code (e.g., "SG"), or empty string if not found
        """
        from django_countries import countries

        if not country:
            return ""

        # If already an ISO code (2 chars), return uppercase
        if len(country) == 2:
            return country.upper()

        # Try to find the code by country name
        # django-countries provides countries.by_name()
        for code, name in countries:
            if name.lower() == country.lower():
                return code

        # If not found, return the original (might be a valid code we missed)
        return country.upper()

    def matches_address(self, address):
        """
        Check if the given address falls within this zone.

        Args:
            address: Address object or dict with keys: country, state, postal_code

        Returns:
            bool: True if address matches this zone
        """
        import re

        # Get address components
        if hasattr(address, "country"):
            country = address.country
            state = getattr(address, "state", "")
            postal_code = getattr(address, "postal_code", "")
        else:
            country = address.get("country", "")
            state = address.get("state", "")
            postal_code = address.get("postal_code", "")

        # Normalize country to ISO code for all comparisons
        # Handles both "Singapore" and "SG" formats
        country_code = self._normalize_country_code(country)

        logger.debug(
            "Zone '%s' matching: address_country='%s' → normalized='%s', zone_countries=%s",
            self.name,
            country,
            country_code,
            self.countries,
        )

        # If zone has no country restrictions, skip country check
        # Otherwise, country must be in the list
        if self.countries:
            if country_code not in self.countries:
                logger.debug(
                    "Zone '%s' rejected: '%s' not in %s", self.name, country_code, self.countries
                )
                return False
            else:
                logger.debug(
                    "Zone '%s' matched: '%s' found in %s", self.name, country_code, self.countries
                )

        # Check state restrictions for this country (using normalized code)
        if self.states and country_code in self.states:
            state_list = self.states[country_code]
            if state_list and state not in state_list:
                return False

        # Check postal code patterns
        if self.postal_code_patterns and postal_code:
            pattern_matched = False
            for pattern in self.postal_code_patterns:
                try:
                    if re.match(pattern, postal_code):
                        pattern_matched = True
                        break
                except re.error:
                    # Invalid regex pattern, skip it
                    continue

            # If patterns are defined but none matched, address doesn't match zone
            if not pattern_matched:
                return False

        return True

    def get_country_count(self):
        """Get number of countries in this zone"""
        return len(self.countries) if self.countries else 0

    def get_state_count(self):
        """Get total number of states/provinces across all countries"""
        if not self.states:
            return 0
        return sum(len(states) for states in self.states.values())

    def get_coverage_summary(self):
        """Get human-readable summary of zone coverage"""
        parts = []

        country_count = self.get_country_count()
        if country_count > 0:
            # Use f-string to properly coerce lazy translation to string
            country_word = _("country") if country_count == 1 else _("countries")
            parts.append(f"{country_count} {country_word}")
        else:
            parts.append(f"{_('All countries')}")

        state_count = self.get_state_count()
        if state_count > 0:
            state_word = _("state") if state_count == 1 else _("states")
            parts.append(f"{state_count} {state_word}")

        pattern_count = len(self.postal_code_patterns) if self.postal_code_patterns else 0
        if pattern_count > 0:
            pattern_word = _("postal pattern") if pattern_count == 1 else _("postal patterns")
            parts.append(f"{pattern_count} {pattern_word}")

        return ", ".join(parts) if parts else f"{_('No restrictions')}"


class ShippingPromotion(models.Model):
    """
    Conditional shipping promotions (e.g., "Free shipping over $50", "Flat $10 if weight < 5kg")
    Promotions are evaluated in priority order to calculate final shipping costs
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200,
        verbose_name=_("promotion name"),
        help_text=_("Internal name for this promotion"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
        help_text=_("Optional description of what this promotion does"),
    )

    # Promotion type determines how the promotion modifies shipping costs
    PROMOTION_TYPES = [
        ("discount_percentage", _("Percentage Discount")),
        ("discount_fixed", _("Fixed Amount Discount")),
        ("override_cost", _("Override Cost")),
        ("free_shipping", _("Free Shipping")),
        ("surcharge_fixed", _("Fixed Surcharge")),
        ("surcharge_percentage", _("Percentage Surcharge")),
    ]
    promotion_type = models.CharField(
        max_length=30, choices=PROMOTION_TYPES, verbose_name=_("promotion type")
    )

    # Promotion value (depends on promotion_type)
    # For percentage: 0-100 (e.g., 50 = 50% off)
    # For fixed amount: dollar amount (e.g., 10.00)
    # For override_cost: specific cost to set (e.g., 5.00)
    promotion_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("promotion value"),
        help_text=_("Amount or percentage value for this promotion"),
    )

    # Conditions - Cart Value
    min_cart_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("minimum cart value"),
        help_text=_("Promotion applies if cart subtotal is at least this amount"),
    )

    max_cart_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("maximum cart value"),
        help_text=_("Promotion applies if cart subtotal is at most this amount"),
    )

    # Conditions - Cart Weight
    min_cart_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("minimum cart weight (kg)"),
        help_text=_("Promotion applies if total cart weight is at least this amount"),
    )

    max_cart_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("maximum cart weight (kg)"),
        help_text=_("Promotion applies if total cart weight is at most this amount"),
    )

    # Conditions - Item Count
    min_item_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("minimum item count"),
        help_text=_("Promotion applies if cart has at least this many items"),
    )

    max_item_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("maximum item count"),
        help_text=_("Promotion applies if cart has at most this many items"),
    )

    # Geographic restrictions
    zones = models.ManyToManyField(
        "ShippingZone",
        blank=True,
        related_name="shipping_promotions",
        verbose_name=_("shipping zones"),
        help_text=_("Promotion only applies to these zones (empty = all zones)"),
    )

    # Shipping method restrictions
    shipping_methods = models.ManyToManyField(
        "cart.ShippingMethod",
        blank=True,
        related_name="shipping_promotions",
        verbose_name=_("shipping methods"),
        help_text=_("Promotion only applies to these shipping methods (empty = all methods)"),
    )

    # Product/Category conditions
    requires_products = models.ManyToManyField(
        "catalog.Product",
        blank=True,
        related_name="required_for_shipping_promotions",
        verbose_name=_("requires products"),
        help_text=_("Promotion only applies if cart contains these products"),
    )

    requires_categories = models.ManyToManyField(
        "catalog.Category",
        blank=True,
        related_name="required_for_shipping_promotions",
        verbose_name=_("requires categories"),
        help_text=_("Promotion only applies if cart contains products from these categories"),
    )

    excludes_products = models.ManyToManyField(
        "catalog.Product",
        blank=True,
        related_name="excluded_from_shipping_promotions",
        verbose_name=_("excludes products"),
        help_text=_("Promotion does not apply if cart contains these products"),
    )

    excludes_categories = models.ManyToManyField(
        "catalog.Category",
        blank=True,
        related_name="excluded_from_shipping_promotions",
        verbose_name=_("excludes categories"),
        help_text=_("Promotion does not apply if cart contains products from these categories"),
    )

    # Customer restrictions
    customer_groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="shipping_promotions",
        verbose_name=_("customer groups"),
        help_text=_("Promotion only applies to these customer groups (empty = all customers)"),
    )

    first_time_customers_only = models.BooleanField(
        default=False,
        verbose_name=_("first-time customers only"),
        help_text=_("Promotion only applies to customers with no previous orders"),
    )

    # Time restrictions
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("start date"),
        help_text=_("Promotion is active starting from this date/time"),
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("end date"),
        help_text=_("Promotion is active until this date/time"),
    )

    # Promotion behavior
    priority = models.IntegerField(
        default=0,
        verbose_name=_("priority"),
        help_text=_("Promotions are evaluated in priority order (higher = evaluated first)"),
    )

    stop_further_promotions = models.BooleanField(
        default=False,
        verbose_name=_("stop further promotions"),
        help_text=_("If this promotion matches, do not evaluate lower priority promotions"),
    )

    controls_visibility = models.BooleanField(
        default=False,
        verbose_name=_("controls method visibility"),
        help_text=_(
            "When enabled, linked shipping methods are only shown at checkout when this promotion's conditions are met"
        ),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text=_("Whether this promotion is currently active"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_shipping_promotions",
        verbose_name=_("created by"),
    )

    class Meta:
        db_table = "shipping_shippingrule"
        ordering = ["-priority", "name"]
        verbose_name = _("shipping promotion")
        verbose_name_plural = _("shipping promotions")
        indexes = [
            models.Index(fields=["is_active", "-priority"]),
            models.Index(fields=["-priority"]),
            models.Index(fields=["start_date", "end_date"]),
        ]

    def __str__(self):
        return self.name

    def is_time_valid(self):
        """Check if promotion is valid based on time restrictions"""
        now = timezone.now()

        if self.start_date and now < self.start_date:
            return False

        return not (self.end_date and now > self.end_date)

    def matches_cart_value(self, cart_value):
        """Check if cart value matches promotion conditions"""
        if self.min_cart_value and cart_value < self.min_cart_value:
            return False

        return not (self.max_cart_value and cart_value > self.max_cart_value)

    def matches_cart_weight(self, cart_weight):
        """Check if cart weight matches promotion conditions"""
        from decimal import Decimal

        if self.min_cart_weight and cart_weight < Decimal(str(self.min_cart_weight)):
            return False

        return not (self.max_cart_weight and cart_weight > Decimal(str(self.max_cart_weight)))

    def matches_item_count(self, item_count):
        """Check if item count matches promotion conditions"""
        if self.min_item_count and item_count < self.min_item_count:
            return False

        return not (self.max_item_count and item_count > self.max_item_count)

    def matches_address(self, address):
        """Check if address matches promotion's zone restrictions"""
        # If no zones specified, promotion applies to all addresses
        if not self.zones.exists():
            return True

        # Check if address matches any of the zones
        return any(zone.matches_address(address) for zone in self.zones.all())

    def matches_shipping_method(self, shipping_method):
        """Check if shipping method matches promotion restrictions"""
        # If no methods specified, promotion applies to all methods
        if not self.shipping_methods.exists():
            return True

        return self.shipping_methods.filter(id=shipping_method.id).exists()

    def matches_cart_products(self, cart):
        """Check if cart products match promotion conditions"""
        cart_products = {item.product for item in cart.items.all()}
        cart_categories = {
            item.product.category for item in cart.items.all() if item.product.category
        }

        # Check required products
        if self.requires_products.exists():
            required = set(self.requires_products.all())
            if not required.intersection(cart_products):
                return False

        # Check required categories
        if self.requires_categories.exists():
            required_cats = set(self.requires_categories.all())
            if not required_cats.intersection(cart_categories):
                return False

        # Check excluded products
        if self.excludes_products.exists():
            excluded = set(self.excludes_products.all())
            if excluded.intersection(cart_products):
                return False

        # Check excluded categories
        if self.excludes_categories.exists():
            excluded_cats = set(self.excludes_categories.all())
            if excluded_cats.intersection(cart_categories):
                return False

        return True

    def matches_customer(self, user):
        """Check if customer matches promotion restrictions"""
        # Check customer groups
        if self.customer_groups.exists():
            if not user or not user.is_authenticated:
                return False
            user_groups = set(user.groups.all())
            rule_groups = set(self.customer_groups.all())
            if not user_groups.intersection(rule_groups):
                return False

        # Check first-time customer restriction
        if self.first_time_customers_only:
            if not user or not user.is_authenticated:
                return False
            if user.orders.filter(status="delivered").exists():
                return False

        return True

    def applies_to_cart(self, cart, address, shipping_method, user=None):
        """
        Check if this promotion applies to the given cart and conditions

        Args:
            cart: Cart instance
            address: Address instance or dict
            shipping_method: ShippingMethod instance
            user: User instance (optional)

        Returns:
            tuple: (applies: bool, reason: str)
        """
        if not self.is_active:
            return False, _("Promotion is not active")

        if not self.is_time_valid():
            return False, _("Promotion is not valid at this time")

        if not self.matches_cart_value(cart.subtotal):
            return False, _("Cart value does not match promotion conditions")

        if not self.matches_cart_weight(cart.total_weight):
            return False, _("Cart weight does not match promotion conditions")

        if not self.matches_item_count(cart.total_items):
            return False, _("Item count does not match promotion conditions")

        if not self.matches_address(address):
            return False, _("Address does not match promotion zones")

        if not self.matches_shipping_method(shipping_method):
            return False, _("Shipping method does not match promotion")

        if not self.matches_cart_products(cart):
            return False, _("Cart products do not match promotion conditions")

        if user and not self.matches_customer(user):
            return False, _("Customer does not match promotion conditions")

        return True, _("Promotion applies")

    def calculate_adjustment(self, base_cost):
        """
        Calculate the shipping cost adjustment based on this promotion

        Args:
            base_cost: Base shipping cost (Decimal or Money)

        Returns:
            Money: Adjusted shipping cost
        """
        from decimal import Decimal

        from djmoney.money import Money

        # Convert base_cost to Money if it's Decimal
        if isinstance(base_cost, Decimal):
            from core.utils import get_default_currency

            base_cost = Money(base_cost, get_default_currency())

        if self.promotion_type == "free_shipping":
            return Money(0, base_cost.currency)

        elif self.promotion_type == "override_cost":
            if self.promotion_value:
                return Money(self.promotion_value.amount, base_cost.currency)
            return base_cost

        elif self.promotion_type == "discount_percentage":
            if self.promotion_value:
                discount_percent = self.promotion_value.amount / 100
                adjusted = base_cost.amount * (1 - discount_percent)
                return Money(max(adjusted, 0), base_cost.currency)
            return base_cost

        elif self.promotion_type == "discount_fixed":
            if self.promotion_value:
                adjusted = base_cost.amount - self.promotion_value.amount
                return Money(max(adjusted, 0), base_cost.currency)
            return base_cost

        elif self.promotion_type == "surcharge_fixed":
            if self.promotion_value:
                return Money(base_cost.amount + self.promotion_value.amount, base_cost.currency)
            return base_cost

        elif self.promotion_type == "surcharge_percentage":
            if self.promotion_value:
                surcharge_percent = self.promotion_value.amount / 100
                return Money(base_cost.amount * (1 + surcharge_percent), base_cost.currency)
            return base_cost

        return base_cost


class ShippingRateTable(models.Model):
    """
    Tiered rate tables for weight-based and price-based shipping calculations
    Example: "0-5kg = $10, 5-10kg = $15, 10+ kg = $20"
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200,
        verbose_name=_("table name"),
        help_text=_("Internal name for this rate table"),
    )

    description = models.TextField(blank=True, verbose_name=_("description"))

    # Table basis (what the tiers are based on)
    BASIS_TYPES = [
        ("weight", _("Cart Weight")),
        ("price", _("Cart Subtotal")),
        ("quantity", _("Item Quantity")),
    ]
    basis_type = models.CharField(
        max_length=20,
        choices=BASIS_TYPES,
        verbose_name=_("basis type"),
        help_text=_("What metric this table is based on"),
    )

    # Associated shipping method (required - each table belongs to a method)
    shipping_method = models.ForeignKey(
        "cart.ShippingMethod",
        on_delete=models.CASCADE,
        related_name="rate_tables",
        verbose_name=_("shipping method"),
        help_text=_("Shipping method this table provides pricing for"),
    )

    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_rate_tables",
        verbose_name=_("created by"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("shipping rate table")
        verbose_name_plural = _("shipping rate tables")
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["basis_type"]),
        ]

    def __str__(self):
        return self.name

    def get_rate_for_value(self, value):
        """
        Get shipping rate for a given value based on tiered rates

        Args:
            value: Cart weight, price, or quantity (Decimal)

        Returns:
            Money: Calculated shipping cost, or None if no matching tier
        """
        from decimal import Decimal

        from djmoney.money import Money

        # Convert value to Decimal if needed
        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        # Find matching tier
        matching_tier = None
        for tier in self.tiers.filter(is_active=True).order_by("min_value"):
            # Check if value falls within this tier's range
            if tier.min_value is not None and value < tier.min_value:
                continue
            if tier.max_value is not None and value > tier.max_value:
                continue

            matching_tier = tier
            break

        if matching_tier:
            return Money(matching_tier.rate.amount, matching_tier.rate.currency)

        return None

    def applies_to_address(self, address):
        """Check if this rate table applies to the given address.
        Zone restrictions are inherited from the parent shipping method.
        """
        return True


class ShippingRateTier(models.Model):
    """
    Individual tier within a rate table
    Example: "5kg - 10kg costs $15"
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    rate_table = models.ForeignKey(
        "ShippingRateTable",
        on_delete=models.CASCADE,
        related_name="tiers",
        verbose_name=_("rate table"),
    )

    # Tier range
    min_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("minimum value"),
        help_text=_("Minimum cart weight/price/quantity (null = no minimum)"),
    )

    max_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("maximum value"),
        help_text=_("Maximum cart weight/price/quantity (null = no maximum)"),
    )

    # Rate for this tier
    rate = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        verbose_name=_("shipping rate"),
        help_text=_("Shipping cost for this tier"),
    )

    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        ordering = ["rate_table", "min_value"]
        verbose_name = _("shipping rate tier")
        verbose_name_plural = _("shipping rate tiers")
        indexes = [
            models.Index(fields=["rate_table", "min_value"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        min_str = str(self.min_value) if self.min_value is not None else _("no min")
        max_str = str(self.max_value) if self.max_value is not None else _("no max")
        return f"{self.rate_table.name}: {min_str} - {max_str} = {self.rate}"

    def contains_value(self, value):
        """Check if the given value falls within this tier's range"""
        from decimal import Decimal

        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        if self.min_value is not None and value < self.min_value:
            return False

        return not (self.max_value is not None and value > self.max_value)


class Location(models.Model):
    """
    Physical locations for in-store pickup, warehouse fulfillment, or merchant fleet dispatch.

    Used by built-in shipping methods:
    - In-Store Collection: Customers pick up orders at retail locations
    - Merchant Fleet: Dispatch point for merchant's own delivery vehicles
    - Future: Warehouse locations for inventory management
    """

    LOCATION_TYPES = [
        ("store", _("Retail Store")),
        ("warehouse", _("Warehouse")),
        ("fulfillment_center", _("Fulfillment Center")),
        ("dispatch_center", _("Dispatch Center")),
    ]

    # Basic information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200,
        verbose_name=_("location name"),
        help_text=_('e.g., "Downtown Store", "Main Warehouse"'),
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("location code"),
        help_text=_('Unique identifier for this location (e.g., "STORE-NYC-01")'),
    )
    location_type = models.CharField(
        max_length=30, choices=LOCATION_TYPES, default="store", verbose_name=_("location type")
    )

    # Address
    address1 = models.CharField(max_length=255, verbose_name=_("address line 1"))
    address2 = models.CharField(max_length=255, blank=True, verbose_name=_("address line 2"))
    city = models.CharField(max_length=100, verbose_name=_("city"))
    state = models.CharField(max_length=100, verbose_name=_("state/province"))
    postal_code = models.CharField(max_length=20, verbose_name=_("postal code"))
    country = models.CharField(
        max_length=2,
        verbose_name=_("country"),
        help_text=_('ISO 3166-1 alpha-2 country code (e.g., "US", "CA")'),
    )

    # Geocoding (for distance calculations)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("latitude"),
        help_text=_("Decimal degrees (e.g., 40.7128)"),
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("longitude"),
        help_text=_("Decimal degrees (e.g., -74.0060)"),
    )

    # Contact information
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("phone number"))
    email = models.EmailField(blank=True, verbose_name=_("contact email"))

    # Operating hours (JSON structure for flexibility)
    operating_hours = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("operating hours"),
        help_text=_(
            'JSON structure: {"monday": {"open": "09:00", "close": "17:00", "closed": false}, ...}'
        ),
    )

    # Special instructions for pickup/delivery
    pickup_instructions = models.TextField(
        blank=True,
        verbose_name=_("pickup instructions"),
        help_text=_(
            'Instructions for customers picking up orders (e.g., "Enter through side door")'
        ),
    )
    delivery_notes = models.TextField(
        blank=True,
        verbose_name=_("delivery notes"),
        help_text=_("Internal notes for delivery fleet"),
    )

    # Availability settings
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Whether this location is currently operational"),
    )
    accepts_pickup = models.BooleanField(
        default=True,
        verbose_name=_("accepts pickup orders"),
        help_text=_("Allow customers to pick up orders at this location"),
    )
    accepts_delivery_dispatch = models.BooleanField(
        default=False,
        verbose_name=_("accepts delivery dispatch"),
        help_text=_("Use this location as dispatch point for merchant fleet deliveries"),
    )

    # Capacity and restrictions
    max_daily_pickups = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("max daily pickups"),
        help_text=_("Maximum number of pickup orders per day (blank = unlimited)"),
    )
    pickup_preparation_time = models.PositiveIntegerField(
        default=60,
        verbose_name=_("pickup preparation time (minutes)"),
        help_text=_("Time needed to prepare order for pickup after placement"),
    )

    # Geographic coverage (for delivery fleet)
    delivery_radius = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("delivery radius (km)"),
        help_text=_("Maximum delivery distance from this location for merchant fleet"),
    )

    # Integration with shipping zones
    zones = models.ManyToManyField(
        "ShippingZone",
        blank=True,
        related_name="locations",
        verbose_name=_("shipping zones"),
        help_text=_("Zones this location services"),
    )

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_locations",
        verbose_name=_("created by"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["location_type", "is_active"]),
            models.Index(fields=["country", "state", "city"]),
            models.Index(fields=["is_active", "accepts_pickup"]),
            models.Index(fields=["is_active", "accepts_delivery_dispatch"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def full_address(self):
        """Return complete formatted address."""
        parts = [self.address1]
        if self.address2:
            parts.append(self.address2)
        parts.append(f"{self.city}, {self.state} {self.postal_code}")
        parts.append(self.country)
        return ", ".join(parts)

    @property
    def coordinates(self):
        """Return (latitude, longitude) tuple if available."""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    def is_open_at(self, datetime_obj=None):
        """
        Check if location is open at a specific datetime.

        Args:
            datetime_obj: datetime object to check (defaults to now)

        Returns:
            bool: True if location is open at that time
        """
        from django.utils import timezone as tz

        if not self.is_active:
            return False

        if not self.operating_hours:
            # No hours specified = always open
            return True

        dt = datetime_obj or tz.now()
        day_name = dt.strftime("%A").lower()

        day_hours = self.operating_hours.get(day_name)
        if not day_hours:
            return True  # No restriction for this day

        if day_hours.get("closed", False):
            return False

        # Check if current time is within operating hours
        open_time = day_hours.get("open")
        close_time = day_hours.get("close")

        if not open_time or not close_time:
            return True

        current_time = dt.time()
        from datetime import datetime as dt_class

        open_dt = dt_class.strptime(open_time, "%H:%M").time()
        close_dt = dt_class.strptime(close_time, "%H:%M").time()

        return open_dt <= current_time <= close_dt

    def can_accept_pickup(self, order_datetime=None):
        """
        Check if location can accept a pickup order.

        Args:
            order_datetime: When the order will be ready (defaults to now + prep time)

        Returns:
            tuple: (can_accept: bool, reason: str)
        """
        from datetime import timedelta

        from django.utils import timezone as tz

        if not self.is_active:
            return False, _("Location is not active")

        if not self.accepts_pickup:
            return False, _("Location does not accept pickup orders")

        # Check if there's a max daily limit
        if self.max_daily_pickups:
            dt = order_datetime or tz.now()
            from orders.models import Order

            today_pickups = Order.objects.filter(
                pickup_location=self, pickup_date__date=dt.date()
            ).count()

            if today_pickups >= self.max_daily_pickups:
                return False, _("Location has reached daily pickup capacity")

        # Check operating hours for pickup time
        if order_datetime:
            if not self.is_open_at(order_datetime):
                return False, _("Location is closed at requested pickup time")
        else:
            # Check if will be ready within prep time during operating hours
            ready_time = tz.now() + timedelta(minutes=self.pickup_preparation_time)
            if not self.is_open_at(ready_time):
                return False, _("Location will be closed when order is ready")

        return True, _("Location available for pickup")

    def calculate_distance_to(self, latitude, longitude):
        """
        Calculate distance from this location to given coordinates.

        Uses Haversine formula for great-circle distance.

        Args:
            latitude: Destination latitude
            longitude: Destination longitude

        Returns:
            Decimal: Distance in kilometers, or None if this location has no coordinates
        """
        if not self.coordinates:
            return None

        from math import asin, cos, radians, sin, sqrt

        # Convert to radians
        lat1, lon1 = radians(float(self.latitude)), radians(float(self.longitude))
        lat2, lon2 = radians(float(latitude)), radians(float(longitude))

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))

        # Earth's radius in kilometers
        radius = 6371

        return Decimal(str(c * radius))

    def is_within_delivery_range(self, latitude, longitude):
        """
        Check if coordinates are within this location's delivery radius.

        Args:
            latitude: Destination latitude
            longitude: Destination longitude

        Returns:
            tuple: (in_range: bool, distance: Decimal or None)
        """
        if not self.accepts_delivery_dispatch:
            return False, None

        if not self.delivery_radius:
            # No radius limit = unlimited range
            return True, None

        distance = self.calculate_distance_to(latitude, longitude)
        if distance is None:
            # Can't calculate without coordinates
            return False, None

        return distance <= self.delivery_radius, distance

    def get_available_pickup_slots(self, date):
        """
        Get available pickup time slots for a given date.

        Args:
            date: Date object for which to get slots

        Returns:
            list: List of available time slot dictionaries
                [{'start': '09:00', 'end': '09:30', 'available': True}, ...]
        """
        from datetime import datetime, timedelta

        if not self.is_active or not self.accepts_pickup:
            return []

        day_name = date.strftime("%A").lower()
        day_hours = self.operating_hours.get(day_name, {})

        if day_hours.get("closed", False):
            return []

        open_time = day_hours.get("open", "09:00")
        close_time = day_hours.get("close", "17:00")

        # Generate 30-minute slots
        slots = []
        current = datetime.strptime(open_time, "%H:%M")
        end = datetime.strptime(close_time, "%H:%M")

        while current < end:
            slot_end = current + timedelta(minutes=30)
            if slot_end > end:
                slot_end = end

            slots.append(
                {
                    "start": current.strftime("%H:%M"),
                    "end": slot_end.strftime("%H:%M"),
                    "available": True,  # Could check capacity here
                }
            )

            current = slot_end

        return slots
