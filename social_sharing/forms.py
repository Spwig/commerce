"""
Social Sharing Settings Admin Form

Custom form that replaces the raw JSON enabled_platforms field
with a CheckboxSelectMultiple widget for merchant-friendly platform selection.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from social_sharing.models import SocialShare
from social_sharing.settings_models import SocialSharingSettings


class SocialSharingSettingsForm(forms.ModelForm):
    """
    Custom form for SocialSharingSettings admin.

    - Replaces JSONField enabled_platforms with CheckboxSelectMultiple
    - Excludes widget_slug and default_config (internal fields)
    """

    enabled_platforms = forms.MultipleChoiceField(
        required=False,
        choices=SocialShare.PLATFORM_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "social-platform-checkboxes"}),
        label=_("Enabled Platforms"),
        help_text=_(
            "Select which platforms to show. If none selected, all platforms will be shown."
        ),
    )

    class Meta:
        model = SocialSharingSettings
        fields = [
            "enable_on_products",
            "enable_on_categories",
            "enable_on_blog_posts",
            "enable_on_pages",
            "placement_position",
            "enabled_platforms",
            "button_style",
            "button_size",
            "layout_direction",
            "show_title",
            "mobile_visibility",
            "show_counts",
            "track_shares",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.enabled_platforms:
            self.fields["enabled_platforms"].initial = self.instance.enabled_platforms

    def clean_enabled_platforms(self):
        """Return a plain list for JSON storage."""
        return self.cleaned_data.get("enabled_platforms", [])
