"""
Webhook system models for outbound webhook delivery.

This module provides models for configuring webhook endpoints and
tracking webhook deliveries with retry logic.
"""

import secrets
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_webhook_secret():
    """Generate a secure random secret for webhook signing."""
    return secrets.token_hex(32)


class WebhookEndpoint(models.Model):
    """
    Merchant-configured webhook endpoint.

    Stores the URL and configuration for a webhook receiver that will
    receive HTTP POST requests when subscribed events occur.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("name"), max_length=255, help_text=_("A friendly name to identify this webhook endpoint")
    )
    url = models.URLField(
        _("URL"), max_length=2048, help_text=_("The URL that will receive webhook POST requests")
    )
    secret = models.CharField(
        _("secret"),
        max_length=64,
        default=generate_webhook_secret,
        help_text=_("Secret key used for HMAC signature verification"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Whether this endpoint is currently receiving webhooks"),
    )

    # Event subscriptions
    events = models.JSONField(
        _("subscribed events"),
        default=list,
        help_text=_("List of event types this endpoint is subscribed to"),
    )

    # Configuration
    max_retries = models.PositiveIntegerField(
        _("max retries"),
        default=5,
        help_text=_("Maximum number of retry attempts for failed deliveries"),
    )
    timeout_seconds = models.PositiveIntegerField(
        _("timeout (seconds)"), default=30, help_text=_("Timeout in seconds for webhook requests")
    )

    # Metadata
    description = models.TextField(
        _("description"), blank=True, help_text=_("Optional description of this webhook endpoint")
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    last_triggered_at = models.DateTimeField(
        _("last triggered"),
        null=True,
        blank=True,
        help_text=_("When this endpoint last received a webhook"),
    )

    # Health tracking
    consecutive_failures = models.PositiveIntegerField(
        _("consecutive failures"),
        default=0,
        help_text=_("Number of consecutive failed delivery attempts"),
    )
    is_disabled_by_failures = models.BooleanField(
        _("disabled by failures"),
        default=False,
        help_text=_("Whether this endpoint was auto-disabled due to failures"),
    )

    class Meta:
        verbose_name = _("webhook endpoint")
        verbose_name_plural = _("webhook endpoints")
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.name} ({self.url[:50]}...)"
            if len(self.url) > 50
            else f"{self.name} ({self.url})"
        )

    def rotate_secret(self):
        """Generate a new secret for this endpoint."""
        self.secret = generate_webhook_secret()
        self.save(update_fields=["secret", "updated_at"])
        return self.secret

    def reset_failures(self):
        """Reset failure tracking for this endpoint."""
        self.consecutive_failures = 0
        self.is_disabled_by_failures = False
        self.save(update_fields=["consecutive_failures", "is_disabled_by_failures", "updated_at"])

    def record_failure(self, auto_disable_threshold=10):
        """
        Record a delivery failure and potentially auto-disable.

        Args:
            auto_disable_threshold: Number of consecutive failures before auto-disable
        """
        self.consecutive_failures += 1
        if self.consecutive_failures >= auto_disable_threshold:
            self.is_disabled_by_failures = True
        self.save(update_fields=["consecutive_failures", "is_disabled_by_failures", "updated_at"])

    def record_success(self):
        """Record a successful delivery and reset failure count."""
        from django.utils import timezone

        self.consecutive_failures = 0
        self.last_triggered_at = timezone.now()
        self.save(update_fields=["consecutive_failures", "last_triggered_at", "updated_at"])


class WebhookDelivery(models.Model):
    """
    Log of webhook delivery attempts.

    Tracks each delivery attempt including the payload, response, and retry status.
    """

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        SUCCESS = "success", _("Success")
        FAILED = "failed", _("Failed")
        RETRYING = "retrying", _("Retrying")
        SANDBOX_BLOCKED = "sandbox_blocked", _("Sandbox Blocked")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint = models.ForeignKey(
        WebhookEndpoint,
        on_delete=models.CASCADE,
        related_name="deliveries",
        verbose_name=_("endpoint"),
    )
    event_type = models.CharField(
        _("event type"),
        max_length=100,
        db_index=True,
        help_text=_("The type of event that triggered this delivery"),
    )

    # Payload
    payload = models.JSONField(
        _("payload"), help_text=_("The JSON payload sent to the webhook endpoint")
    )

    # Delivery status
    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )

    # Response tracking
    response_status_code = models.PositiveIntegerField(
        _("response status code"),
        null=True,
        blank=True,
        help_text=_("HTTP status code from the webhook receiver"),
    )
    response_body = models.TextField(
        _("response body"),
        blank=True,
        help_text=_("Response body from the webhook receiver (truncated)"),
    )
    response_headers = models.JSONField(
        _("response headers"),
        default=dict,
        blank=True,
        help_text=_("Response headers from the webhook receiver"),
    )
    response_time_ms = models.PositiveIntegerField(
        _("response time (ms)"),
        null=True,
        blank=True,
        help_text=_("Time taken for the webhook request in milliseconds"),
    )

    # Error tracking
    error_message = models.TextField(
        _("error message"), blank=True, help_text=_("Error message if delivery failed")
    )

    # Retry tracking
    attempt_count = models.PositiveIntegerField(
        _("attempt count"), default=0, help_text=_("Number of delivery attempts made")
    )
    next_retry_at = models.DateTimeField(
        _("next retry at"),
        null=True,
        blank=True,
        db_index=True,
        help_text=_("When the next retry attempt will be made"),
    )

    # Timestamps
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    delivered_at = models.DateTimeField(
        _("delivered at"),
        null=True,
        blank=True,
        help_text=_("When the webhook was successfully delivered"),
    )

    class Meta:
        verbose_name = _("webhook delivery")
        verbose_name_plural = _("webhook deliveries")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "next_retry_at"]),
            models.Index(fields=["endpoint", "created_at"]),
            models.Index(fields=["event_type", "created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} to {self.endpoint.name} ({self.status})"

    def mark_success(self, response_code, response_body, response_time_ms, response_headers=None):
        """Mark delivery as successful."""
        from django.utils import timezone

        self.status = self.Status.SUCCESS
        self.response_status_code = response_code
        self.response_body = response_body[:10000] if response_body else ""  # Truncate
        self.response_time_ms = response_time_ms
        self.response_headers = response_headers or {}
        self.delivered_at = timezone.now()
        self.next_retry_at = None
        self.save()

        # Update endpoint health
        self.endpoint.record_success()

    def mark_failed(
        self,
        error_message,
        response_code=None,
        response_body=None,
        response_time_ms=None,
        will_retry=False,
        next_retry_at=None,
    ):
        """Mark delivery as failed or retrying."""
        self.status = self.Status.RETRYING if will_retry else self.Status.FAILED
        self.error_message = error_message
        self.response_status_code = response_code
        self.response_body = response_body[:10000] if response_body else ""
        self.response_time_ms = response_time_ms
        self.next_retry_at = next_retry_at
        self.save()

        # Update endpoint health only on final failure
        if not will_retry:
            self.endpoint.record_failure()
