"""
Social Sharing Settings Models

Allows merchants to configure social sharing behavior through admin interface
without editing code.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache


class SocialSharingSettings(models.Model):
    """
    Global settings for social sharing functionality.

    Singleton model - only one instance should exist.
    Merchants configure these settings through admin interface.
    """

    class Meta:
        verbose_name = _("Social Sharing Settings")
        verbose_name_plural = _("Social Sharing Settings")

    # Automatic placement settings
    enable_on_products = models.BooleanField(
        default=True,
        verbose_name=_("Enable on Products"),
        help_text=_("Automatically show share buttons on product detail pages")
    )

    enable_on_categories = models.BooleanField(
        default=False,
        verbose_name=_("Enable on Categories"),
        help_text=_("Automatically show share buttons on category pages")
    )

    enable_on_blog_posts = models.BooleanField(
        default=True,
        verbose_name=_("Enable on Blog Posts"),
        help_text=_("Automatically show share buttons on blog post pages")
    )

    enable_on_pages = models.BooleanField(
        default=False,
        verbose_name=_("Enable on Custom Pages"),
        help_text=_("Automatically show share buttons on custom pages")
    )

    # Placement position
    POSITION_CHOICES = [
        ('above_content', _('Above Content')),
        ('below_content', _('Below Content')),
        ('sidebar', _('Sidebar')),
        ('floating', _('Floating (sticky)')),
    ]

    placement_position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='below_content',
        verbose_name=_("Placement Position"),
        help_text=_("Where to display share buttons on the page")
    )

    # Button display style
    BUTTON_STYLE_CHOICES = [
        ('icon_only', _('Icon Only')),
        ('icon_label', _('Icon + Label')),
        ('label_only', _('Label Only')),
    ]

    button_style = models.CharField(
        max_length=20,
        choices=BUTTON_STYLE_CHOICES,
        default='icon_only',
        verbose_name=_("Button Style"),
        help_text=_("How share buttons are displayed")
    )

    # Button size
    BUTTON_SIZE_CHOICES = [
        ('small', _('Small')),
        ('medium', _('Medium')),
        ('large', _('Large')),
    ]

    button_size = models.CharField(
        max_length=10,
        choices=BUTTON_SIZE_CHOICES,
        default='medium',
        verbose_name=_("Button Size"),
        help_text=_("Size of the share buttons")
    )

    # Layout direction
    LAYOUT_DIRECTION_CHOICES = [
        ('horizontal', _('Horizontal')),
        ('vertical', _('Vertical')),
    ]

    layout_direction = models.CharField(
        max_length=12,
        choices=LAYOUT_DIRECTION_CHOICES,
        default='horizontal',
        verbose_name=_("Layout Direction"),
        help_text=_("Arrange share buttons horizontally or vertically")
    )

    # Show title
    show_title = models.BooleanField(
        default=True,
        verbose_name=_("Show Title"),
        help_text=_("Show the 'Share' heading above the buttons")
    )

    # Mobile visibility
    MOBILE_VISIBILITY_CHOICES = [
        ('show', _('Always Show')),
        ('hide', _('Hide on Mobile')),
        ('mobile_only', _('Mobile Only')),
    ]

    mobile_visibility = models.CharField(
        max_length=12,
        choices=MOBILE_VISIBILITY_CHOICES,
        default='show',
        verbose_name=_("Mobile Visibility"),
        help_text=_("Control whether share buttons appear on mobile devices")
    )

    # Widget configuration (references the widget package)
    widget_slug = models.CharField(
        max_length=100,
        default='social_share_buttons',
        verbose_name=_("Widget Slug"),
        help_text=_("Slug of the widget package to use for rendering")
    )

    # Default widget config override
    default_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Default Widget Configuration"),
        help_text=_("Override default widget configuration (display_style, button_size, etc.)")
    )

    # Enabled platforms
    enabled_platforms = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Enabled Platforms"),
        help_text=_("List of enabled platforms. Leave empty to use widget defaults.")
    )

    # Display options
    show_counts = models.BooleanField(
        default=True,
        verbose_name=_("Show Share Counts"),
        help_text=_("Display number of shares for each platform")
    )

    track_shares = models.BooleanField(
        default=True,
        verbose_name=_("Track Shares"),
        help_text=_("Track share events and award loyalty badges")
    )

    # Timestamps
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Updated By")
    )

    def save(self, *args, **kwargs):
        """Override save to ensure singleton pattern"""
        self.pk = 1
        super().save(*args, **kwargs)
        # Clear settings cache on save
        cache.delete('social_sharing_settings')

    def delete(self, *args, **kwargs):
        """Prevent deletion of settings"""
        pass

    @classmethod
    def get_settings(cls):
        """Get current settings (cached)"""
        settings = cache.get('social_sharing_settings')
        if settings is None:
            settings, created = cls.objects.get_or_create(pk=1)
            cache.set('social_sharing_settings', settings, 3600)  # Cache for 1 hour
        return settings

    def __str__(self):
        return str(_("Social Sharing Settings"))
