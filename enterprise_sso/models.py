import logging

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class SSOProviderConfig(models.Model):
    """
    Singleton model for enterprise SSO (OIDC) provider configuration.

    Uses pk=1 pattern like SiteSettings. Stores OIDC provider endpoints,
    client credentials, claims mapping, and role mapping configuration.
    """

    # Display
    provider_name = models.CharField(
        max_length=100,
        default='SSO',
        verbose_name=_("Provider Name"),
        help_text=_("Display name for the SSO button, e.g. 'Microsoft', 'Okta', 'Google Workspace'"),
    )

    # OIDC Core Settings
    oidc_discovery_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("OIDC Discovery URL"),
        help_text=_("OpenID Connect discovery endpoint (e.g. https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration)"),
    )
    oidc_authorization_endpoint = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("Authorization Endpoint"),
    )
    oidc_token_endpoint = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("Token Endpoint"),
    )
    oidc_userinfo_endpoint = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("UserInfo Endpoint"),
    )
    oidc_jwks_endpoint = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("JWKS Endpoint"),
    )
    oidc_end_session_endpoint = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("End Session Endpoint"),
        help_text=_("Used for single sign-out (optional)"),
    )

    # Client credentials
    oidc_client_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Client ID"),
        help_text=_("Application/Client ID from your identity provider"),
    )
    oidc_client_secret_encrypted = models.BinaryField(
        blank=True,
        default=b'',
        verbose_name=_("Client Secret (Encrypted)"),
    )

    # Claims mapping
    claim_email = models.CharField(
        max_length=100,
        default='email',
        verbose_name=_("Email Claim"),
        help_text=_("OIDC claim field for user email address"),
    )
    claim_first_name = models.CharField(
        max_length=100,
        default='given_name',
        verbose_name=_("First Name Claim"),
        help_text=_("OIDC claim field for first name"),
    )
    claim_last_name = models.CharField(
        max_length=100,
        default='family_name',
        verbose_name=_("Last Name Claim"),
        help_text=_("OIDC claim field for last name"),
    )
    claim_groups = models.CharField(
        max_length=100,
        default='groups',
        blank=True,
        verbose_name=_("Groups Claim"),
        help_text=_("OIDC claim field for group memberships (leave blank to disable group mapping)"),
    )

    # Role mapping
    staff_groups = models.TextField(
        blank=True,
        verbose_name=_("Staff Groups"),
        help_text=_("Comma-separated group names or IDs that grant staff status"),
    )
    superuser_groups = models.TextField(
        blank=True,
        verbose_name=_("Superuser Groups"),
        help_text=_("Comma-separated group names or IDs that grant superuser status"),
    )

    # Scopes
    oidc_scopes = models.CharField(
        max_length=500,
        default='openid email profile',
        verbose_name=_("OIDC Scopes"),
        help_text=_("Space-separated OIDC scopes to request"),
    )

    # Behavior
    auto_create_users = models.BooleanField(
        default=False,
        verbose_name=_("Auto-Create Users"),
        help_text=_("Automatically create a user account when an SSO user signs in for the first time"),
    )
    restrict_to_staff = models.BooleanField(
        default=True,
        verbose_name=_("Restrict to Staff"),
        help_text=_("Only allow existing staff users to sign in via SSO. Disable to allow SSO user auto-creation."),
    )

    class Meta:
        verbose_name = _("SSO Provider Configuration")
        verbose_name_plural = _("SSO Provider Configuration")

    def __str__(self):
        return f"SSO Provider: {self.provider_name}"

    @classmethod
    def get_config(cls):
        """Get or create the singleton SSO configuration."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def is_configured(self):
        """Check if the SSO provider has minimum required configuration."""
        return bool(
            self.oidc_client_id
            and self.oidc_client_secret_encrypted
            and (self.oidc_discovery_url or self.oidc_authorization_endpoint)
        )

    def set_client_secret(self, plain_secret):
        """Encrypt and store the client secret."""
        if not plain_secret:
            self.oidc_client_secret_encrypted = b''
            return

        encryption_key = getattr(settings, 'EMAIL_ENCRYPTION_KEY', None)
        if not encryption_key:
            logger.warning("EMAIL_ENCRYPTION_KEY not set - storing client secret unencrypted")
            self.oidc_client_secret_encrypted = plain_secret.encode()
            return

        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()

        f = Fernet(encryption_key)
        self.oidc_client_secret_encrypted = f.encrypt(plain_secret.encode())

    def get_client_secret(self):
        """Decrypt and return the client secret."""
        if not self.oidc_client_secret_encrypted:
            return ''

        encrypted = self.oidc_client_secret_encrypted
        if isinstance(encrypted, memoryview):
            encrypted = bytes(encrypted)

        if not encrypted:
            return ''

        encryption_key = getattr(settings, 'EMAIL_ENCRYPTION_KEY', None)
        if not encryption_key:
            # Stored unencrypted (fallback)
            return encrypted.decode()

        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()

        try:
            f = Fernet(encryption_key)
            return f.decrypt(encrypted).decode()
        except Exception:
            logger.error("Failed to decrypt SSO client secret")
            return ''
