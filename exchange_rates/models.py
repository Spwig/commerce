from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal


class ExchangeRateProviderAccount(models.Model):
    """
    Merchant's connection to an exchange rate provider component.
    Pattern follows shipping/models.py ProviderAccount.
    """
    site = models.ForeignKey(
        'sites.Site',
        on_delete=models.CASCADE,
        verbose_name=_("Site"),
        help_text=_("Site this provider account belongs to")
    )

    component = models.ForeignKey(
        'component_updates.ComponentRegistry',
        on_delete=models.PROTECT,
        limit_choices_to={'component_type': 'exchange_rate_provider'},
        related_name='exchange_rate_accounts',
        verbose_name=_("Provider Component"),
        help_text=_("Exchange rate provider component from update system")
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Account Name"),
        help_text=_("Friendly name for this provider account (e.g., 'Main Exchange Rate Provider')")
    )

    credentials = models.BinaryField(
        verbose_name=_("Encrypted Credentials"),
        help_text=_("Encrypted API credentials for this provider")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this provider account is active and should be used for rate fetching")
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary Provider"),
        help_text=_("Use this provider as primary source for exchange rates")
    )

    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Priority"),
        help_text=_("Priority for fallback chain (lower = higher priority)")
    )

    settings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Provider Settings"),
        help_text=_("Provider-specific settings and configuration")
    )

    # Sync tracking
    last_sync_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Sync At"),
        help_text=_("When rates were last successfully fetched")
    )

    sync_status = models.CharField(
        max_length=32,
        choices=[
            ('pending', _('Pending')),
            ('success', _('Success')),
            ('error', _('Error')),
        ],
        default='pending',
        verbose_name=_("Sync Status")
    )

    sync_error_message = models.TextField(
        blank=True,
        verbose_name=_("Sync Error Message"),
        help_text=_("Error message from last sync attempt")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Exchange Rate Provider Account")
        verbose_name_plural = _("Exchange Rate Provider Accounts")
        ordering = ['-is_primary', '-is_active', 'priority', 'name']
        indexes = [
            models.Index(fields=['site', 'is_active']),
            models.Index(fields=['priority']),
            models.Index(fields=['is_primary']),
        ]
        constraints = [
            # Only one primary provider per site
            models.UniqueConstraint(
                fields=['site', 'is_primary'],
                condition=models.Q(is_primary=True),
                name='unique_primary_provider_per_site'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.component.name})"

    def get_provider_instance(self):
        """Get initialized provider instance"""
        from exchange_rates.providers.registry import ProviderRegistry
        from exchange_rates.utils.encryption import decrypt_credentials

        provider_class = ProviderRegistry.get_provider(self.component.slug)
        if not provider_class:
            raise ValueError(f"Provider {self.component.slug} not found in registry")

        # Decrypt credentials and pass to provider
        credentials = decrypt_credentials(self.credentials)
        return provider_class(credentials=credentials, config=self.settings)


class ExchangeRate(models.Model):
    """
    Cached exchange rates from providers.
    Reduces API calls and provides fallback when provider is down.
    """
    provider_account = models.ForeignKey(
        ExchangeRateProviderAccount,
        on_delete=models.CASCADE,
        verbose_name=_("Provider Account"),
        related_name='cached_rates'
    )

    base_currency = models.CharField(
        max_length=3,
        verbose_name=_("Base Currency"),
        help_text=_("Base currency code (e.g., 'USD')")
    )

    target_currency = models.CharField(
        max_length=3,
        verbose_name=_("Target Currency"),
        help_text=_("Target currency code (e.g., 'EUR')")
    )

    rate = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        verbose_name=_("Exchange Rate"),
        help_text=_("Exchange rate from base to target (e.g., 0.85 means 1 USD = 0.85 EUR)")
    )

    fetched_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Fetched At"),
        help_text=_("When this rate was last fetched from provider")
    )

    class Meta:
        verbose_name = _("Exchange Rate")
        verbose_name_plural = _("Exchange Rates")
        unique_together = [['provider_account', 'base_currency', 'target_currency']]
        indexes = [
            models.Index(fields=['base_currency', 'target_currency']),
            models.Index(fields=['fetched_at']),
        ]

    def __str__(self):
        return f"{self.base_currency}/{self.target_currency}: {self.rate}"

    @property
    def is_stale(self):
        """Check if rate is older than 24 hours"""
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() - self.fetched_at > timedelta(hours=24)


class ExchangeRateHistory(models.Model):
    """
    Historical exchange rates for order auditing.
    Stores the rate used at time of order placement.
    """
    base_currency = models.CharField(
        max_length=3,
        verbose_name=_("Base Currency")
    )

    target_currency = models.CharField(
        max_length=3,
        verbose_name=_("Target Currency")
    )

    rate = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        verbose_name=_("Exchange Rate")
    )

    provider_name = models.CharField(
        max_length=255,
        verbose_name=_("Provider Name"),
        help_text=_("Name of exchange rate provider used")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("When this rate snapshot was created")
    )

    # Optional: Link to specific order
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='exchange_rate_snapshots',
        verbose_name=_("Order")
    )

    class Meta:
        verbose_name = _("Exchange Rate History")
        verbose_name_plural = _("Exchange Rate History")
        indexes = [
            models.Index(fields=['base_currency', 'target_currency', 'created_at']),
            models.Index(fields=['order']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.base_currency}/{self.target_currency}: {self.rate} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class ManualExchangeRate(models.Model):
    """
    Merchant-defined exchange rates for manual currency conversion.
    Takes precedence over provider-fetched rates when active.
    """
    site = models.ForeignKey(
        'sites.Site',
        on_delete=models.CASCADE,
        verbose_name=_("Site"),
        help_text=_("Site this manual rate belongs to")
    )

    base_currency = models.CharField(
        max_length=3,
        verbose_name=_("Base Currency"),
        help_text=_("Base currency code (e.g., 'USD')")
    )

    target_currency = models.CharField(
        max_length=3,
        verbose_name=_("Target Currency"),
        help_text=_("Target currency code (e.g., 'EUR')")
    )

    rate = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        verbose_name=_("Exchange Rate"),
        help_text=_("Exchange rate from base to target (e.g., 0.85 means 1 base = 0.85 target)")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this manual rate is active and should be used for conversions")
    )

    exclude_from_auto_sync = models.BooleanField(
        default=False,
        verbose_name=_("Locked (Exclude from Auto-Sync)"),
        help_text=_("When enabled, this rate will not be overwritten by provider sync operations. "
                    "Use for rates you manage manually.")
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Optional notes about this rate (e.g., 'Fixed rate for wholesale customers')")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Manual Exchange Rate")
        verbose_name_plural = _("Manual Exchange Rates")
        unique_together = [['site', 'base_currency', 'target_currency']]
        ordering = ['base_currency', 'target_currency']
        indexes = [
            models.Index(fields=['base_currency', 'target_currency']),
            models.Index(fields=['is_active']),
            models.Index(fields=['site', 'is_active']),
        ]

    def __str__(self):
        status = _("Active") if self.is_active else _("Inactive")
        return f"{self.base_currency}/{self.target_currency}: {self.rate} ({status})"

    def clean(self):
        super().clean()
        if self.base_currency and self.target_currency:
            if self.base_currency == self.target_currency:
                raise ValidationError({
                    'target_currency': _("Base and target currencies must be different.")
                })
        if self.rate is not None and self.rate <= 0:
            raise ValidationError({
                'rate': _("Exchange rate must be greater than zero.")
            })
