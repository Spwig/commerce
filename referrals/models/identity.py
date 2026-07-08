"""
Referral Identity model.

Each customer gets one referral identity with a unique token for tracking.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import secrets

User = get_user_model()


class ReferralIdentity(models.Model):
    """
    Unique referral identity for each customer/referrer.

    Each customer gets a unique token for their referral link and QR code.
    Denormalized stats tracked for performance.
    """

    # Link to customer (OneToOne)
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='referral_identity',
        verbose_name=_('Customer')
    )

    # Unique token for referral links
    token = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name=_('Referral Token'),
        help_text=_('Unique token used in referral links')
    )

    # QR Code image (optional)
    qr_code = models.ImageField(
        upload_to='referrals/qr_codes/',
        blank=True,
        null=True,
        verbose_name=_('QR Code'),
        help_text=_('Generated QR code for this referral link')
    )

    # Denormalized Stats (updated via signals)
    total_clicks = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Clicks'),
        help_text=_('Total number of referral link clicks')
    )
    total_signups = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Signups'),
        help_text=_('Total number of signups from referrals')
    )
    total_conversions = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Conversions'),
        help_text=_('Total number of successful referral conversions')
    )
    total_rewards_earned = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('Total Rewards Earned'),
        help_text=_('Total value of rewards earned from referrals')
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Referral Identity')
        verbose_name_plural = _('Referral Identities')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['customer']),
        ]

    def __str__(self):
        customer_name = self.customer.get_full_name() or self.customer.email
        return f"{customer_name} - {self.token}"

    def save(self, *args, **kwargs):
        """Auto-generate token if not set."""
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_token(length=12):
        """
        Generate a secure random token for referral links.

        Args:
            length (int): Length of the token (default 12 characters)

        Returns:
            str: Secure random token
        """
        return secrets.token_urlsafe(length)[:length]

    def get_referral_link(self, request=None):
        """
        Get the full referral link for this identity.

        Args:
            request (HttpRequest, optional): Request object for building absolute URL

        Returns:
            str: Full referral link
        """
        # For now, return a relative URL. Will be updated when we have the view.
        return f"/?ref={self.token}"

    def get_conversion_rate(self):
        """
        Calculate conversion rate (conversions / clicks).

        Returns:
            float: Conversion rate as percentage (0-100)
        """
        if self.total_clicks == 0:
            return 0.0
        return (self.total_conversions / self.total_clicks) * 100

    def get_signup_rate(self):
        """
        Calculate signup rate (signups / clicks).

        Returns:
            float: Signup rate as percentage (0-100)
        """
        if self.total_clicks == 0:
            return 0.0
        return (self.total_signups / self.total_clicks) * 100

    def increment_clicks(self):
        """Increment click counter (called by tracking service)."""
        self.total_clicks += 1
        self.save(update_fields=['total_clicks', 'updated_at'])

    def increment_signups(self):
        """Increment signup counter (called by tracking service)."""
        self.total_signups += 1
        self.save(update_fields=['total_signups', 'updated_at'])

    def increment_conversions(self, reward_amount=0):
        """
        Increment conversion counter and total rewards.

        Args:
            reward_amount (Decimal): Amount of reward earned
        """
        self.total_conversions += 1
        self.total_rewards_earned += reward_amount
        self.save(update_fields=['total_conversions', 'total_rewards_earned', 'updated_at'])
