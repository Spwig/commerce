"""
Referral Event tracking model.

Logs all referral-related events: clicks, signups, orders, approvals, rejections.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ReferralEvent(models.Model):
    """
    Event tracking for referral program.

    Logs every event in the referral funnel: click → signup → order → approval/rejection.
    Used for analytics and fraud detection.
    """

    EVENT_TYPE_CHOICES = [
        ("click", _("Click")),
        ("signup", _("Signup")),
        ("order", _("Order")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
        ("reward_issued", _("Reward Issued")),
        ("reward_redeemed", _("Reward Redeemed")),
    ]

    # Link to program
    program = models.ForeignKey(
        "referrals.ReferralProgram",
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("Program"),
    )

    # Link to referrer identity
    referrer_identity = models.ForeignKey(
        "referrals.ReferralIdentity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name=_("Referrer Identity"),
    )

    # Link to customer (referee or referrer depending on event type)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referral_events",
        verbose_name=_("Customer"),
    )

    # Link to order (if applicable)
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referral_events",
        verbose_name=_("Order"),
    )

    # Event type
    event_type = models.CharField(
        max_length=24, choices=EVENT_TYPE_CHOICES, db_index=True, verbose_name=_("Event Type")
    )

    # Tracking Data
    ip_address = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name=_("IP Address"),
        help_text=_("Hashed IP address of the visitor (for privacy)"),
    )
    user_agent = models.TextField(
        blank=True,
        default="",
        verbose_name=_("User Agent"),
        help_text=_("Browser user agent string"),
    )
    device_fingerprint = models.CharField(
        max_length=64,
        blank=True,
        default="",
        db_index=True,
        verbose_name=_("Device Fingerprint"),
        help_text=_("Hashed device fingerprint for fraud detection"),
    )
    referrer_url = models.URLField(
        max_length=500,
        blank=True,
        default="",
        verbose_name=_("Referrer URL"),
        help_text=_("HTTP referrer header"),
    )
    landing_url = models.URLField(
        max_length=500,
        blank=True,
        default="",
        verbose_name=_("Landing URL"),
        help_text=_("URL where the visitor landed"),
    )

    # Additional Metadata (JSON)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional event data (utm params, browser info, etc.)"),
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Referral Event")
        verbose_name_plural = _("Referral Events")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["referrer_identity", "event_type"]),
            models.Index(fields=["customer", "event_type"]),
            models.Index(fields=["device_fingerprint"]),
        ]

    def __str__(self):
        if self.referrer_identity:
            referrer_name = (
                self.referrer_identity.customer.get_full_name()
                or self.referrer_identity.customer.email
            )
            return f"{self.get_event_type_display()} - {referrer_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        return f"{self.get_event_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @staticmethod
    def log_event(
        event_type, program, referrer_identity=None, customer=None, order=None, **tracking_data
    ):
        """
        Static method to log an event.

        Args:
            event_type (str): Type of event (click, signup, order, etc.)
            program (ReferralProgram): Program instance
            referrer_identity (ReferralIdentity, optional): Referrer identity
            customer (User, optional): Customer instance
            order (Order, optional): Order instance
            **tracking_data: Additional tracking data (ip, user_agent, urls, metadata)

        Returns:
            ReferralEvent: Created event instance
        """
        return ReferralEvent.objects.create(
            event_type=event_type,
            program=program,
            referrer_identity=referrer_identity,
            customer=customer,
            order=order,
            ip_address=tracking_data.get("ip_address"),
            user_agent=tracking_data.get("user_agent", ""),
            device_fingerprint=tracking_data.get("device_fingerprint", ""),
            referrer_url=tracking_data.get("referrer_url", ""),
            landing_url=tracking_data.get("landing_url", ""),
            metadata=tracking_data.get("metadata", {}),
        )
