import secrets
import string
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_pairing_code():
    """Generate an 8-character alphanumeric pairing code (uppercase, no ambiguous chars)."""
    chars = string.ascii_uppercase + string.digits
    # Remove ambiguous characters: O, 0, I, 1, L
    chars = (
        chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "").replace("L", "")
    )
    return "".join(secrets.choice(chars) for _ in range(8))


class StoreGroup(models.Model):
    """
    Groups retail store locations for organization and settings inheritance.
    Settings cascade: Site Default → Store Group → Individual Store → Terminal
    """

    name = models.CharField(
        _("group name"), max_length=200, help_text=_('e.g. "NZ Stores", "Singapore Region"')
    )
    code = models.CharField(
        _("group code"),
        max_length=50,
        unique=True,
        db_index=True,
        help_text=_('Short unique code e.g. "NZ", "SG"'),
    )

    # Regional settings (blank = inherit from site default)
    currency = models.CharField(
        _("currency"),
        max_length=3,
        blank=True,
        help_text=_("Currency for stores in this group (e.g. NZD, SGD). Blank = site default."),
    )
    language = models.CharField(
        _("language"),
        max_length=10,
        blank=True,
        help_text=_("Default language for stores in this group. Blank = site default."),
    )
    timezone = models.CharField(
        _("timezone"),
        max_length=50,
        blank=True,
        help_text=_("Timezone for reports (e.g. Pacific/Auckland). Blank = site default."),
    )

    # Extensibility for future settings
    settings = models.JSONField(
        _("additional settings"),
        default=dict,
        blank=True,
        help_text=_("Additional group-level settings as JSON."),
    )

    sort_order = models.PositiveIntegerField(
        _("sort order"), default=0, help_text=_("Lower numbers appear first in lists.")
    )
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Store Group")
        verbose_name_plural = _("Store Groups")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    @property
    def effective_currency(self):
        """Return group currency or fall back to site default."""
        if self.currency:
            return self.currency
        from core.models import SiteSettings

        site_settings = SiteSettings.objects.first()
        return str(site_settings.default_currency) if site_settings else "EUR"

    @property
    def store_count(self):
        """Number of retail warehouses in this group."""
        return self.warehouses.filter(is_retail_location=True).count()


class POSTerminal(models.Model):
    """A physical POS device (tablet, register, terminal)."""

    name = models.CharField(
        _("terminal name"),
        max_length=200,
        help_text=_('Friendly name for this terminal, e.g. "Front Register"'),
    )
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique identifier for this terminal"),
    )
    warehouse = models.ForeignKey(
        "catalog.Warehouse",
        on_delete=models.PROTECT,
        related_name="pos_terminals",
        limit_choices_to={"is_retail_location": True},
        verbose_name=_("store location"),
        help_text=_("The physical store (warehouse) this terminal is located in"),
    )
    pairing_code = models.CharField(
        _("pairing code"),
        max_length=8,
        unique=True,
        default=generate_pairing_code,
        help_text=_("Code used to pair a new device with this terminal"),
    )

    # Hardware configuration stored as JSON, applied by the frontend
    hardware_config = models.JSONField(
        _("hardware configuration"),
        default=dict,
        blank=True,
        help_text=_(
            "Terminal hardware settings. Example: "
            '{"printer": {"type": "network", "url": "http://192.168.1.100:9100"}, '
            '"scanner": "keyboard_wedge", "cash_drawer": true, "customer_display": true}'
        ),
    )

    currency = models.CharField(
        _("currency"),
        max_length=3,
        blank=True,
        help_text=_("Currency for this terminal (e.g. NZD, SGD). Blank = site default."),
    )

    order_sync_days = models.PositiveIntegerField(
        _("order history (days)"),
        default=14,
        help_text=_(
            "Number of days of order history to sync to the terminal for offline access. "
            "Higher values increase storage usage and sync time. Recommended: 7-30 days."
        ),
    )
    order_sync_limit = models.PositiveIntegerField(
        _("order sync limit"),
        default=500,
        help_text=_(
            "Maximum number of orders to cache on the terminal. POS orders are prioritised "
            "over web orders. Higher values increase device storage and sync time. "
            "Recommended: 200-1000."
        ),
    )

    is_active = models.BooleanField(_("active"), default=True)
    last_heartbeat = models.DateTimeField(
        _("last heartbeat"),
        null=True,
        blank=True,
        help_text=_("Last time this terminal reported as online"),
    )
    remote_unlock_at = models.DateTimeField(
        _("remote unlock at"),
        null=True,
        blank=True,
        help_text=_(
            "Set by admin to remotely unlock the terminal. Frontend polls and unlocks if this is newer than lock time."
        ),
    )
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="pos_terminals",
        verbose_name=_("assigned staff"),
        help_text=_("Staff members authorized to use this terminal"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("POS Terminal")
        verbose_name_plural = _("POS Terminals")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.warehouse.pos_display_name or self.warehouse.name})"

    @property
    def effective_currency(self):
        """Return terminal → store group → site default currency."""
        if self.currency:
            return self.currency
        # Check warehouse's store group
        if self.warehouse and self.warehouse.store_group:
            if self.warehouse.store_group.currency:
                return self.warehouse.store_group.currency
        # Fall back to site default
        from core.models import SiteSettings

        site_settings = SiteSettings.objects.first()
        return str(site_settings.default_currency) if site_settings else "EUR"

    @property
    def effective_language(self):
        """Return store group language or empty (site default)."""
        if self.warehouse and self.warehouse.store_group:
            return self.warehouse.store_group.language or ""
        return ""

    def regenerate_pairing_code(self):
        """Generate a new pairing code for this terminal."""
        self.pairing_code = generate_pairing_code()
        self.save(update_fields=["pairing_code"])
        return self.pairing_code


