"""
SMS System Models.

Provides SMS/WhatsApp provider accounts, message templates, and delivery tracking.
"""

from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_provider_choices():
    """
    Get provider choices dynamically from the registry.

    Returns a list of tuples for use in model choices.
    Falls back to empty list if registry is not available.
    """
    try:
        from sms_system.providers.registry import SMSProviderRegistry

        providers = SMSProviderRegistry.list_providers()
        return [(p["key"], p["name"]) for p in providers]
    except Exception:
        # Fallback during migrations or if registry not ready
        return []


class SMSProviderAccount(models.Model):
    """
    SMS/WhatsApp provider account configuration.

    Stores credentials for SMS providers like Twilio, AWS SNS, MessageBird, etc.
    Providers are discovered dynamically from component packages.
    """

    CONNECTION_STATUS_CHOICES = [
        ("untested", _("Untested")),
        ("success", _("Connected")),
        ("failed", _("Connection Failed")),
    ]

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="sms_accounts",
        default=1,
    )
    provider_key = models.CharField(
        max_length=50,
        verbose_name=_("Provider"),
        help_text=_("SMS/messaging service provider"),
    )
    component = models.ForeignKey(
        "component_updates.ComponentRegistry",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sms_accounts",
        limit_choices_to={"component_type": "sms_provider"},
        verbose_name=_("Provider Component"),
        help_text=_("Reference to installed provider component"),
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name=_("Display Name"),
        help_text=_("Friendly name for this account"),
    )
    credentials = models.BinaryField(
        verbose_name=_("Encrypted Credentials"),
        help_text=_("Encrypted API credentials for this provider"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )
    is_default_sms = models.BooleanField(
        default=False,
        verbose_name=_("Default SMS Account"),
        help_text=_("Use this account for sending SMS by default"),
    )
    is_default_whatsapp = models.BooleanField(
        default=False,
        verbose_name=_("Default WhatsApp Account"),
        help_text=_("Use this account for sending WhatsApp messages by default"),
    )
    connection_status = models.CharField(
        max_length=20,
        choices=CONNECTION_STATUS_CHOICES,
        default="untested",
        verbose_name=_("Connection Status"),
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Checked"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("SMS Provider Account")
        verbose_name_plural = _("SMS Provider Accounts")
        ordering = ["-is_default_sms", "-is_default_whatsapp", "display_name"]

    def __str__(self):
        return f"{self.display_name} ({self.provider_display_name})"

    @property
    def provider_display_name(self):
        """Get the display name for the provider."""
        try:
            from sms_system.providers.registry import SMSProviderRegistry

            info = SMSProviderRegistry.get_provider_info(self.provider_key)
            if info:
                return info.get("name", self.provider_key)
        except Exception:
            pass
        return self.provider_key

    def save(self, *args, **kwargs):
        # Ensure only one default per type
        if self.is_default_sms:
            SMSProviderAccount.objects.filter(
                site=self.site,
                is_default_sms=True,
            ).exclude(pk=self.pk).update(is_default_sms=False)

        if self.is_default_whatsapp:
            SMSProviderAccount.objects.filter(
                site=self.site,
                is_default_whatsapp=True,
            ).exclude(pk=self.pk).update(is_default_whatsapp=False)

        super().save(*args, **kwargs)

    def get_credentials(self):
        """Get decrypted credentials as dict."""
        from email_system.utils.encryption import decrypt_credentials

        if not self.credentials:
            return {}

        return decrypt_credentials(self.credentials)

    def set_credentials(self, credentials_dict):
        """Set credentials from dict (will be encrypted on save)."""
        from email_system.utils.encryption import encrypt_credentials

        self.credentials = encrypt_credentials(credentials_dict)

    def get_provider_instance(self):
        """
        Get an instance of the provider with credentials.

        Returns:
            Provider instance or None if provider not found
        """
        from sms_system.providers.registry import SMSProviderRegistry

        try:
            return SMSProviderRegistry.create_provider_instance(
                self.provider_key,
                self.get_credentials(),
            )
        except ValueError:
            return None

    def test_connection(self):
        """
        Test the connection to this provider.

        Returns:
            Dict with 'success' boolean and status details
        """
        provider = self.get_provider_instance()
        if not provider:
            return {
                "success": False,
                "error": f"Provider {self.provider_key} not found",
            }

        if hasattr(provider, "test_connection"):
            result = provider.test_connection()
            # Update connection status
            self.connection_status = "success" if result.get("success") else "failed"
            self.last_checked = timezone.now()
            self.save(update_fields=["connection_status", "last_checked"])
            return result

        return {
            "success": True,
            "message": "Provider does not support connection testing",
        }

    @classmethod
    def get_default_sms_account(cls):
        """Get the default SMS account for the current site."""
        return cls.objects.filter(
            site_id=1,
            is_active=True,
            is_default_sms=True,
        ).first()

    @classmethod
    def get_default_whatsapp_account(cls):
        """Get the default WhatsApp account for the current site."""
        return cls.objects.filter(
            site_id=1,
            is_active=True,
            is_default_whatsapp=True,
        ).first()


class SMSTemplate(models.Model):
    """
    Short message templates with variable substitution.

    Used for sending templated SMS messages like receipts, notifications, etc.
    """

    TEMPLATE_TYPE_CHOICES = [
        ("pos_receipt", _("POS Receipt")),
        ("order_confirmation", _("Order Confirmation")),
        ("shipping_update", _("Shipping Update")),
        ("delivery_notification", _("Delivery Notification")),
        ("password_reset", _("Password Reset")),
        ("verification_code", _("Verification Code")),
        ("marketing", _("Marketing")),
        ("custom", _("Custom")),
    ]

    template_type = models.CharField(
        max_length=50,
        choices=TEMPLATE_TYPE_CHOICES,
        unique=True,
        verbose_name=_("Template Type"),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
    )
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("Message template. Use {variable} syntax for placeholders."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("SMS Template")
        verbose_name_plural = _("SMS Templates")
        ordering = ["template_type"]

    def __str__(self):
        return f"{self.name} ({self.template_type})"

    def render(self, context: dict) -> str:
        """Render template with context variables."""
        message = self.message
        for key, value in context.items():
            message = message.replace(f"{{{key}}}", str(value))
        return message


class SMSOutbox(models.Model):
    """
    SMS message queue and delivery tracking.

    Records all sent and pending SMS messages with status tracking.
    """

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("queued", _("Queued")),
        ("sent", _("Sent")),
        ("delivered", _("Delivered")),
        ("failed", _("Failed")),
        ("skipped", _("Skipped")),
        ("sandbox_logged", _("Sandbox Logged")),
    ]

    MESSAGE_TYPE_CHOICES = [
        ("sms", _("SMS")),
        ("whatsapp", _("WhatsApp")),
    ]

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="sms_outbox",
        default=1,
    )
    account = models.ForeignKey(
        SMSProviderAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        verbose_name=_("Provider Account"),
    )
    template = models.ForeignKey(
        SMSTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        verbose_name=_("Template"),
    )
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPE_CHOICES,
        default="sms",
        verbose_name=_("Message Type"),
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number"),
        help_text=_("Recipient phone number in E.164 format"),
    )
    message = models.TextField(
        verbose_name=_("Message"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )
    provider_message_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Provider Message ID"),
        help_text=_("Message ID from the SMS provider"),
    )
    error_message = models.TextField(
        blank=True,
        verbose_name=_("Error Message"),
    )
    skip_reason = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Skip Reason"),
        help_text=_("Reason why SMS was skipped (e.g., user_preference_disabled, unsubscribed)"),
    )
    retry_count = models.IntegerField(
        default=0,
        verbose_name=_("Retry Count"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    queued_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Queued At"),
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Sent At"),
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Delivered At"),
    )

    class Meta:
        verbose_name = _("SMS Outbox")
        verbose_name_plural = _("SMS Outbox")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["provider_message_id"]),
        ]

    def __str__(self):
        return f"{self.message_type.upper()} to {self.phone} ({self.status})"

    def mark_queued(self):
        """Mark message as queued for sending."""
        self.status = "queued"
        self.queued_at = timezone.now()
        self.save(update_fields=["status", "queued_at"])

    def mark_sent(self, provider_message_id=""):
        """Mark message as sent."""
        self.status = "sent"
        self.sent_at = timezone.now()
        self.provider_message_id = provider_message_id
        self.save(update_fields=["status", "sent_at", "provider_message_id"])

    def mark_delivered(self):
        """Mark message as delivered."""
        self.status = "delivered"
        self.delivered_at = timezone.now()
        self.save(update_fields=["status", "delivered_at"])

    def mark_failed(self, error_message):
        """Mark message as failed."""
        self.status = "failed"
        self.error_message = error_message
        self.retry_count += 1
        self.save(update_fields=["status", "error_message", "retry_count"])
