"""
Payout Provider Models

Stores merchant's payout provider accounts (Airwallex, PayPal) with
encrypted credentials and configuration.
"""

import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from payment_providers.utils.encryption import encrypt_credentials, decrypt_credentials

logger = logging.getLogger(__name__)


class PayoutProviderAccount(models.Model):
    """
    Stores a merchant's payout provider account configuration.

    Each merchant can have multiple provider accounts (e.g., both PayPal
    and Airwallex) and designate one as default.
    """

    PROVIDER_CHOICES = [
        ('paypal', _('PayPal')),
        ('airwallex', _('Airwallex')),
        ('wise', _('Wise')),
    ]

    CONNECTION_STATUS_CHOICES = [
        ('untested', _('Untested')),
        ('connected', _('Connected')),
        ('failed', _('Connection Failed')),
        ('invalid_credentials', _('Invalid Credentials')),
    ]

    # Provider identification
    provider_type = models.CharField(
        _('Provider Type'),
        max_length=50,
        choices=PROVIDER_CHOICES,
        help_text=_('The payout provider service')
    )

    # Optional link to component registry for installed provider packages
    component = models.ForeignKey(
        'component_updates.ComponentRegistry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payout_provider_accounts',
        help_text=_('Installed provider component from the component registry')
    )

    # Display name for this account
    name = models.CharField(
        _('Account Name'),
        max_length=100,
        help_text=_('A friendly name for this account (e.g., "Primary PayPal")')
    )

    # Encrypted credentials storage (uses same format as payment_providers)
    credentials_encrypted = models.JSONField(
        _('Credentials'),
        default=dict,
        blank=True,
        help_text=_('Encrypted API credentials (never stored in plain text)')
    )

    # Provider-specific settings (non-sensitive)
    settings = models.JSONField(
        _('Settings'),
        default=dict,
        blank=True,
        help_text=_('Provider-specific configuration settings')
    )

    # Supported payout methods for this account
    supported_methods = models.JSONField(
        _('Supported Methods'),
        default=list,
        blank=True,
        help_text=_('List of payout methods this account supports')
    )

    # Account status
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Whether this provider account is active')
    )

    is_default = models.BooleanField(
        _('Default'),
        default=False,
        help_text=_('Whether this is the default provider for its supported methods')
    )

    # Connection testing
    connection_status = models.CharField(
        _('Connection Status'),
        max_length=30,
        choices=CONNECTION_STATUS_CHOICES,
        default='untested'
    )

    last_tested_at = models.DateTimeField(
        _('Last Tested'),
        null=True,
        blank=True
    )

    last_error_message = models.TextField(
        _('Last Error'),
        blank=True,
        default='',
        help_text=_('Last connection error message')
    )

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Payout Provider Account')
        verbose_name_plural = _('Payout Provider Accounts')
        ordering = ['-is_default', '-is_active', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

    @property
    def logo_url(self):
        """Get the logo URL from the component registry if available"""
        if self.component and self.component.logo:
            return self.component.logo.get('url')
        return None

    # Credentials property with encryption/decryption
    @property
    def credentials(self) -> dict:
        """Get decrypted credentials"""
        if not self.credentials_encrypted:
            return {}
        try:
            return decrypt_credentials(self.credentials_encrypted)
        except Exception as e:
            logger.error(f"Failed to decrypt credentials for {self}: {e}")
            return {}

    @credentials.setter
    def credentials(self, value: dict):
        """Set credentials with encryption"""
        if value:
            self.credentials_encrypted = encrypt_credentials(value)
        else:
            self.credentials_encrypted = {}

    def clean(self):
        """Validate model data"""
        super().clean()

        # Ensure only one default per provider type
        if self.is_default:
            existing_default = PayoutProviderAccount.objects.filter(
                provider_type=self.provider_type,
                is_default=True
            ).exclude(pk=self.pk).first()

            if existing_default:
                raise ValidationError({
                    'is_default': _(
                        'There is already a default account for %(provider)s: %(name)s'
                    ) % {'provider': self.get_provider_type_display(), 'name': existing_default.name}
                })

    def save(self, *args, **kwargs):
        # Auto-set as default if it's the first active account for this provider
        if self.is_active and not self.pk:
            existing = PayoutProviderAccount.objects.filter(
                provider_type=self.provider_type,
                is_active=True
            ).exists()
            if not existing:
                self.is_default = True

        super().save(*args, **kwargs)

    def get_provider_instance(self):
        """
        Get an instance of the provider class.

        Returns:
            BasePayoutProvider instance or None if provider not available
        """
        from .loader import get_provider_class

        provider_class = get_provider_class(self.provider_type, self.component)
        if provider_class:
            return provider_class(self.credentials)
        return None

    def test_connection(self) -> dict:
        """
        Test the connection to the provider.

        Returns:
            Dict with 'success', 'message', and optionally 'details'
        """
        from django.utils import timezone

        provider = self.get_provider_instance()
        if not provider:
            self.connection_status = 'failed'
            self.last_error_message = 'Provider class not found'
            self.last_tested_at = timezone.now()
            self.save(update_fields=['connection_status', 'last_error_message', 'last_tested_at'])
            return {'success': False, 'message': self.last_error_message}

        try:
            result = provider.test_connection()
            if result.get('success'):
                self.connection_status = 'connected'
                self.last_error_message = ''
            else:
                self.connection_status = 'failed'
                self.last_error_message = result.get('message', 'Connection failed')

            self.last_tested_at = timezone.now()
            self.save(update_fields=['connection_status', 'last_error_message', 'last_tested_at'])
            return result

        except Exception as e:
            self.connection_status = 'failed'
            self.last_error_message = str(e)
            self.last_tested_at = timezone.now()
            self.save(update_fields=['connection_status', 'last_error_message', 'last_tested_at'])
            return {'success': False, 'message': str(e)}


class PayoutWebhookLog(models.Model):
    """
    Logs incoming webhooks from payout providers for debugging and audit.
    """

    provider_account = models.ForeignKey(
        PayoutProviderAccount,
        on_delete=models.CASCADE,
        related_name='webhook_logs',
        null=True,
        blank=True
    )

    provider_type = models.CharField(
        _('Provider Type'),
        max_length=50,
        help_text=_('Provider that sent the webhook')
    )

    event_type = models.CharField(
        _('Event Type'),
        max_length=100,
        help_text=_('Type of webhook event')
    )

    event_id = models.CharField(
        _('Event ID'),
        max_length=255,
        blank=True,
        default='',
        help_text=_('Provider\'s unique event identifier')
    )

    payload = models.JSONField(
        _('Payload'),
        default=dict,
        help_text=_('Full webhook payload')
    )

    headers = models.JSONField(
        _('Headers'),
        default=dict,
        help_text=_('Request headers')
    )

    signature_valid = models.BooleanField(
        _('Signature Valid'),
        null=True,
        help_text=_('Whether signature verification passed')
    )

    processed = models.BooleanField(
        _('Processed'),
        default=False,
        help_text=_('Whether the webhook was successfully processed')
    )

    processing_error = models.TextField(
        _('Processing Error'),
        blank=True,
        default='',
        help_text=_('Error message if processing failed')
    )

    # Related payout (if identifiable from webhook)
    payout_reference = models.CharField(
        _('Payout Reference'),
        max_length=255,
        blank=True,
        default='',
        db_index=True
    )

    received_at = models.DateTimeField(_('Received'), auto_now_add=True)
    processed_at = models.DateTimeField(_('Processed At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Payout Webhook Log')
        verbose_name_plural = _('Payout Webhook Logs')
        ordering = ['-received_at']
        indexes = [
            models.Index(fields=['provider_type', 'event_type']),
            models.Index(fields=['event_id']),
        ]

    def __str__(self):
        return f"{self.provider_type}: {self.event_type} ({self.received_at})"
