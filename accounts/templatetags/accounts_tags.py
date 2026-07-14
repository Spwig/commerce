"""
Template tags for accounts app.
"""

from allauth.account.models import EmailAddress
from django import template

register = template.Library()


@register.simple_tag
def primary_email_verified(user):
    """
    Check if the user's PRIMARY email is verified.

    Unlike allauth's default check which looks at ALL emails,
    this only checks the primary email address.

    Usage:
        {% load accounts_tags %}
        {% primary_email_verified request.user as is_verified %}
        {% if not is_verified %}
            Show verification warning
        {% endif %}
    """
    if not user or not user.is_authenticated:
        return False

    try:
        primary_email = EmailAddress.objects.get(user=user, primary=True)
        return primary_email.verified
    except EmailAddress.DoesNotExist:
        # No primary email set - treat as unverified
        return False