def generate_display_pairing_code():
    """Generate a 6-digit numeric pairing code for customer display."""
    return f"{secrets.randbelow(1000000):06d}"


class DisplayPairingCode(models.Model):
    """Short-lived pairing code for customer display authentication."""

    terminal = models.ForeignKey(
        POSTerminal,
        on_delete=models.CASCADE,
        related_name="display_pairing_codes",
        verbose_name=_("terminal"),
    )
    code = models.CharField(_("pairing code"), max_length=6, default=generate_display_pairing_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(_("expires at"))
    used_at = models.DateTimeField(_("used at"), null=True, blank=True)

    class Meta:
        verbose_name = _("Display Pairing Code")
        verbose_name_plural = _("Display Pairing Codes")
        indexes = [
            models.Index(fields=["terminal", "code", "expires_at"]),
        ]

    def __str__(self):
        return f"{self.terminal.name} - {self.code}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            from datetime import timedelta

            from django.utils import timezone

            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    @classmethod
    def create_for_terminal(cls, terminal):
        """Create a new pairing code, invalidating any existing unused codes."""
        from datetime import timedelta

        from django.utils import timezone

        # Delete any existing unused codes for this terminal
        cls.objects.filter(terminal=terminal, used_at__isnull=True).delete()
        return cls.objects.create(
            terminal=terminal, expires_at=timezone.now() + timedelta(minutes=5)
        )

    @classmethod
    def validate_code(cls, terminal_uuid, code):
        """
        Validate a pairing code. Returns True if valid, marks as used.
        Code must be unused, not expired, and match the terminal.
        """
        from django.utils import timezone

        pairing = (
            cls.objects.filter(
                terminal__uuid=terminal_uuid,
                code=code,
                expires_at__gt=timezone.now(),
                used_at__isnull=True,
            )
            .select_related("terminal")
            .first()
        )

        if pairing:
            pairing.used_at = timezone.now()
            pairing.save(update_fields=["used_at"])
            return True
        return False


class POSShift(models.Model):
    """A cashier's working shift on a terminal."""

    terminal = models.ForeignKey(
        POSTerminal, on_delete=models.CASCADE, related_name="shifts", verbose_name=_("terminal")
    )
    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pos_shifts",
        verbose_name=_("cashier"),
    )

    started_at = models.DateTimeField(_("shift started"), auto_now_add=True)
    ended_at = models.DateTimeField(_("shift ended"), null=True, blank=True)

    # Cash tracking
    opening_cash = models.DecimalField(
        _("opening cash"),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Cash in drawer at shift start"),
    )
    closing_cash = models.DecimalField(
        _("closing cash"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Actual cash counted at shift end"),
    )
    expected_cash = models.DecimalField(
        _("expected cash"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Calculated expected cash based on transactions"),
    )
    cash_difference = models.DecimalField(
        _("cash difference"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Difference between closing and expected cash"),
    )

    # Shift totals (updated as transactions occur)
    total_sales = models.DecimalField(_("total sales"), max_digits=10, decimal_places=2, default=0)
    total_refunds = models.DecimalField(
        _("total refunds"), max_digits=10, decimal_places=2, default=0
    )
    total_transactions = models.PositiveIntegerField(_("total transactions"), default=0)

    # Manual discount tracking for shift reports
    total_manual_discounts = models.DecimalField(
        _("total manual discounts"),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Total value of manual discounts given during shift"),
    )
    manual_discount_count = models.PositiveIntegerField(
        _("manual discount count"),
        default=0,
        help_text=_("Number of manual discounts applied during shift"),
    )

    notes = models.TextField(_("notes"), blank=True)

    class Meta:
        verbose_name = _("POS Shift")
        verbose_name_plural = _("POS Shifts")
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.cashier.get_full_name() or self.cashier.username} - {self.terminal.name} ({self.started_at:%Y-%m-%d %H:%M})"

    @property
    def is_open(self):
        return self.ended_at is None

    def close_shift(self, closing_cash_amount):
        """Close this shift and calculate cash difference.

        Uses transaction.atomic() and select_for_update() to prevent race
        conditions between concurrent close attempts and to ensure aggregate
        queries are consistent with the final save.
        """
        from django.db import transaction
        from django.utils import timezone

        with transaction.atomic():
            # Lock the shift row and refetch to prevent concurrent close
            shift = POSShift.objects.select_for_update().get(pk=self.pk)
            if shift.ended_at is not None:
                raise ValueError("Shift is already closed.")

            shift.ended_at = timezone.now()
            shift.closing_cash = closing_cash_amount

            # Calculate expected cash: opening + cash sales - cash refunds + cash in - cash out
            cash_in = (
                shift.cash_movements.filter(movement_type="in").aggregate(
                    total=models.Sum("amount")
                )["total"]
                or 0
            )
            cash_out = (
                shift.cash_movements.filter(movement_type="out").aggregate(
                    total=models.Sum("amount")
                )["total"]
                or 0
            )

            # Cash from sales
            cash_payments = (
                shift.pos_payments.filter(method="cash").aggregate(total=models.Sum("amount"))[
                    "total"
                ]
                or 0
            )
            cash_refund_payments = (
                shift.pos_payments.filter(method="cash", amount__lt=0).aggregate(
                    total=models.Sum("amount")
                )["total"]
                or 0
            )

            shift.expected_cash = (
                shift.opening_cash + cash_payments + cash_refund_payments + cash_in - cash_out
            )
            shift.cash_difference = shift.closing_cash - shift.expected_cash

            shift.save(
                update_fields=["ended_at", "closing_cash", "expected_cash", "cash_difference"]
            )

            # Update self to reflect the changes
            self.ended_at = shift.ended_at
            self.closing_cash = shift.closing_cash
            self.expected_cash = shift.expected_cash
            self.cash_difference = shift.cash_difference


class CashMovement(models.Model):
    """Cash in/out events during a shift (float changes, petty cash, etc.)."""

    MOVEMENT_TYPES = [
        ("in", _("Cash In")),
        ("out", _("Cash Out")),
    ]

    shift = models.ForeignKey(
        POSShift, on_delete=models.CASCADE, related_name="cash_movements", verbose_name=_("shift")
    )
    movement_type = models.CharField(_("type"), max_length=3, choices=MOVEMENT_TYPES)
    amount = models.DecimalField(
        _("amount"), max_digits=10, decimal_places=2, help_text=_("Amount in base currency")
    )
    reason = models.CharField(
        _("reason"),
        max_length=200,
        help_text=_('Reason for cash movement, e.g. "Change float top-up"'),
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pos_cash_movements",
        verbose_name=_("performed by"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Cash Movement")
        verbose_name_plural = _("Cash Movements")
        ordering = ["-created_at"]

    def __str__(self):
        direction = "+" if self.movement_type == "in" else "-"
        return f"{direction}{self.amount} - {self.reason}"


class POSTerminalProvider(models.Model):
    """
    A configured payment terminal provider (e.g. Stripe Terminal).
    One active provider per merchant installation.
    """

    PROVIDER_STATUS = [
        ("unknown", _("Unknown")),
        ("connected", _("Connected")),
        ("error", _("Error")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_key = models.CharField(
        _("provider"),
        max_length=50,
        unique=True,
        help_text=_('Provider identifier, e.g. "stripe_terminal", "manual"'),
    )
    display_name = models.CharField(
        _("display name"),
        max_length=128,
        blank=True,
        help_text=_('Friendly name, e.g. "Stripe Terminal"'),
    )

    # Component package (from upgrade server)
    component = models.ForeignKey(
        "component_updates.ComponentRegistry",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminal_provider_accounts",
        limit_choices_to={"component_type": "terminal_provider"},
        help_text=_("Component package. Null for built-in manual provider."),
    )

    # Encrypted credentials (Stripe secret key, etc.)
    credentials_encrypted = models.JSONField(
        _("credentials"), default=dict, blank=True, help_text=_("Encrypted API credentials")
    )

    # Provider-specific settings (non-secret)
    provider_settings = models.JSONField(
        _("settings"),
        default=dict,
        blank=True,
        help_text=_('Provider-specific settings, e.g. {"stripe_location_id": "tml_xxx"}'),
    )

    is_active = models.BooleanField(_("active"), default=True)

    # Connection health
    connection_status = models.CharField(
        _("connection status"), max_length=20, choices=PROVIDER_STATUS, default="unknown"
    )
    connection_error = models.TextField(_("connection error"), blank=True)
    last_tested_at = models.DateTimeField(_("last tested"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("POS Terminal Provider")
        verbose_name_plural = _("POS Terminal Providers")

    def __str__(self):
        return self.display_name or self.provider_key

    def get_provider_instance(self):
        """Return an instantiated provider with decrypted credentials."""
        from payment_providers.utils.encryption import decrypt_credentials

        from .terminal_providers import TerminalProviderRegistry

        provider_class = TerminalProviderRegistry.get_provider(self.provider_key)
        if not provider_class:
            raise ValueError(f"Unknown terminal provider: {self.provider_key}")

        credentials = (
            decrypt_credentials(self.credentials_encrypted) if self.credentials_encrypted else {}
        )
        return provider_class(credentials=credentials, config=self.provider_settings)

    def set_credentials(self, plain_credentials):
        """Encrypt and store credentials."""
        from payment_providers.utils.encryption import encrypt_credentials

        self.credentials_encrypted = encrypt_credentials(plain_credentials)

    def test_connection(self):
        """Test provider connection and update status."""
        from django.utils import timezone

        try:
            provider = self.get_provider_instance()
            result = provider.test_connection()
            self.connection_status = "connected" if result["success"] else "error"
            self.connection_error = "" if result["success"] else result.get("message", "")
        except Exception as e:
            self.connection_status = "error"
            self.connection_error = str(e)
        self.last_tested_at = timezone.now()
        self.save(update_fields=["connection_status", "connection_error", "last_tested_at"])
        return self.connection_status == "connected"


class POSTerminalReader(models.Model):
    """A physical card reader device registered with a terminal provider."""

    READER_STATUS = [
        ("online", _("Online")),
        ("offline", _("Offline")),
        ("busy", _("Busy")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(
        POSTerminalProvider,
        on_delete=models.CASCADE,
        related_name="readers",
        verbose_name=_("provider"),
    )
    terminal = models.OneToOneField(
        POSTerminal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="card_reader",
        verbose_name=_("assigned terminal"),
        help_text=_("Which POS register this reader is paired with"),
    )

    # Provider identifiers
    provider_reader_id = models.CharField(
        _("provider reader ID"),
        max_length=255,
        help_text=_('Reader ID from the provider, e.g. "tmr_xxx" for Stripe'),
    )
    reader_label = models.CharField(
        _("label"),
        max_length=200,
        blank=True,
        help_text=_('Friendly name, e.g. "Front Counter Reader"'),
    )

    # Reader details (cached from provider)
    reader_type = models.CharField(
        _("reader type"),
        max_length=50,
        blank=True,
        help_text=_('Device type, e.g. "bbpos_wisepos_e", "stripe_s700"'),
    )
    serial_number = models.CharField(_("serial number"), max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)

    # Status
    status = models.CharField(_("status"), max_length=20, choices=READER_STATUS, default="offline")
    last_seen_at = models.DateTimeField(_("last seen"), null=True, blank=True)

    # Splash screen customization
    splash_override_image = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("custom splash screen"),
        help_text=_(
            "Upload a custom splash screen image. Leave blank to auto-generate from site logo."
        ),
    )
    stripe_splash_file_id = models.CharField(
        _("Stripe file ID"),
        max_length=100,
        blank=True,
        help_text=_("Stripe File ID (file_xxx) of the uploaded splash screen"),
    )
    stripe_splash_config_id = models.CharField(
        _("Stripe configuration ID"),
        max_length=100,
        blank=True,
        help_text=_("Stripe Configuration ID (cfg_xxx) for this reader"),
    )
    splash_generated_at = models.DateTimeField(
        _("splash generated at"),
        null=True,
        blank=True,
        help_text=_("When the splash screen was last generated and uploaded"),
    )

    # Generic provider metadata (for non-Stripe providers)
    provider_metadata = models.JSONField(
        _("provider metadata"),
        default=dict,
        blank=True,
        help_text=_("Provider-specific reader data, e.g. Adyen POIID, Square device_code_id."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("POS Card Reader")
        verbose_name_plural = _("POS Card Readers")
        ordering = ["reader_label"]

    def __str__(self):
        label = self.reader_label or self.provider_reader_id
        if self.terminal:
            return f"{label} → {self.terminal.name}"
        return f"{label} (unassigned)"


class POSPayment(models.Model):
    """Payment record for a POS sale. Supports split tender (multiple per order)."""

    PAYMENT_METHODS = [
        ("cash", _("Cash")),
        ("card", _("Card (Manual)")),
        ("terminal_card", _("Card (Terminal)")),
        ("gift_card", _("Gift Card")),
    ]

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="pos_payments",
        verbose_name=_("order"),
    )
    shift = models.ForeignKey(
        POSShift,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pos_payments",
        verbose_name=_("shift"),
    )

    method = models.CharField(_("payment method"), max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(
        _("amount"), max_digits=10, decimal_places=2, help_text=_("Amount paid via this method")
    )

    # Cash-specific fields
    amount_tendered = models.DecimalField(
        _("amount tendered"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Cash amount given by customer"),
    )
    change_given = models.DecimalField(
        _("change given"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Change returned to customer"),
    )

    # Card-specific fields
    card_last_four = models.CharField(
        _("card last four"),
        max_length=4,
        blank=True,
        help_text=_("Last four digits of card number"),
    )
    card_reference = models.CharField(
        _("card reference"),
        max_length=100,
        blank=True,
        help_text=_("Reference number from external card terminal"),
    )

    # Terminal card-specific fields
    provider_payment_id = models.CharField(
        _("provider payment ID"),
        max_length=255,
        blank=True,
        help_text=_("Payment ID from terminal provider, e.g. Stripe PaymentIntent ID"),
    )
    card_brand = models.CharField(
        _("card brand"),
        max_length=20,
        blank=True,
        help_text=_('Card brand, e.g. "visa", "mastercard"'),
    )

    # Gift card-specific fields
    gift_card_code = models.CharField(
        _("gift card code"),
        max_length=50,
        blank=True,
        help_text=_("Gift card code used for payment"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("POS Payment")
        verbose_name_plural = _("POS Payments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_method_display()} - {self.amount} (Order #{self.order_id})"


class ReceiptTemplate(models.Model):
    """
    Receipt layout and content template.

    Scope hierarchy (checked in order):
    1. Specific store template (warehouse set)
    2. Store group template (store_group set)
    3. Default template (both null)
    """

    PAPER_WIDTHS = [
        ("58", _("58mm (32 chars)")),
        ("80", _("80mm (48 chars)")),
    ]

    name = models.CharField(
        _("template name"),
        max_length=200,
        help_text=_('e.g. "Downtown Store Receipt", "Default Receipt"'),
    )
    store_group = models.OneToOneField(
        "StoreGroup",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="receipt_template",
        verbose_name=_("store group"),
        help_text=_(
            "Template for all stores in this group. Leave blank for default or specific store."
        ),
    )
    warehouse = models.OneToOneField(
        "catalog.Warehouse",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="receipt_template",
        limit_choices_to={"is_retail_location": True},
        verbose_name=_("specific store"),
        help_text=_("Template for this specific store. Overrides group template."),
    )

    # Paper
    paper_width = models.CharField(
        _("paper width"),
        max_length=4,
        choices=PAPER_WIDTHS,
        default="80",
        help_text=_("Receipt paper width. 80mm is standard for most thermal printers."),
    )

    # Header
    logo = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("logo"),
        help_text=_("Monochrome logo image. Max 384px wide for 80mm paper, 192px for 58mm."),
    )
    header_text = models.CharField(
        _("header text"),
        max_length=200,
        blank=True,
        help_text=_("Store name on receipt. Leave blank to use the store POS display name."),
    )
    show_store_address = models.BooleanField(_("show address"), default=True)
    custom_address = models.TextField(
        _("custom address"),
        blank=True,
        help_text=_("Custom receipt address. Leave blank to use the store warehouse address."),
    )
    show_store_phone = models.BooleanField(_("show phone"), default=True)
    custom_phone = models.CharField(
        _("custom phone"),
        max_length=50,
        blank=True,
        help_text=_("Leave blank to use the store contact phone."),
    )
    show_store_email = models.BooleanField(_("show email"), default=False)
    custom_email = models.EmailField(
        _("custom email"), blank=True, help_text=_("Leave blank to use the store contact email.")
    )

    # Business / Tax details
    tax_id_label = models.CharField(
        _("tax ID label"),
        max_length=50,
        blank=True,
        help_text=_('Label for your tax number, e.g. "GST No.", "VAT No.", "ABN", "Tax ID"'),
    )
    tax_id_number = models.CharField(
        _("tax ID number"),
        max_length=100,
        blank=True,
        help_text=_("Your tax identification number"),
    )
    business_registration = models.CharField(
        _("business registration"),
        max_length=200,
        blank=True,
        help_text=_("Business registration number"),
    )

    # Body options
    show_sku = models.BooleanField(
        _("show SKU"), default=False, help_text=_("Display product SKU on receipt items")
    )
    show_cashier = models.BooleanField(
        _("show cashier"), default=True, help_text=_("Display cashier name on receipt")
    )
    show_terminal_name = models.BooleanField(
        _("show terminal name"), default=False, help_text=_("Display terminal name on receipt")
    )

    # Footer
    footer_text = models.CharField(
        _("footer text"),
        max_length=500,
        blank=True,
        default="Thank you for your purchase!",
        help_text=_("Custom message at the bottom of the receipt"),
    )
    return_policy = models.TextField(
        _("return policy"),
        blank=True,
        help_text=_("Short return policy printed in small text at the bottom"),
    )

    # QR Code promo
    qr_enabled = models.BooleanField(
        _("enable QR code"),
        default=False,
        help_text=_("Print a QR code at the bottom of the receipt"),
    )
    qr_url = models.URLField(
        _("QR code URL"),
        blank=True,
        help_text=_("URL encoded in the QR code (e.g. review page, discount page, website)"),
    )
    qr_label = models.CharField(
        _("QR code label"),
        max_length=200,
        blank=True,
        help_text=_(
            'Text printed below the QR code, e.g. "Scan for 10% off your next online order"'
        ),
    )

    # Branding
    show_powered_by = models.BooleanField(
        _('show "Powered by Spwig POS"'),
        default=True,
        help_text=_("Display Spwig branding at the bottom of the receipt"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Receipt Template")
        verbose_name_plural = _("Receipt Templates")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_scope_display()})"

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        if self.store_group and self.warehouse:
            raise ValidationError(
                _(
                    "A template cannot be assigned to both a store group and a specific store. Choose one."
                )
            )

    def get_scope_display(self):
        """Return human-readable scope for admin display."""
        if self.warehouse:
            return self.warehouse.pos_display_name or self.warehouse.name
        if self.store_group:
            return f"{self.store_group.name} ({_('Group')})"
        return _("Default")

    def get_effective_address(self):
        """Return custom address or fall back to warehouse address."""
        if self.custom_address:
            return self.custom_address
        if self.warehouse:
            return self.warehouse.full_address
        return ""

    def get_effective_phone(self):
        """Return custom phone or fall back to warehouse contact phone."""
        if self.custom_phone:
            return self.custom_phone
        if self.warehouse:
            return self.warehouse.contact_phone
        return ""

    def get_effective_email(self):
        """Return custom email or fall back to warehouse contact email."""
        if self.custom_email:
            return self.custom_email
        if self.warehouse:
            return self.warehouse.contact_email
        return ""

    def get_effective_header(self):
        """Return header text or fall back to warehouse POS display name."""
        if self.header_text:
            return self.header_text
        if self.warehouse:
            return self.warehouse.pos_display_name or self.warehouse.name
        return ""


class PromoSlide(models.Model):
    """
    Promotional slide for POS customer display.

    Scope hierarchy:
    - Both store_group and warehouse null = All Stores
    - Only store_group set = All stores in that group
    - Only warehouse set = Specific store only
    """

    store_group = models.ForeignKey(
        "StoreGroup",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="promo_slides",
        verbose_name=_("store group"),
        help_text=_("Show in all stores in this group. Leave blank for All or specific store."),
    )
    warehouse = models.ForeignKey(
        "catalog.Warehouse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="promo_slides",
        limit_choices_to={"is_retail_location": True},
        verbose_name=_("specific store"),
        help_text=_("Show in this specific store only. Overrides group."),
    )
    image = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("slide image"),
        help_text=_("Recommended size: 1920x1080 or 16:9 aspect ratio."),
    )
    title = models.CharField(
        _("title"), max_length=200, blank=True, help_text=_("Large text overlay on the slide.")
    )
    subtitle = models.CharField(
        _("subtitle"), max_length=500, blank=True, help_text=_("Secondary text below the title.")
    )
    sort_order = models.PositiveIntegerField(
        _("sort order"), default=0, help_text=_("Lower numbers appear first.")
    )
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Promo Slide")
        verbose_name_plural = _("Promo Slides")
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        title = self.title or _("Untitled Slide")
        return f"{title} ({self.get_scope_display()})"

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        if self.store_group and self.warehouse:
            raise ValidationError(
                _(
                    "A slide cannot be assigned to both a store group and a specific store. Choose one."
                )
            )

    def get_scope_display(self):
        """Return human-readable scope for admin display."""
        if self.warehouse:
            return self.warehouse.pos_display_name or self.warehouse.name
        if self.store_group:
            return f"{self.store_group.name} ({_('Group')})"
        return _("All Stores")


class POSStaffDiscount(models.Model):
    """Staff discount permissions and limits for POS manual discounts."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pos_discount_limit",
        verbose_name=_("staff member"),
    )

    # Discount limits
    max_discount_percentage = models.DecimalField(
        _("max discount %"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("10.00"),
        help_text=_("Maximum percentage discount this staff member can apply (0-100)"),
    )
    max_discount_amount = models.DecimalField(
        _("max discount amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Maximum fixed amount discount per transaction. Blank = no limit."),
    )

    # Permission flags
    can_apply_item_discounts = models.BooleanField(
        _("can apply item discounts"),
        default=True,
        help_text=_("Allow applying discounts to individual items"),
    )
    can_apply_cart_discounts = models.BooleanField(
        _("can apply cart discounts"),
        default=True,
        help_text=_("Allow applying discounts to entire cart"),
    )
    requires_reason = models.BooleanField(
        _("requires reason"),
        default=False,
        help_text=_("Staff must provide a reason when applying discounts"),
    )

    # Manager role for approving discounts that exceed limits
    is_manager = models.BooleanField(
        _("is manager"),
        default=False,
        help_text=_("Can approve discounts exceeding other staff limits"),
    )
    manager_pin = models.CharField(
        _("manager PIN"),
        max_length=6,
        blank=True,
        help_text=_(
            "4-6 digit PIN for approving discounts (managers only). "
            "Migrated to hashed storage on first use."
        ),
    )
    manager_pin_hash = models.CharField(
        _("manager PIN (hashed)"),
        max_length=128,
        blank=True,
        help_text=_("PBKDF2-hashed manager PIN"),
    )
    cashier_pin = models.CharField(
        _("cashier PIN"),
        max_length=6,
        blank=True,
        help_text=_(
            "4-6 digit PIN for terminal lock/unlock. Migrated to hashed storage on first use."
        ),
    )
    cashier_pin_hash = models.CharField(
        _("cashier PIN (hashed)"),
        max_length=128,
        blank=True,
        help_text=_("PBKDF2-hashed cashier PIN"),
    )
    card_identifier = models.CharField(
        _("card identifier hash"),
        max_length=64,
        blank=True,
        db_index=True,
        help_text=_("SHA-256 hash of card swipe data for unlock authentication"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("POS Staff Discount")
        verbose_name_plural = _("POS Staff Discounts")

    def save(self, *args, **kwargs):
        """Auto-hash plaintext PINs when saved (e.g., via admin)."""
        from django.contrib.auth.hashers import make_password

        # Hash manager PIN if set as plaintext
        if self.manager_pin and not self.manager_pin_hash:
            self.manager_pin_hash = make_password(self.manager_pin)
            self.manager_pin = ""
        # Hash cashier PIN if set as plaintext
        if self.cashier_pin and not self.cashier_pin_hash:
            self.cashier_pin_hash = make_password(self.cashier_pin)
            self.cashier_pin = ""
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        role = _("Manager") if self.is_manager else _("Staff")
        return f"{name} ({role}) - Max {self.max_discount_percentage}%"

    def validate_discount(self, discount_type, discount_value, cart_subtotal):
        """
        Validate a discount against this user's limits.
        Returns (valid: bool, error_message: str or None, requires_approval: bool)
        """
        if discount_type == "percentage":
            if discount_value > self.max_discount_percentage:
                return False, None, True  # Requires manager approval
        elif discount_type == "fixed":
            if self.max_discount_amount and discount_value > self.max_discount_amount:
                return False, None, True  # Requires manager approval
            # Also check percentage equivalent
            if cart_subtotal > 0:
                pct_equivalent = (discount_value / cart_subtotal) * 100
                if pct_equivalent > self.max_discount_percentage:
                    return False, None, True  # Requires manager approval
        return True, None, False

    def verify_pin(self, pin):
        """Verify if the provided PIN matches this manager's PIN.

        Checks hashed PIN first. Falls back to plaintext for migration:
        on successful plaintext match, auto-hashes and clears plaintext.
        """
        from django.contrib.auth.hashers import check_password, make_password

        if not self.is_manager:
            return False
        # Check hashed PIN first
        if self.manager_pin_hash:
            return check_password(pin, self.manager_pin_hash)
        # Legacy fallback: check plaintext, then auto-migrate to hash
        if self.manager_pin and self.manager_pin == pin:
            self.manager_pin_hash = make_password(pin)
            self.manager_pin = ""
            self.save(update_fields=["manager_pin_hash", "manager_pin"])
            return True
        return False

    def verify_cashier_pin(self, pin):
        """Verify if the provided PIN matches this user's cashier PIN.

        Checks hashed PIN first. Falls back to plaintext for migration.
        """
        from django.contrib.auth.hashers import check_password, make_password

        # Check hashed PIN first
        if self.cashier_pin_hash:
            return check_password(pin, self.cashier_pin_hash)
        # Legacy fallback: check plaintext, then auto-migrate to hash
        if self.cashier_pin and self.cashier_pin == pin:
            self.cashier_pin_hash = make_password(pin)
            self.cashier_pin = ""
            self.save(update_fields=["cashier_pin_hash", "cashier_pin"])
            return True
        return False

    def verify_card(self, card_data):
        """Verify if the provided card swipe data matches this user's registered card."""
        import hashlib

        if not self.card_identifier:
            return False
        return self.card_identifier == hashlib.sha256(card_data.strip().encode()).hexdigest()

    @staticmethod
    def hash_card_data(card_data):
        """Hash raw card swipe data for storage."""
        import hashlib

        return hashlib.sha256(card_data.strip().encode()).hexdigest()


class TerminalLockEvent(models.Model):
    """Audit log for terminal lock/unlock events."""

    EVENT_TYPES = [
        ("lock_manual", _("Manual Lock")),
        ("lock_auto", _("Auto-Lock (Idle Timeout)")),
        ("unlock_cashier", _("Unlock by Cashier")),
        ("unlock_manager", _("Unlock by Manager")),
        ("unlock_card", _("Unlock by Card")),
        ("unlock_biometric", _("Unlock by Biometric")),
        ("unlock_failed", _("Failed Unlock Attempt")),
        ("lockout_triggered", _("Lockout (3+ failures)")),
    ]

    UNLOCK_METHODS = [
        ("pin", _("PIN")),
        ("card", _("Card Swipe")),
        ("biometric", _("Biometric")),
    ]

    terminal = models.ForeignKey(
        POSTerminal,
        on_delete=models.CASCADE,
        related_name="lock_events",
        verbose_name=_("terminal"),
    )
    shift = models.ForeignKey(
        "POSShift",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lock_events",
        verbose_name=_("shift"),
    )
    event_type = models.CharField(
        _("event type"), max_length=20, choices=EVENT_TYPES, db_index=True
    )

    # Who performed the action (cashier for lock, cashier or manager for unlock)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminal_lock_actions",
        verbose_name=_("performed by"),
    )
    # Who was logged in when terminal was locked (for unlock context)
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminal_locks_initiated",
        verbose_name=_("locked by"),
    )

    # Manager override tracking
    manager_override = models.BooleanField(
        _("manager override"),
        default=False,
        help_text=_("True if unlocked by manager instead of original cashier"),
    )

    # Unlock method
    unlock_method = models.CharField(
        _("unlock method"),
        max_length=20,
        choices=UNLOCK_METHODS,
        default="pin",
    )

    # Failed attempt tracking
    failed_attempt_count = models.PositiveIntegerField(
        _("failed attempts"), default=0, help_text=_("Cumulative failed attempts before this event")
    )

    # Cart state at time of event (for audit trail)
    cart_item_count = models.PositiveIntegerField(_("cart items"), default=0)
    cart_total = models.DecimalField(
        _("cart total"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Request metadata
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)

    created_at = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("Terminal Lock Event")
        verbose_name_plural = _("Terminal Lock Events")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["terminal", "created_at"]),
            models.Index(fields=["event_type", "created_at"]),
        ]

    def __str__(self):
        return f"{self.terminal.name} - {self.get_event_type_display()} ({self.created_at:%Y-%m-%d %H:%M})"


class WebAuthnCredential(models.Model):
    """WebAuthn credential for biometric POS terminal unlock (fingerprint/face)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="webauthn_credentials",
        verbose_name=_("user"),
    )
    credential_id = models.BinaryField(
        _("credential ID"),
        unique=True,
    )
    public_key = models.BinaryField(
        _("public key"), help_text=_("CBOR-encoded attested credential data")
    )
    sign_count = models.PositiveIntegerField(
        _("sign count"),
        default=0,
    )
    device_name = models.CharField(
        _("device name"),
        max_length=200,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("WebAuthn Credential")
        verbose_name_plural = _("WebAuthn Credentials")
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        name = self.user.get_full_name() or self.user.email
        return f"{name} - {self.device_name or 'Credential'}"


class ParkedCart(models.Model):
    """
    A parked cart snapshot for later restoration.
    Used when a customer needs to step away and another customer needs to be served.
    """

    terminal = models.ForeignKey(
        POSTerminal,
        on_delete=models.CASCADE,
        related_name="parked_carts",
        verbose_name=_("terminal"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parked_carts",
        verbose_name=_("parked by"),
    )
    parked_at = models.DateTimeField(_("parked at"), auto_now_add=True)
    restored_at = models.DateTimeField(_("restored at"), null=True, blank=True)
    expires_at = models.DateTimeField(
        _("expires at"),
        null=True,
        blank=True,
        help_text=_("Auto-cleanup after this time. Default: 24h from parking."),
    )

    # Cart snapshot
    cart_data = models.JSONField(
        _("cart data"), help_text=_("Full cart snapshot: items, customer, discounts, etc.")
    )

    # Quick reference fields for display
    item_count = models.PositiveIntegerField(_("item count"), default=0)
    total_amount = models.DecimalField(
        _("total amount"), max_digits=10, decimal_places=2, default=0
    )
    customer_name = models.CharField(
        _("customer name"),
        max_length=100,
        blank=True,
        help_text=_("Customer name for quick display in parked carts list"),
    )

    class Meta:
        verbose_name = _("Parked Cart")
        verbose_name_plural = _("Parked Carts")
        ordering = ["-parked_at"]

    def save(self, *args, **kwargs):
        if not self.expires_at and not self.pk:
            from datetime import timedelta

            from django.utils import timezone

            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        customer = self.customer_name or _("Guest")
        return f"{customer} - {self.item_count} items ({self.parked_at:%H:%M})"

    @property
    def is_restored(self):
        return self.restored_at is not None
