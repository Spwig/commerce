"""
Referral Attribution model.

Links referrer → referee → first order for attribution tracking.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ReferralAttribution(models.Model):
    """
    Attribution case linking referrer to referee's first order.

    Represents a complete referral case from link click through conversion.
    Subject to validation and fraud checks before approval.
    """

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
        ("expired", _("Expired")),
    ]

    REJECTION_REASON_CHOICES = [
        ("self_referral", _("Self Referral")),
        ("not_new_customer", _("Not New Customer")),
        ("below_minimum", _("Below Minimum Order Value")),
        ("disposable_email", _("Disposable Email")),
        ("cap_exceeded", _("Cap Exceeded")),
        ("fraud_risk", _("Fraud Risk")),
        ("order_refunded", _("Order Refunded")),
        ("order_cancelled", _("Order Cancelled")),
        ("manual_rejection", _("Manual Rejection")),
        ("other", _("Other")),
    ]

    # Link to program
    program = models.ForeignKey(
        "referrals.ReferralProgram",
        on_delete=models.CASCADE,
        related_name="attributions",
        verbose_name=_("Program"),
    )

    # Link to referrer identity
    referrer_identity = models.ForeignKey(
        "referrals.ReferralIdentity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals_made",
        verbose_name=_("Referrer Identity"),
    )

    # Link to referee (new customer)
    referee_customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referred_by",
        verbose_name=_("Referee Customer"),
    )

    # Link to first order
    first_order = models.OneToOneField(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referral_attribution",
        verbose_name=_("First Order"),
    )

    # Status
    status = models.CharField(
        max_length=24,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
        verbose_name=_("Status"),
    )

    # Rejection Details
    rejection_reason = models.CharField(
        max_length=64,
        choices=REJECTION_REASON_CHOICES,
        blank=True,
        default="",
        db_index=True,
        verbose_name=_("Rejection Reason"),
    )
    rejection_notes = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Rejection Notes"),
        help_text=_("Additional notes about why this was rejected"),
    )

    # Validation Data (JSON)
    validation_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Validation Data"),
        help_text=_("Results from fraud detection and validation checks"),
    )

    # Risk Score (0-100, higher = riskier)
    risk_score = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Risk Score"), help_text=_("Calculated fraud risk score (0-100)")
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Approved At"))
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Reviewed At"))
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_attributions",
        verbose_name=_("Reviewed By"),
        help_text=_("Admin user who approved/rejected this attribution"),
    )

    class Meta:
        verbose_name = _("Referral Attribution")
        verbose_name_plural = _("Referral Attributions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["referrer_identity", "status"]),
            models.Index(fields=["referee_customer"]),
            models.Index(fields=["first_order"]),
            models.Index(fields=["rejection_reason"]),
            models.Index(fields=["risk_score"]),
        ]

    def __str__(self):
        referrer_name = "Unknown"
        referee_name = "Unknown"

        if self.referrer_identity and self.referrer_identity.customer:
            referrer_name = (
                self.referrer_identity.customer.get_full_name()
                or self.referrer_identity.customer.email
            )

        if self.referee_customer:
            referee_name = self.referee_customer.get_full_name() or self.referee_customer.email

        return f"{referrer_name} → {referee_name} ({self.get_status_display()})"

    def approve(self, reviewed_by=None):
        """
        Approve this attribution.

        Args:
            reviewed_by (User, optional): Admin user who approved
        """
        from django.utils import timezone

        self.status = "approved"
        self.approved_at = timezone.now()
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.save(update_fields=["status", "approved_at", "reviewed_at", "reviewed_by"])

    def reject(self, reason, notes="", reviewed_by=None):
        """
        Reject this attribution.

        Args:
            reason (str): Rejection reason code
            notes (str): Additional notes
            reviewed_by (User, optional): Admin user who rejected
        """
        from django.utils import timezone

        self.status = "rejected"
        self.rejection_reason = reason
        self.rejection_notes = notes
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.save(
            update_fields=[
                "status",
                "rejection_reason",
                "rejection_notes",
                "reviewed_at",
                "reviewed_by",
            ]
        )

    def is_pending(self):
        """Check if attribution is pending review."""
        return self.status == "pending"

    def is_approved(self):
        """Check if attribution is approved."""
        return self.status == "approved"

    def is_rejected(self):
        """Check if attribution is rejected."""
        return self.status == "rejected"

    def get_order_value(self):
        """Get the order total value."""
        if self.first_order:
            return self.first_order.total_amount
        return 0

    def get_risk_level(self):
        """
        Get human-readable risk level based on risk_score.

        Returns:
            str: 'low', 'medium', 'high', or 'critical'
        """
        if self.risk_score < 30:
            return "low"
        elif self.risk_score < 70:
            return "medium"
        elif self.risk_score < 90:
            return "high"
        return "critical"
