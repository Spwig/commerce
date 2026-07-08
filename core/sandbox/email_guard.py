"""
Sandbox Email Guard

Enforces email restrictions in sandbox mode by checking recipients
against a whitelist. Non-whitelisted recipients have their emails
logged only (never delivered).

This module is under core/ and will be Cython-compiled in production builds,
making it harder to patch out.
"""

import logging
import re

from core.license import is_sandbox_mode

logger = logging.getLogger(__name__)

# Maximum number of whitelisted email addresses
MAX_WHITELIST_SIZE = 10


def get_email_whitelist():
    """
    Get the sandbox email whitelist from SiteSettings.
    Always includes the admin email automatically.

    Returns:
        set of lowercase email addresses
    """
    try:
        from core.models import SiteSettings
        ss = SiteSettings.objects.first()
        if not ss:
            return set()

        whitelist = set()

        # Admin email is always whitelisted
        if ss.admin_email:
            whitelist.add(ss.admin_email.lower())

        # Add explicitly whitelisted addresses
        if ss.sandbox_email_whitelist:
            for addr in ss.sandbox_email_whitelist:
                if isinstance(addr, str) and addr.strip():
                    whitelist.add(addr.strip().lower())

        return whitelist

    except Exception:
        return set()


def validate_whitelist_entry(email_address):
    """
    Validate that a whitelist entry is an exact email address (no wildcards).

    Args:
        email_address: The email address to validate

    Returns:
        (is_valid, error_message) tuple

    Raises nothing - returns validation result.
    """
    if not email_address or not isinstance(email_address, str):
        return False, "Email address is required."

    email_address = email_address.strip()

    # Reject wildcards and patterns
    if '*' in email_address or '?' in email_address:
        return False, "Wildcards are not allowed. Use exact email addresses only."

    # Reject domain-only patterns like @domain.com
    if email_address.startswith('@'):
        return False, "Domain patterns are not allowed. Use exact email addresses only."

    # Basic email format check
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email_address):
        return False, "Invalid email address format."

    return True, None


def validate_whitelist(whitelist):
    """
    Validate an entire whitelist. Returns errors for any invalid entries.

    Args:
        whitelist: list of email address strings

    Returns:
        (is_valid, errors) where errors is a list of error strings
    """
    if not isinstance(whitelist, list):
        return False, ["Whitelist must be a list of email addresses."]

    if len(whitelist) > MAX_WHITELIST_SIZE:
        return False, [
            f"Maximum {MAX_WHITELIST_SIZE} whitelisted addresses allowed "
            f"(got {len(whitelist)})."
        ]

    errors = []
    for i, addr in enumerate(whitelist):
        is_valid, error = validate_whitelist_entry(addr)
        if not is_valid:
            errors.append(f"Entry {i + 1} ({addr!r}): {error}")

    return len(errors) == 0, errors


def sandbox_filter_recipient(to_email):
    """
    Determine how to handle an email recipient in sandbox mode.

    Args:
        to_email: The intended recipient email address

    Returns:
        (action, to_email) tuple where:
        - action is 'send' (deliver the email) or 'log' (log only, don't send)
        - to_email is the (possibly unchanged) recipient address

    In production mode, always returns ('send', to_email).
    In sandbox mode:
        - Whitelisted address -> ('send', to_email) with email delivered normally
        - Non-whitelisted -> ('log', to_email) recorded but never sent
    """
    if not is_sandbox_mode():
        return 'send', to_email

    whitelist = get_email_whitelist()

    if to_email and to_email.lower() in whitelist:
        logger.info(
            f"[SANDBOX] Email to {to_email} — whitelisted, will deliver"
        )
        return 'send', to_email
    else:
        logger.info(
            f"[SANDBOX] Email to {to_email} — not whitelisted, logging only"
        )
        return 'log', to_email
