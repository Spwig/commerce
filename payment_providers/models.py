import json
from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from djmoney.models.fields import MoneyField
import uuid

User = get_user_model()


class PaymentProviderAccount(models.Model):
    """
    Payment provider connections (Stripe, PayPal, AirWallex, etc.)
    Stores encrypted credentials and configuration.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to ComponentRegistry (payment_provider type)
    component = models.ForeignKey(
        'component_updates.ComponentRegistry',
        on_delete=models.CASCADE,
        limit_choices_to={'component_type': 'payment_provider'},
        related_name='payment_provider_accounts',
        verbose_name=_('component'),
        help_text=_('Installed payment provider component')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_providers',
        verbose_name=_('user'),
        help_text=_('User who owns this provider account')
    )

    display_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_('display name'),
        help_text=_('Friendly name for this connection (e.g., "My Payment Provider")')
    )

    # Encrypted credentials (API keys, secrets, tokens)
    credentials_encrypted = models.JSONField(
        default=dict,
        verbose_name=_('credentials'),
        help_text=_('Encrypted API credentials (never stored in plain text)')
    )

    # Provider-specific settings and capabilities
    settings = models.JSONField(
        default=dict,
        verbose_name=_('settings'),
        help_text=_('Provider-specific configuration (checkout mode, features, etc.)')
    )

    # Signup affiliate link (optional)
    signup_url = models.URLField(
        blank=True,
        verbose_name=_('signup URL'),
        help_text=_('Link for merchants to create provider account (may be affiliate link)')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active'),
        help_text=_('Whether this provider connection is active for checkout')
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_('is default'),
        help_text=_('Use this provider as default for payment processing')
    )

    # Checkout mode (hosted or integrated)
    checkout_mode = models.CharField(
        max_length=20,
        choices=[
            ('hosted', _('Hosted - Redirect to provider')),
            ('integrated', _('Integrated - On-site checkout')),
        ],
        default='hosted',
        verbose_name=_('checkout mode'),
        help_text=_('How customers will complete payment')
    )

    # Display settings
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('sort order'),
        help_text=_('Display order in checkout (lower numbers appear first)')
    )

    # Connection health
    last_tested_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last tested at'),
        help_text=_('Last successful connection test')
    )

    connection_status = models.CharField(
        max_length=20,
        choices=[
            ('unknown', _('Unknown')),
            ('connected', _('Connected')),
            ('error', _('Connection Error')),
        ],
        default='unknown',
        verbose_name=_('connection status')
    )

    connection_error = models.TextField(
        blank=True,
        verbose_name=_('connection error'),
        help_text=_('Last connection error message')
    )

    # Payment method sync tracking
    available_payment_methods = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('available payment methods'),
        help_text=_(
            'Payment methods available from provider API, organized by country. '
            'Use "_global" key for methods available regardless of country. '
            'Format: {"_global": ["card", "apple_pay"], "SG": ["card", "paynow"]}'
        )
    )

    enabled_payment_methods = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('enabled payment methods'),
        help_text=_(
            'Payment methods enabled by merchant. Use "_global" for all countries, '
            'or per-country keys to override. '
            'Format: {"_global": ["card", "apple_pay"], "SG": ["card"]}'
        )
    )

    last_method_sync_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last method sync at'),
        help_text=_('When payment methods were last synced from provider')
    )

    method_sync_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending - Not synced yet')),
            ('syncing', _('Syncing - In progress')),
            ('success', _('Success - Synced successfully')),
            ('error', _('Error - Sync failed')),
        ],
        default='pending',
        verbose_name=_('method sync status'),
        help_text=_('Status of payment method synchronization')
    )

    method_sync_error = models.TextField(
        blank=True,
        verbose_name=_('method sync error'),
        help_text=_('Last payment method sync error message')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ['-is_default', 'sort_order', '-created_at']
        verbose_name = _('payment provider account')
        verbose_name_plural = _('payment provider accounts')
        indexes = [
            models.Index(fields=['user', 'is_active'], name='pp_acct_user_active_idx'),
            models.Index(fields=['is_default'], name='pp_acct_default_idx'),
            models.Index(fields=['sort_order'], name='pp_acct_sort_idx'),
        ]

    def __str__(self):
        name = self.display_name or self.component.name
        return f"{name} ({self.user.username})"

    def save(self, *args, **kwargs):
        # Ensure only one default provider per user
        if self.is_default:
            PaymentProviderAccount.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    @property
    def test_mode(self):
        """
        Check if provider is in test/sandbox mode from stored credentials.

        Supports both NEW dual-credential structure (test_mode boolean)
        and LEGACY single-credential structure (environment string).
        Defaults to True for safety.
        """
        creds = self.credentials_encrypted or {}

        # NEW: Check test_mode boolean first
        test_mode_flag = creds.get('test_mode')
        if test_mode_flag is not None:
            return bool(test_mode_flag)

        # LEGACY: Fall back to environment-based detection
        env = creds.get('environment', '')
        if isinstance(env, str) and env:
            # Include 'demo' for Airwallex and other providers
            return env.lower() in ('test', 'sandbox', 'development', 'dev', 'demo')

        # Default to test mode for safety
        return True

    def get_provider_instance(self):
        """
        Get instantiated provider class with decrypted credentials.

        Returns:
            Provider instance ready for API calls

        Raises:
            ValueError: If provider cannot be loaded or credentials invalid
            SandboxPaymentError: If live credentials detected in sandbox mode
        """
        from payment_providers.providers.registry import ProviderRegistry
        from payment_providers.utils.encryption import decrypt_credentials
        from core.sandbox.payment_guard import validate_provider_credentials

        # Get provider class from registry
        provider_class = ProviderRegistry.get_provider(self.component.slug)
        if not provider_class:
            raise ValueError(f"Provider '{self.component.slug}' not found in registry")

        # Decrypt credentials
        credentials = decrypt_credentials(self.credentials_encrypted)

        # Sandbox guard: reject live credentials in sandbox mode
        validate_provider_credentials(self.component.slug, credentials)

        # Instantiate provider with credentials and settings
        return provider_class(credentials=credentials, config=self.settings)

    def test_connection(self) -> dict:
        """
        Test connection to payment provider.

        Returns:
            Dictionary with test results:
            {
                'success': True/False,
                'message': '...',
                'details': {...}
            }

        Updates connection_status, connection_error, and last_tested_at fields.
        """
        try:
            provider = self.get_provider_instance()
            result = provider.test_connection()

            if result.get('success'):
                self.connection_status = 'connected'
                self.connection_error = ''
                self.last_tested_at = timezone.now()
            else:
                self.connection_status = 'error'
                self.connection_error = result.get('message', 'Unknown error')

            self.save(update_fields=['connection_status', 'connection_error', 'last_tested_at'])
            return result

        except Exception as e:
            self.connection_status = 'error'
            self.connection_error = str(e)
            self.save(update_fields=['connection_status', 'connection_error'])

            return {
                'success': False,
                'message': f'Connection test failed: {str(e)}',
                'details': {}
            }

    def sync_payment_methods(self) -> dict:
        """
        Sync available payment methods from provider API.

        Returns:
            Dictionary with sync results:
            {
                'success': True/False,
                'message': '...',
                'methods': {...}  # Country-to-methods mapping
            }

        Updates available_payment_methods, method_sync_status, method_sync_error,
        and last_method_sync_at fields.
        """
        try:
            # Update status to syncing
            self.method_sync_status = 'syncing'
            self.save(update_fields=['method_sync_status'])

            # Get provider instance
            provider = self.get_provider_instance()

            # Check if provider supports payment method sync
            if not hasattr(provider, 'get_payment_method_types'):
                return {
                    'success': False,
                    'message': _('Provider does not support payment method synchronization'),
                    'methods': {}
                }

            # Fetch payment methods from provider
            result = provider.get_payment_method_types()

            if result.get('success'):
                # Store available methods
                self.available_payment_methods = result.get('methods', {})

                # Auto-enable all synced methods if none are configured yet
                if not self.enabled_payment_methods:
                    self.enabled_payment_methods = result.get('methods', {}).copy()

                # Update sync status
                self.method_sync_status = 'success'
                self.method_sync_error = ''
                self.last_method_sync_at = timezone.now()

                self.save(update_fields=[
                    'available_payment_methods',
                    'enabled_payment_methods',
                    'method_sync_status',
                    'method_sync_error',
                    'last_method_sync_at'
                ])

                return {
                    'success': True,
                    'message': _('Payment methods synced successfully'),
                    'methods': self.available_payment_methods
                }
            else:
                # Sync failed
                self.method_sync_status = 'error'
                self.method_sync_error = result.get('message', 'Unknown error')
                self.save(update_fields=['method_sync_status', 'method_sync_error'])

                return {
                    'success': False,
                    'message': result.get('message', 'Sync failed'),
                    'methods': {}
                }

        except Exception as e:
            self.method_sync_status = 'error'
            self.method_sync_error = str(e)
            self.save(update_fields=['method_sync_status', 'method_sync_error'])

            return {
                'success': False,
                'message': f'Sync failed: {str(e)}',
                'methods': {}
            }

    GLOBAL_KEY = '_global'

    def get_available_methods_for_country(self, country_code: str) -> list:
        """
        Get available payment methods for a specific country.
        Falls back to _global if no country-specific entry exists.

        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'SG')
                          or '_global' for global methods

        Returns:
            List of available payment method slugs
        """
        if country_code == self.GLOBAL_KEY:
            return self.available_payment_methods.get(self.GLOBAL_KEY, [])
        country_methods = self.available_payment_methods.get(country_code.upper(), [])
        if country_methods:
            return country_methods
        return self.available_payment_methods.get(self.GLOBAL_KEY, [])

    def get_enabled_methods_for_country(self, country_code: str) -> list:
        """
        Get enabled payment methods for a specific country.
        Country-specific config takes priority; falls back to _global.

        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'SG')
                          or '_global' for global methods

        Returns:
            List of enabled payment method slugs
        """
        if country_code == self.GLOBAL_KEY:
            return self.enabled_payment_methods.get(self.GLOBAL_KEY, [])
        country_methods = self.enabled_payment_methods.get(country_code.upper(), [])
        if country_methods:
            return country_methods
        return self.enabled_payment_methods.get(self.GLOBAL_KEY, [])

    def is_method_available(self, country_code: str, method_slug: str) -> bool:
        """
        Check if a payment method is available from the provider for a country.

        Args:
            country_code: ISO 3166-1 alpha-2 country code
            method_slug: Payment method identifier (e.g., 'card', 'apple_pay')

        Returns:
            True if method is available, False otherwise
        """
        available_methods = self.get_available_methods_for_country(country_code)
        return method_slug in available_methods

    def is_method_enabled(self, country_code: str, method_slug: str) -> bool:
        """
        Check if a payment method is enabled by merchant for a country.

        Args:
            country_code: ISO 3166-1 alpha-2 country code
            method_slug: Payment method identifier

        Returns:
            True if method is enabled, False otherwise
        """
        enabled_methods = self.get_enabled_methods_for_country(country_code)
        return method_slug in enabled_methods

    def enable_payment_method(self, country_code: str, method_slug: str) -> bool:
        """
        Enable a payment method for a country or globally (_global).

        Args:
            country_code: ISO 3166-1 alpha-2 country code or '_global'
            method_slug: Payment method identifier

        Returns:
            True if enabled successfully

        Raises:
            ValueError: If method is not available from provider
        """
        key = self.GLOBAL_KEY if country_code == self.GLOBAL_KEY else country_code.upper()

        # Check if method is available from provider
        if not self.is_method_available(key, method_slug):
            raise ValueError(
                f"Payment method '{method_slug}' is not available for {key} "
                f"from provider. Please sync payment methods first."
            )

        enabled_methods = self.enabled_payment_methods.get(key, [])
        if method_slug not in enabled_methods:
            enabled_methods.append(method_slug)
            self.enabled_payment_methods[key] = enabled_methods
            self.save(update_fields=['enabled_payment_methods', 'updated_at'])

        return True

    def disable_payment_method(self, country_code: str, method_slug: str) -> bool:
        """
        Disable a payment method for a country or globally (_global).

        Args:
            country_code: ISO 3166-1 alpha-2 country code or '_global'
            method_slug: Payment method identifier

        Returns:
            True if disabled successfully, False if not found
        """
        key = self.GLOBAL_KEY if country_code == self.GLOBAL_KEY else country_code.upper()

        enabled_methods = self.enabled_payment_methods.get(key, [])
        if method_slug in enabled_methods:
            enabled_methods.remove(method_slug)
            self.enabled_payment_methods[key] = enabled_methods
            self.save(update_fields=['enabled_payment_methods', 'updated_at'])
            return True

        return False

    def get_all_enabled_countries(self) -> list:
        """
        Get list of all countries with enabled payment methods.
        Excludes the '_global' key.

        Returns:
            List of ISO 3166-1 alpha-2 country codes
        """
        return [k for k in self.enabled_payment_methods.keys() if k != self.GLOBAL_KEY]

    def has_global_config(self) -> bool:
        """Whether a global payment method configuration exists."""
        return self.GLOBAL_KEY in self.enabled_payment_methods


class PaymentTransaction(models.Model):
    """
    Payment transactions processed through providers.
    Tracks charges, authorizations, captures, voids, and refunds.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('authorized', _('Authorized - Not captured')),
        ('completed', _('Completed - Payment successful')),
        ('failed', _('Failed')),
        ('voided', _('Voided - Authorization canceled')),
        ('refunded', _('Refunded - Full refund')),
        ('partially_refunded', _('Partially Refunded')),
    ]

    TYPE_CHOICES = [
        ('charge', _('Charge - Immediate payment')),
        ('authorize', _('Authorize - Hold funds')),
        ('capture', _('Capture - Collect authorized funds')),
        ('void', _('Void - Cancel authorization')),
        ('refund', _('Refund - Return payment')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to provider account
    provider_account = models.ForeignKey(
        PaymentProviderAccount,
        on_delete=models.PROTECT,
        null=True,  # Nullable during migration period
        blank=True,
        related_name='transactions',
        verbose_name=_('provider account'),
        help_text=_('Payment provider account used for this transaction')
    )

    # Link to order (optional - may be set after transaction)
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment_transactions',
        verbose_name=_('order')
    )

    # Transaction identifiers
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('transaction ID'),
        help_text=_('Internal transaction ID')
    )

    provider_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name=_('provider transaction ID'),
        help_text=_('Provider transaction ID (charge ID, payment intent ID, etc.)')
    )

    # For authorizations that can be captured
    authorization_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name=_('authorization ID'),
        help_text=_('Provider authorization ID (if applicable)')
    )

    # Transaction details
    amount = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_('amount'),
        help_text=_('Transaction amount')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('status')
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='charge',
        verbose_name=_('type')
    )

    # Customer information
    customer_email = models.EmailField(
        blank=True,
        verbose_name=_('customer email')
    )

    customer_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('customer name')
    )

    # Payment method information
    payment_method_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('payment method type'),
        help_text=_('Type of payment method used (credit_card, bank_transfer, etc.)')
    )

    payment_method_last4 = models.CharField(
        max_length=4,
        blank=True,
        verbose_name=_('last 4 digits'),
        help_text=_('Last 4 digits of card/account')
    )

    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('metadata'),
        help_text=_('Additional transaction metadata')
    )

    # Provider response data
    provider_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('provider response'),
        help_text=_('Raw response from payment provider')
    )

    # Error information
    error_message = models.TextField(
        blank=True,
        verbose_name=_('error message')
    )

    error_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('error code')
    )

    # Authorization expiry (for authorize transactions)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('expires at'),
        help_text=_('When authorization expires (if applicable)')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('completed at')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('payment transaction')
        verbose_name_plural = _('payment transactions')
        indexes = [
            models.Index(fields=['-created_at'], name='pp_txn_created_idx'),
            models.Index(fields=['provider_account', 'status'], name='pp_txn_prov_status_idx'),
            models.Index(fields=['order', 'status'], name='pp_txn_order_status_idx'),
            models.Index(fields=['status', 'transaction_type'], name='pp_txn_status_type_idx'),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.provider_account.component.name} - {self.amount}"

    def is_successful(self):
        """Check if transaction was successful"""
        return self.status in ['completed', 'authorized']

    def can_be_captured(self):
        """Check if transaction can be captured"""
        return (
            self.transaction_type == 'authorize' and
            self.status == 'authorized' and
            (not self.expires_at or self.expires_at > timezone.now())
        )

    def can_be_voided(self):
        """Check if transaction can be voided"""
        return (
            self.transaction_type == 'authorize' and
            self.status == 'authorized' and
            (not self.expires_at or self.expires_at > timezone.now())
        )

    def can_be_refunded(self):
        """Check if transaction can be refunded"""
        return (
            self.status in ['completed'] and
            self.transaction_type in ['charge', 'capture']
        )


