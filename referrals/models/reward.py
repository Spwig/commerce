"""
Referral Reward model.

Tracks rewards issued to referrers and referees.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

User = get_user_model()


class ReferralReward(models.Model):
    """
    Reward issued for successful referral.

    Tracks rewards for both referrer and referee (double-sided rewards).
    Supports multiple reward types: credit, coupon, percent, perk.
    """

    KIND_CHOICES = [
        ('credit', _('Store Credit')),
        ('coupon', _('Coupon Code')),
        ('percent', _('Percentage Discount')),
        ('perk', _('Exclusive Perk')),
    ]

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('issued', _('Issued')),
        ('redeemed', _('Redeemed')),
        ('expired', _('Expired')),
        ('revoked', _('Revoked')),
    ]

    RECIPIENT_TYPE_CHOICES = [
        ('referrer', _('Referrer')),
        ('referee', _('Referee')),
    ]

    # Link to program
    program = models.ForeignKey(
        'referrals.ReferralProgram',
        on_delete=models.CASCADE,
        related_name='rewards',
        verbose_name=_('Program')
    )

    # Link to attribution case
    attribution = models.ForeignKey(
        'referrals.ReferralAttribution',
        on_delete=models.CASCADE,
        related_name='rewards',
        verbose_name=_('Attribution')
    )

    # Link to referrer identity (for referrer rewards)
    referrer_identity = models.ForeignKey(
        'referrals.ReferralIdentity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rewards_earned',
        verbose_name=_('Referrer Identity')
    )

    # Link to customer (recipient of reward)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referral_rewards',
        verbose_name=_('Customer')
    )

    # Recipient type (referrer or referee)
    recipient_type = models.CharField(
        max_length=10,
        choices=RECIPIENT_TYPE_CHOICES,
        default='referrer',
        verbose_name=_('Recipient Type')
    )

    # Reward Details
    kind = models.CharField(
        max_length=24,
        choices=KIND_CHOICES,
        db_index=True,
        verbose_name=_('Reward Kind')
    )
    amount = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_('Amount'),
        help_text=_('Reward amount (for credit, coupon value, or cap)')
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Percentage'),
        help_text=_('Percentage discount (for percent kind)')
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Description'),
        help_text=_('Description of the reward or perk')
    )

    # Status
    status = models.CharField(
        max_length=24,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        verbose_name=_('Status')
    )

    # Integration Links
    wallet_transaction = models.ForeignKey(
        'wallet.WalletTransaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referral_rewards',
        verbose_name=_('Wallet Transaction'),
        help_text=_('Linked wallet transaction if reward is store credit'),
    )

    # Voucher integration (ID reference — FK can be enabled later)
    voucher_code_id = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Voucher Code ID'),
        help_text=_('ID of voucher code if reward is a coupon'),
    )

    # Lifecycle Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    issued_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Issued At'),
        help_text=_('When the reward was issued to the customer')
    )
    redeemed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Redeemed At'),
        help_text=_('When the reward was redeemed')
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_('Expires At'),
        help_text=_('Expiry date for unredeemed rewards')
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Revoked At')
    )
    revocation_reason = models.TextField(
        blank=True,
        default='',
        verbose_name=_('Revocation Reason')
    )

    class Meta:
        verbose_name = _('Issued Reward')
        verbose_name_plural = _('Issued Rewards')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['kind', 'status']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['recipient_type', 'status']),
        ]

    def __str__(self):
        customer_name = 'Unknown'
        if self.customer:
            customer_name = self.customer.get_full_name() or self.customer.email

        return f"{customer_name} - {self.get_kind_display()} - {self.amount} ({self.get_status_display()})"

    def issue(self):
        """
        Mark reward as issued.

        This should be called after wallet credit or coupon has been created.
        """
        from django.utils import timezone

        self.status = 'issued'
        self.issued_at = timezone.now()
        self.save(update_fields=['status', 'issued_at'])

    def redeem(self):
        """Mark reward as redeemed."""
        from django.utils import timezone

        self.status = 'redeemed'
        self.redeemed_at = timezone.now()
        self.save(update_fields=['status', 'redeemed_at'])

    def revoke(self, reason=''):
        """
        Revoke this reward.

        Args:
            reason (str): Reason for revocation
        """
        from django.utils import timezone

        self.status = 'revoked'
        self.revoked_at = timezone.now()
        self.revocation_reason = reason
        self.save(update_fields=['status', 'revoked_at', 'revocation_reason'])

    def expire(self):
        """Mark reward as expired."""
        self.status = 'expired'
        self.save(update_fields=['status'])

    def is_pending(self):
        """Check if reward is pending."""
        return self.status == 'pending'

    def is_issued(self):
        """Check if reward is issued."""
        return self.status == 'issued'

    def is_redeemed(self):
        """Check if reward is redeemed."""
        return self.status == 'redeemed'

    def is_expired(self):
        """Check if reward is expired."""
        return self.status == 'expired'

    def is_revoked(self):
        """Check if reward is revoked."""
        return self.status == 'revoked'

    def is_expiring_soon(self, days=7):
        """
        Check if reward is expiring within N days.

        Args:
            days (int): Number of days threshold (default 7)

        Returns:
            bool: True if expiring soon
        """
        if not self.expires_at or self.status != 'issued':
            return False

        from django.utils import timezone
        from datetime import timedelta

        return self.expires_at <= timezone.now() + timedelta(days=days)
