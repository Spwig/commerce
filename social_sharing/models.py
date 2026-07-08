"""
Social Sharing Models

Tracks social media shares for products, categories, pages, and other content.
Provides aggregated counts for performance and analytics.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()


class SocialShare(models.Model):
    """
    Track individual social media share events.

    Uses Generic Foreign Key to support sharing any content type
    (products, categories, blog posts, pages, etc.)
    """

    # Platform choices
    PLATFORM_FACEBOOK = 'facebook'
    PLATFORM_TWITTER = 'twitter'
    PLATFORM_LINKEDIN = 'linkedin'
    PLATFORM_PINTEREST = 'pinterest'
    PLATFORM_WHATSAPP = 'whatsapp'
    PLATFORM_TELEGRAM = 'telegram'
    PLATFORM_EMAIL = 'email'

    PLATFORM_CHOICES = [
        (PLATFORM_FACEBOOK, _('Facebook')),
        (PLATFORM_TWITTER, _('Twitter/X')),
        (PLATFORM_LINKEDIN, _('LinkedIn')),
        (PLATFORM_PINTEREST, _('Pinterest')),
        (PLATFORM_WHATSAPP, _('WhatsApp')),
        (PLATFORM_TELEGRAM, _('Telegram')),
        (PLATFORM_EMAIL, _('Email')),
    ]

    # Device type choices
    DEVICE_DESKTOP = 'desktop'
    DEVICE_MOBILE = 'mobile'
    DEVICE_TABLET = 'tablet'
    DEVICE_UNKNOWN = 'unknown'

    DEVICE_CHOICES = [
        (DEVICE_DESKTOP, _('Desktop')),
        (DEVICE_MOBILE, _('Mobile')),
        (DEVICE_TABLET, _('Tablet')),
        (DEVICE_UNKNOWN, _('Unknown')),
    ]

    # What was shared - Generic Foreign Key
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('content type'),
        help_text=_('Type of content shared (Product, Category, etc.)')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('object ID'),
        help_text=_('ID of the shared object')
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # Share details
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        db_index=True,
        verbose_name=_('platform'),
        help_text=_('Social platform used for sharing')
    )

    shared_url = models.URLField(
        max_length=500,
        verbose_name=_('shared URL'),
        help_text=_('URL that was shared')
    )

    referrer = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_('referrer'),
        help_text=_('Page from which share was initiated')
    )

    # User tracking (optional - for loyalty integration)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='social_shares',
        verbose_name=_('user'),
        help_text=_('User who shared (if logged in)')
    )

    # Session and device tracking
    session_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('session ID'),
        help_text=_('Session identifier for anonymous users')
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP address'),
        help_text=_('IP address of sharer (for analytics and fraud detection)')
    )

    user_agent = models.TextField(
        blank=True,
        verbose_name=_('user agent'),
        help_text=_('Browser user agent string')
    )

    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_CHOICES,
        default=DEVICE_UNKNOWN,
        verbose_name=_('device type'),
        help_text=_('Type of device used for sharing')
    )

    # Timestamps
    shared_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('shared at'),
        help_text=_('When the share occurred')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at')
    )

    class Meta:
        verbose_name = _('Social Share')
        verbose_name_plural = _('Social Shares')
        db_table = 'social_shares'
        ordering = ['-shared_at']
        indexes = [
            models.Index(fields=['platform', 'shared_at'], name='social_share_platform_date'),
            models.Index(fields=['content_type', 'object_id'], name='social_share_content'),
            models.Index(fields=['user', 'shared_at'], name='social_share_user_date'),
            models.Index(fields=['session_id'], name='social_share_session'),
            models.Index(fields=['shared_at'], name='social_share_date'),
        ]

    def __str__(self):
        user_info = self.user.email if self.user else 'Anonymous'
        return f"{user_info} shared on {self.get_platform_display()} - {self.shared_at.strftime('%Y-%m-%d %H:%M')}"

    def __repr__(self):
        return f"<SocialShare id={self.id} platform={self.platform} user={self.user_id}>"


class ShareCount(models.Model):
    """
    Aggregated share counts for performance.

    Instead of counting SocialShare records every time, we maintain
    aggregated counts that update via signals. Much faster for display.
    """

    # What was shared - Generic Foreign Key
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('content type')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('object ID')
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # Platform-specific count
    platform = models.CharField(
        max_length=20,
        choices=SocialShare.PLATFORM_CHOICES,
        verbose_name=_('platform')
    )

    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('share count'),
        help_text=_('Number of times shared on this platform')
    )

    # Timestamps
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('last updated')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    class Meta:
        verbose_name = _('Share Count')
        verbose_name_plural = _('Share Counts')
        db_table = 'social_share_counts'
        unique_together = [['content_type', 'object_id', 'platform']]
        indexes = [
            models.Index(fields=['content_type', 'object_id'], name='share_count_content'),
            models.Index(fields=['count'], name='share_count_value'),
        ]

    def __str__(self):
        return f"{self.get_platform_display()}: {self.count} shares"

    def __repr__(self):
        return f"<ShareCount content_type={self.content_type_id} object_id={self.object_id} platform={self.platform} count={self.count}>"


# Import settings model
from social_sharing.settings_models import SocialSharingSettings  # noqa: E402
