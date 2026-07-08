"""
Email language resolution utility.

Centralizes the fallback chain for determining which language to use
when sending emails. All email-sending code should use these functions
instead of reading user attributes directly.
"""
import logging

logger = logging.getLogger(__name__)


def get_user_email_language(user) -> str:
    """
    Get the preferred email language for a user.

    Fallback chain:
    1. CommunicationPreference.language_code (explicit user preference)
    2. SiteSettings.default_language (merchant's store default)
    3. 'en' (hardcoded final fallback)

    Args:
        user: Django User instance, or None for guest users

    Returns:
        ISO 639-1 language code string
    """
    if user is None:
        return _get_site_default_language()

    # 1. Try CommunicationPreference.language_code
    try:
        prefs = user.communication_preferences
        if prefs.language_code:
            return prefs.language_code
    except Exception:
        pass

    # 2. Fall back to site default language
    return _get_site_default_language()


def get_order_email_language(order) -> str:
    """
    Get the language for order-related emails.

    Uses the language captured at checkout time (order.language),
    falling back to the user's preference, then site default.

    Args:
        order: Order instance

    Returns:
        ISO 639-1 language code string
    """
    # 1. Try order.language (captured at checkout)
    order_lang = getattr(order, 'language', None)
    if order_lang:
        return order_lang

    # 2. Fall back to user preference
    user = getattr(order, 'user', None)
    return get_user_email_language(user)


def _get_site_default_language() -> str:
    """
    Get the site default language from SiteSettings.

    Returns:
        Language code string, defaults to 'en' if SiteSettings unavailable
    """
    try:
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()
        if settings.default_language:
            return settings.default_language
    except Exception:
        pass
    return 'en'
