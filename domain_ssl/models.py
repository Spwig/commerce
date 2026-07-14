from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class DomainConfiguration(models.Model):
    """
    Singleton model for domain and SSL configuration.
    Tracks the current domain, SSL mode, certificate state, and task status.
    """

    class SSLMode(models.TextChoices):
        NONE = "none", _("None (HTTP only)")
        LETSENCRYPT = "letsencrypt", _("Let's Encrypt (HTTP-01)")
        LETSENCRYPT_DNS = "letsencrypt_dns", _("Let's Encrypt (DNS-01)")
        CLOUDFLARE_ORIGIN = "cloudflare_origin", _("Cloudflare Origin CA")
        CUSTOM = "custom", _("Custom Certificate")
        SELF_SIGNED = "self_signed", _("Self-Signed")
        MANAGED_EXTERNALLY = "managed_externally", _("Managed Externally")

    class Status(models.TextChoices):
        IDLE = "idle", _("Idle")
        VALIDATING_DNS = "validating_dns", _("Validating DNS")
        CONFIGURING = "configuring", _("Configuring")
        OBTAINING_CERT = "obtaining_cert", _("Obtaining Certificate")
        RELOADING = "reloading", _("Reloading Services")
        ERROR = "error", _("Error")

    # Domain
    domain = models.CharField(
        max_length=253,
        blank=True,
        default="",
        verbose_name=_("Domain"),
        help_text=_("Fully qualified domain name (e.g., shop.example.com)"),
    )
    previous_domain = models.CharField(
        max_length=253,
        blank=True,
        default="",
        verbose_name=_("Previous Domain"),
        help_text=_("Domain before the last change, for rollback tracking"),
    )

    # SSL mode
    ssl_mode = models.CharField(
        max_length=20,
        choices=SSLMode.choices,
        default=SSLMode.NONE,
        verbose_name=_("SSL Mode"),
    )

    # Certificate info
    cert_domain = models.CharField(
        max_length=253,
        blank=True,
        default="",
        verbose_name=_("Certificate Domain"),
    )
    cert_issuer = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Certificate Issuer"),
    )
    cert_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Certificate Expiry"),
    )
    cert_obtained_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Certificate Obtained"),
    )
    is_wildcard = models.BooleanField(
        default=False,
        verbose_name=_("Wildcard Certificate"),
    )

    # Cloudflare integration
    cloudflare_api_token = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Cloudflare API Token"),
        help_text=_("API token for DNS-01 challenges or Origin CA"),
    )
    cloudflare_zone_id = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name=_("Cloudflare Zone ID"),
    )

    # Admin email for Let's Encrypt
    admin_email = models.EmailField(
        blank=True,
        default="",
        verbose_name=_("Admin Email"),
        help_text=_("Contact email for Let's Encrypt notifications"),
    )

    # Task status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IDLE,
        verbose_name=_("Status"),
    )
    last_error = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Last Error"),
    )
    task_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Active Task ID"),
        help_text=_("Celery task ID for the current operation"),
    )

    # Auto-renewal
    auto_renew = models.BooleanField(
        default=True,
        verbose_name=_("Auto-Renew"),
        help_text=_("Automatically renew certificates before expiry"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Domain Configuration")
        verbose_name_plural = _("Domain Configuration")

    def __str__(self):
        if self.domain:
            return f"{self.domain} ({self.get_ssl_mode_display()})"
        return _("No domain configured")

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance."""
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance

    @property
    def has_valid_cert(self):
        """Check if the current certificate is valid (not expired)."""
        if not self.cert_expires_at:
            return False
        return self.cert_expires_at > timezone.now()

    @property
    def cert_days_remaining(self):
        """Days until certificate expires, or None if no cert."""
        if not self.cert_expires_at:
            return None
        delta = self.cert_expires_at - timezone.now()
        return max(0, delta.days)

    @property
    def needs_renewal(self):
        """Check if certificate needs renewal (less than 30 days remaining)."""
        days = self.cert_days_remaining
        if days is None:
            return False
        return days < 30

    @property
    def is_ssl_enabled(self):
        """Check if any SSL mode is configured."""
        return self.ssl_mode != self.SSLMode.NONE

    def set_error(self, message):
        """Set error status with message."""
        self.status = self.Status.ERROR
        self.last_error = message
        self.save(update_fields=["status", "last_error", "updated_at"])

    def set_status(self, status):
        """Update the status field."""
        self.status = status
        if status != self.Status.ERROR:
            self.last_error = ""
        self.save(update_fields=["status", "last_error", "updated_at"])
