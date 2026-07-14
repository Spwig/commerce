"""
Referral Program configuration model.

This model follows a singleton pattern - only one active program per installation.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import get_default_currency


class ReferralProgram(models.Model):
    """
    Singleton model for referral program configuration.

    Merchants configure rewards, eligibility rules, fraud policies, and tracking settings.
    """

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("active", _("Active")),
        ("paused", _("Paused")),
    ]

    # Basic Info
    name = models.CharField(
        max_length=120,
        default=_("Referral Program"),
        verbose_name=_("Program Name"),
        help_text=_("Internal name for this referral program"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name=_("Status"),
        help_text=_("Program status: draft, active, or paused"),
    )

    # Reward Configuration (JSON)
    reward_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Reward Configuration"),
        help_text=_(
            'Reward types, amounts, and double-sided settings. Example: {"referrer": {"kind": "credit", "amount": 10}, "referee": {"kind": "discount", "amount": 10}}'
        ),
    )

    # Eligibility Rules (JSON)
    eligibility_rules = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Eligibility Rules"),
        help_text=_("Rules like minimum order value, new customers only, exclude staff, etc."),
    )

    # Timing Configuration (JSON)
    timing_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Timing Configuration"),
        help_text=_("When to issue rewards: signup, first purchase, post-refund window, etc."),
    )

    # Caps & Limits (JSON)
    caps_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Caps & Limits"),
        help_text=_("Monthly/lifetime caps per referrer, maximum reward amounts, etc."),
    )

    # Tracking Configuration (JSON)
    tracking_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Tracking Configuration"),
        help_text=_("Cookie TTL, attribution method (last-touch), tracking window, etc."),
    )

    # Fraud Policy (JSON)
    fraud_policy = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Fraud Policy"),
        help_text=_("Fraud detection thresholds and rules (strict/balanced/lenient)"),
    )

    # Terms & Conditions
    terms_and_conditions = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Terms & Conditions"),
        help_text=_("Legal T&Cs shown to customers (supports Markdown)"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Referral Program")
        verbose_name_plural = _("Referral Program")  # Singular because it's a singleton
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @classmethod
    def get_program(cls):
        """
        Get or create the singleton program instance.

        Returns:
            ReferralProgram: The single program instance
        """
        program, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                "name": _("Referral Program"),
                "status": "draft",
                "reward_config": {
                    "referrer": {
                        "kind": "credit",
                        "amount": 10,
                        "currency": get_default_currency(),
                    },
                    "referee": {
                        "kind": "discount",
                        "amount": 10,
                        "currency": get_default_currency(),
                    },
                    "double_sided": True,
                },
                "eligibility_rules": {
                    "new_customer_only": True,
                    "min_order_value": 40.0,
                    "exclude_discounts": False,
                    "exclude_staff": True,
                },
                "timing_config": {
                    "issue_on": "post_refund",
                    "refund_window_days": 14,
                },
                "caps_config": {
                    "monthly_per_referrer": 20,
                    "lifetime_per_referrer": 200,
                    "max_reward_per_order": 50,
                },
                "tracking_config": {
                    "cookie_ttl_days": 30,
                    "attribution": "last_touch",
                },
                "fraud_policy": {
                    "policy": "balanced",
                    "auto_reject_threshold": 80,
                    "auto_approve_threshold": 30,
                    "check_ip": True,
                    "check_device": True,
                    "check_velocity": True,
                    "velocity_window_hours": 24,
                    "max_referrals_per_window": 5,
                },
            },
        )
        return program

    def save(self, *args, **kwargs):
        """Override save to enforce singleton pattern."""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of the singleton instance."""
        raise ValidationError(
            _('Cannot delete the referral program. Set status to "Paused" instead.')
        )

    def is_active(self):
        """Check if program is currently active."""
        return self.status == "active"

    def get_min_order_value(self):
        """Get minimum order value from eligibility rules."""
        return self.eligibility_rules.get("min_order_value", 0)

    def get_cookie_ttl_days(self):
        """Get cookie TTL in days from tracking config."""
        return self.tracking_config.get("cookie_ttl_days", 30)

    def get_refund_window_days(self):
        """Get refund window in days from timing config."""
        return self.timing_config.get("refund_window_days", 14)

    def get_monthly_cap(self):
        """Get monthly referral cap per referrer."""
        return self.caps_config.get("monthly_per_referrer", 20)

    def get_lifetime_cap(self):
        """Get lifetime referral cap per referrer."""
        return self.caps_config.get("lifetime_per_referrer", 200)
