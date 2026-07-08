"""
License Grace Period System

Tracks installation age and determines whether the grace period
for license activation has expired. Uses progressive lockout:

- Days 0-14:  Grace period (sandbox mode, test payments OK)
- Days 15-21: Warning phase (same as grace but non-dismissible banner)
- Day 22+:    Full lockout (storefront down, admin restricted)
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

GRACE_PERIOD_DAYS = 14
WARNING_PHASE_DAYS = 7  # Additional days 15-21 after grace period
TOTAL_DAYS_BEFORE_LOCKOUT = GRACE_PERIOD_DAYS + WARNING_PHASE_DAYS  # 21

CACHE_KEY = 'license_grace_period_status'
CACHE_TTL = 60  # seconds


@dataclass(frozen=True)
class GracePeriodStatus:
    """Immutable status of the license grace period."""
    has_valid_license: bool
    is_in_grace_period: bool
    is_in_warning_phase: bool
    is_locked_out: bool
    days_remaining: int  # Days until lockout (0 if locked out)
    days_elapsed: int  # Days since installation
    installed_at: Optional[datetime]
    fingerprint_valid: bool

    @property
    def enforcement_state(self) -> str:
        """Return the enforcement state string."""
        if self.has_valid_license:
            return 'licensed'
        if self.is_locked_out:
            return 'locked_out'
        if self.is_in_warning_phase:
            return 'warning_phase'
        if self.is_in_grace_period:
            return 'grace_period'
        return 'locked_out'


def get_grace_period_status() -> GracePeriodStatus:
    """
    Get the current grace period status.

    Cached for 60 seconds to avoid repeated DB hits.
    """
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    status = _compute_grace_period_status()
    cache.set(CACHE_KEY, status, CACHE_TTL)
    return status


def clear_grace_period_cache():
    """Clear the grace period cache (use after license changes)."""
    cache.delete(CACHE_KEY)


def _compute_grace_period_status() -> GracePeriodStatus:
    """Compute the actual grace period status from DB state."""
    from core.license import get_license_manager

    license_manager = get_license_manager()
    has_valid_license = license_manager.is_valid()

    # If licensed, grace period is irrelevant
    if has_valid_license:
        return GracePeriodStatus(
            has_valid_license=True,
            is_in_grace_period=False,
            is_in_warning_phase=False,
            is_locked_out=False,
            days_remaining=0,
            days_elapsed=0,
            installed_at=None,
            fingerprint_valid=True,
        )

    # Get installation date
    try:
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()

        # Stamp installation date if not set (first access)
        if not settings.installed_at:
            settings.stamp_installation_date()
            # Refresh from DB
            settings.refresh_from_db()

        installed_at = settings.installed_at
        fingerprint_valid = settings.verify_installation_fingerprint()

    except Exception as e:
        logger.error(f"Failed to get installation date: {e}")
        # If we can't determine installation date, assume locked out
        # (fail secure)
        return GracePeriodStatus(
            has_valid_license=False,
            is_in_grace_period=False,
            is_in_warning_phase=False,
            is_locked_out=True,
            days_remaining=0,
            days_elapsed=0,
            installed_at=None,
            fingerprint_valid=False,
        )

    # If fingerprint is invalid (tampered), treat as locked out
    if not fingerprint_valid:
        logger.warning("Installation fingerprint verification failed - treating as locked out")
        return GracePeriodStatus(
            has_valid_license=False,
            is_in_grace_period=False,
            is_in_warning_phase=False,
            is_locked_out=True,
            days_remaining=0,
            days_elapsed=0,
            installed_at=installed_at,
            fingerprint_valid=False,
        )

    # Calculate days elapsed
    now = timezone.now()
    delta = now - installed_at
    days_elapsed = delta.days

    # Determine phase
    if days_elapsed <= GRACE_PERIOD_DAYS:
        # Grace period active (days 0-14)
        days_remaining = TOTAL_DAYS_BEFORE_LOCKOUT - days_elapsed
        return GracePeriodStatus(
            has_valid_license=False,
            is_in_grace_period=True,
            is_in_warning_phase=False,
            is_locked_out=False,
            days_remaining=days_remaining,
            days_elapsed=days_elapsed,
            installed_at=installed_at,
            fingerprint_valid=True,
        )
    elif days_elapsed <= TOTAL_DAYS_BEFORE_LOCKOUT:
        # Warning phase (days 15-21)
        days_remaining = TOTAL_DAYS_BEFORE_LOCKOUT - days_elapsed
        return GracePeriodStatus(
            has_valid_license=False,
            is_in_grace_period=False,
            is_in_warning_phase=True,
            is_locked_out=False,
            days_remaining=days_remaining,
            days_elapsed=days_elapsed,
            installed_at=installed_at,
            fingerprint_valid=True,
        )
    else:
        # Full lockout (day 22+)
        return GracePeriodStatus(
            has_valid_license=False,
            is_in_grace_period=False,
            is_in_warning_phase=False,
            is_locked_out=True,
            days_remaining=0,
            days_elapsed=days_elapsed,
            installed_at=installed_at,
            fingerprint_valid=True,
        )
