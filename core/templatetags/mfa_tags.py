"""
Template tags for Multi-Factor Authentication (MFA) status checks
"""
from django import template
from allauth.mfa.adapter import get_adapter

register = template.Library()


@register.filter(name='mfa_enabled')
def mfa_enabled(user):
    """
    Check if a user has MFA enabled.

    Usage in template:
        {% load mfa_tags %}
        {% if user|mfa_enabled %}
            MFA is enabled
        {% else %}
            MFA is not enabled
        {% endif %}

    Args:
        user: Django User object

    Returns:
        bool: True if user has MFA enabled, False otherwise
    """
    if not user or not user.is_authenticated:
        return False

    try:
        adapter = get_adapter()
        return adapter.is_mfa_enabled(user)
    except Exception:
        # If anything goes wrong, assume MFA is not enabled
        return False
