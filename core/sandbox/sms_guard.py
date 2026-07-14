"""
Sandbox SMS Guard

Enforces SMS restrictions in sandbox mode by checking recipients
against a whitelist. Non-whitelisted phone numbers have their messages
logged only (never delivered).

This module is under core/ and will be Cython-compiled in production builds,
making it harder to patch out.
"""

import logging
import re

from core.license import is_sandbox_mode

logger = logging.getLogger(__name__)

# Maximum number of whitelisted phone numbers
MAX_WHITELIST_SIZE = 5


def get_sms_whitelist():
    """
    Get the sandbox SMS whitelist from SiteSettings.

    Returns:
        set of phone number strings (normalized)
    """
    try:
        from core.models import SiteSettings

        ss = SiteSettings.objects.first()
        if not ss:
            return set()

        whitelist = set()

        if ss.sandbox_sms_whitelist:
            for number in ss.sandbox_sms_whitelist:
                if isinstance(number, str) and number.strip():
                    # Normalize: strip whitespace
                    whitelist.add(number.strip())

        return whitelist

    except Exception:
        return set()


def validate_sms_whitelist_entry(phone_number):
    """
    Validate that a whitelist entry is an exact phone number in E.164 format.

    Args:
        phone_number: The phone number to validate

    Returns:
        (is_valid, error_message) tuple
    """
    if not phone_number or not isinstance(phone_number, str):
        return False, "Phone number is required."

    phone_number = phone_number.strip()

    # Reject wildcards and patterns
    if "*" in phone_number or "?" in phone_number:
        return False, "Wildcards are not allowed. Use exact phone numbers only."

    # E.164 format: + followed by 1-15 digits
    if not re.match(r"^\+[1-9]\d{1,14}$", phone_number):
        return False, "Invalid phone number format. Use E.164 format (e.g., +1234567890)."

    return True, None


def validate_sms_whitelist(whitelist):
    """
    Validate an entire SMS whitelist.

    Args:
        whitelist: list of phone number strings

    Returns:
        (is_valid, errors) where errors is a list of error strings
    """
    if not isinstance(whitelist, list):
        return False, ["Whitelist must be a list of phone numbers."]

    if len(whitelist) > MAX_WHITELIST_SIZE:
        return False, [
            f"Maximum {MAX_WHITELIST_SIZE} whitelisted phone numbers allowed "
            f"(got {len(whitelist)})."
        ]

    errors = []
    for i, number in enumerate(whitelist):
        is_valid, error = validate_sms_whitelist_entry(number)
        if not is_valid:
            errors.append(f"Entry {i + 1} ({number!r}): {error}")

    return len(errors) == 0, errors


def sandbox_filter_sms_recipient(phone_number):
    """
    Determine how to handle an SMS recipient in sandbox mode.

    Args:
        phone_number: The intended recipient phone number

    Returns:
        (action, phone_number) tuple where:
        - action is 'send' (deliver the SMS) or 'log' (log only, don't send)
        - phone_number is the (unchanged) recipient number

    In production mode, always returns ('send', phone_number).
    In sandbox mode:
        - Whitelisted number -> ('send', phone_number)
        - Non-whitelisted -> ('log', phone_number)
    """
    if not is_sandbox_mode():
        return "send", phone_number

    whitelist = get_sms_whitelist()

    if phone_number and phone_number.strip() in whitelist:
        logger.info(f"[SANDBOX] SMS to {phone_number} — whitelisted, will deliver")
        return "send", phone_number
    else:
        logger.info(f"[SANDBOX] SMS to {phone_number} — not whitelisted, logging only")
        return "log", phone_number
