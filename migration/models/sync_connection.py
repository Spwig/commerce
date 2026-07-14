"""
SyncConnection Model
Stores saved connection profiles for Spwig-to-Spwig sync and migration.
"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SyncConnection(models.Model):
    """
    Saved connection to another Spwig instance.
    Reusable across sync jobs and full migrations.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200, help_text=_("Descriptive name (e.g., 'Production Server', 'Staging')")
    )

    ROLE_CHOICES = [
        ("production", _("Production")),
        ("staging", _("Staging")),
        ("backup", _("Backup")),
        ("other", _("Other")),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="other",
        help_text=_("Role of the remote instance"),
    )

    remote_url = models.URLField(
        help_text=_("Base URL of the remote Spwig instance (e.g., https://merchant-store.com)")
    )

    # Encrypted SyncToken for authenticating with the remote instance
    auth_token = models.TextField(
        help_text=_("SyncToken for the remote instance (stored encrypted)")
    )

    # Remote instance metadata (populated on connection test)
    remote_version = models.CharField(
        max_length=20, blank=True, help_text=_("Spwig version running on the remote instance")
    )
    remote_site_name = models.CharField(
        max_length=200, blank=True, help_text=_("Site name of the remote instance")
    )

    is_verified = models.BooleanField(
        default=False, help_text=_("Whether the connection has been verified")
    )
    last_verified_at = models.DateTimeField(
        null=True, blank=True, help_text=_("Last successful connection test")
    )
    last_sync_at = models.DateTimeField(
        null=True, blank=True, help_text=_("Last time a sync was performed using this connection")
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sync_connections",
        help_text=_("User who created this connection"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = _("Sync Connection")
        verbose_name_plural = _("Sync Connections")

    def __str__(self):
        return f"{self.name} ({self.get_role_display()}) - {self.remote_url}"

    @property
    def is_production(self):
        return self.role == "production"
