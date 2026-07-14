"""
Social Sharing API Serializers
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from social_sharing.models import SocialShare


class TrackShareSerializer(serializers.Serializer):
    """Serializer for tracking social media shares"""

    content_type = serializers.CharField(
        max_length=100,
        required=True,
        help_text=_("Model name (lowercase) - e.g., 'product', 'page', 'post'"),
    )
    object_id = serializers.IntegerField(
        required=True, help_text=_("ID of the content being shared")
    )
    platform = serializers.ChoiceField(
        choices=[c[0] for c in SocialShare.PLATFORM_CHOICES],
        required=True,
        help_text=_("Social media platform"),
    )
    url = serializers.URLField(required=True, help_text=_("Full URL being shared"))