class PaymentWebhook(models.Model):
    """
    Webhook events from payment providers.
    Tracks all webhook deliveries for audit and debugging.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to provider account
    provider_account = models.ForeignKey(
        PaymentProviderAccount,
        on_delete=models.CASCADE,
        null=True,  # Allow null initially for webhook routing
        blank=True,
        related_name='webhooks',
        verbose_name=_('provider account')
    )

    # Provider slug for webhook routing
    provider_slug = models.CharField(
        max_length=100,
        default='',
        blank=True,
        db_index=True,
        verbose_name=_('provider slug'),
        help_text=_('Provider identifier for routing')
    )

    # Webhook identifiers
    event_id = models.CharField(
        max_length=255,
        default='',
        blank=True,
        db_index=True,
        verbose_name=_('event ID'),
        help_text=_('Provider webhook event ID')
    )

    event_type = models.CharField(
        max_length=100,
        default='',
        blank=True,
        db_index=True,
        verbose_name=_('event type'),
        help_text=_('Type of webhook event')
    )

    # Webhook payload
    payload = models.JSONField(
        verbose_name=_('payload'),
        help_text=_('Complete webhook payload')
    )

    headers = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('headers'),
        help_text=_('HTTP headers from webhook request')
    )

    # Processing status
    processed = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_('processed'),
        help_text=_('Whether webhook has been processed')
    )

    processing_result = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('processing result'),
        help_text=_('Result from webhook handler')
    )

    processing_error = models.TextField(
        blank=True,
        verbose_name=_('processing error'),
        help_text=_('Error message if processing failed')
    )

    # Signature verification
    signature_verified = models.BooleanField(
        default=False,
        verbose_name=_('signature verified'),
        help_text=_('Whether webhook signature was verified')
    )

    # Idempotency - prevent duplicate processing
    idempotency_key = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name=_('idempotency key'),
        help_text=_('Key to prevent duplicate processing')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('received at'))
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('processed at')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('payment webhook')
        verbose_name_plural = _('payment webhooks')
        indexes = [
            models.Index(fields=['-created_at'], name='pp_wh_created_idx'),
            models.Index(fields=['provider_slug', 'event_type'], name='pp_wh_prov_event_idx'),
            models.Index(fields=['processed', 'created_at'], name='pp_wh_processed_idx'),
            models.Index(fields=['event_id', 'provider_slug'], name='pp_wh_event_idx'),
        ]
        # Prevent duplicate event processing
        unique_together = [['provider_slug', 'event_id']]

    def __str__(self):
        return f"{self.provider_slug} - {self.event_type} ({self.event_id})"

    def mark_processed(self, result: dict = None, error: str = None):
        """
        Mark webhook as processed.

        Args:
            result: Processing result dictionary
            error: Error message if processing failed
        """
        self.processed = True
        self.processed_at = timezone.now()
        if result:
            self.processing_result = result
        if error:
            self.processing_error = error
        self.save(update_fields=['processed', 'processed_at', 'processing_result', 'processing_error'])


class PaymentIntent(models.Model):
    """
    Tracks payment lifecycle for checkout.
    Links to Order which is created first with payment_status='unpaid'.

    Flow:
    1. create_payment_intent() → Creates Order (unpaid) + PaymentIntent
    2. Customer pays via provider (hosted/embedded)
    3. handle_payment_success() → Updates Order to 'paid'
    """
    STATUS_CHOICES = [
        ('created', _('Created')),
        ('requires_payment_method', _('Requires Payment Method')),
        ('requires_confirmation', _('Requires Confirmation')),
        ('requires_action', _('Requires Action')),  # 3DS
        ('processing', _('Processing')),
        ('succeeded', _('Succeeded')),
        ('canceled', _('Canceled')),
        ('failed', _('Failed')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    checkout_session = models.ForeignKey(
        'cart.CheckoutSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment_intents',
        verbose_name=_('checkout session'),
        help_text=_('Checkout session this payment intent was created for')
    )

    provider_account = models.ForeignKey(
        PaymentProviderAccount,
        on_delete=models.PROTECT,
        related_name='payment_intents',
        verbose_name=_('provider account'),
        help_text=_('Payment provider account used for this intent')
    )

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payment_intents',
        verbose_name=_('order'),
        help_text=_('Order this payment intent is for')
    )

    # Provider identifiers
    provider_intent_id = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('provider intent ID'),
        help_text=_('Provider payment intent ID (e.g., Stripe pi_xxx, AirWallex int_xxx)')
    )

    client_secret = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('client secret'),
        help_text=_('Client secret for embedded checkout (never expose in logs)')
    )

    checkout_url = models.URLField(
        max_length=2000,
        blank=True,
        verbose_name=_('checkout URL'),
        help_text=_('Hosted checkout redirect URL')
    )

    # State
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='created',
        db_index=True,
        verbose_name=_('status')
    )

    # Amount (snapshot from checkout session)
    amount = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_('amount'),
        help_text=_('Payment amount')
    )

    # 3DS/Authentication
    requires_action = models.BooleanField(
        default=False,
        verbose_name=_('requires action'),
        help_text=_('Whether customer action is required (e.g., 3DS)')
    )

    action_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('action type'),
        help_text=_('Type of action required (redirect, 3ds_challenge, etc.)')
    )

    action_url = models.URLField(
        max_length=2000,
        blank=True,
        verbose_name=_('action URL'),
        help_text=_('URL to redirect for action (3DS, verification, etc.)')
    )

    action_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('action data'),
        help_text=_('Provider-specific action data for SDK handling')
    )

    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('metadata'),
        help_text=_('Additional intent metadata')
    )

    provider_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('provider response'),
        help_text=_('Raw response from payment provider')
    )

    # Error information
    error_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('error code')
    )

    error_message = models.TextField(
        blank=True,
        verbose_name=_('error message')
    )

    # Timestamps
    expires_at = models.DateTimeField(
        verbose_name=_('expires at'),
        help_text=_('When this payment intent expires')
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('payment intent')
        verbose_name_plural = _('payment intents')
        indexes = [
            models.Index(fields=['checkout_session', 'status'], name='pp_intent_session_idx'),
            models.Index(fields=['provider_intent_id'], name='pp_intent_provider_idx'),
            models.Index(fields=['-created_at'], name='pp_intent_created_idx'),
            models.Index(fields=['order', 'status'], name='pp_intent_order_idx'),
        ]

    def __str__(self):
        return f"{self.provider_intent_id} - {self.status} ({self.amount})"

    def is_terminal(self) -> bool:
        """Check if intent is in a terminal state (succeeded, canceled, or failed)."""
        return self.status in ['succeeded', 'canceled', 'failed']

    def can_retry(self) -> bool:
        """Check if payment can be retried (failed but not expired)."""
        return (
            self.status == 'failed' and
            self.expires_at > timezone.now()
        )

    @staticmethod
    def _json_safe(data):
        """Convert provider data to JSON-safe types (Decimal → str)."""
        return json.loads(json.dumps(data, default=str))

    def mark_succeeded(self, provider_data: dict = None):
        """Mark intent as succeeded."""
        self.status = 'succeeded'
        self.requires_action = False
        if provider_data:
            self.provider_response = self._json_safe(provider_data)
        self.save(update_fields=['status', 'requires_action', 'provider_response', 'updated_at'])

    def mark_failed(self, error_code: str = '', error_message: str = '', provider_data: dict = None):
        """Mark intent as failed."""
        self.status = 'failed'
        self.error_code = error_code
        self.error_message = error_message
        if provider_data:
            self.provider_response = self._json_safe(provider_data)
        self.save(update_fields=['status', 'error_code', 'error_message', 'provider_response', 'updated_at'])

    def mark_requires_action(self, action_type: str, action_url: str = '', action_data: dict = None):
        """Mark intent as requiring customer action (3DS, etc.)."""
        self.status = 'requires_action'
        self.requires_action = True
        self.action_type = action_type
        self.action_url = action_url
        if action_data:
            self.action_data = action_data
        self.save(update_fields=[
            'status', 'requires_action', 'action_type', 'action_url', 'action_data', 'updated_at'
        ])


# Legacy model - keep for backwards compatibility during migration
