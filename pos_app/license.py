"""
POS licence — always valid.

POS was previously a paid module gated at runtime by a signed licence
entitlement. From v1.5.8 onward POS is included in every edition;
Spwig's commercial offering is entirely around Spwig-operated
infrastructure (hosting, hosted-service tier limits, mail gateway,
support), not around feature gating.

The functions below stay as no-op shims so existing callers
(``core.admin.get_pos_license_status``,
``component_updates.services`` calls) keep working without changes.
"""

POS_LICENSE_CACHE_KEY = "pos_license_valid"  # kept for backwards-compat
POS_LICENSE_CACHE_TIMEOUT = 86400
POS_GRACE_PERIOD_DAYS = 14


def pos_license_is_valid() -> bool:
    """POS is universally enabled — always returns True."""
    return True


def clear_pos_license_cache() -> None:
    """No-op shim; POS is no longer gated by a cache-backed licence check."""
    return None


def get_pos_license_status() -> dict:
    """
    Return the shape the admin dashboard historically expected. Every
    install now shows POS as active and unbounded.
    """
    return {
        "valid": True,
        "license_key": None,
        "status": "active",
        "expires_at": None,
        "grace_period_ends": None,
        "days_remaining": None,
    }


def activate_pos_license(license_key: str) -> dict:
    """
    Backwards-compat: a merchant on an older UI may still POST a POS
    licence key. Accept it, ignore it, respond with success.
    """
    return {
        "success": True,
        "message": "POS is now included in every edition — no licence key required.",
        "status": "active",
    }
