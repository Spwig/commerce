"""
POS License validation.

Checks whether a valid POS license is activated for this installation.
Uses UpdateServerConfig to store the POS license key and validation state,
and validates against the Spwig update server's validate-pos endpoint.

Key behaviors:
- 24-hour cache to avoid repeated DB lookups
- Validates against update server on cache miss
- 14-day grace period after expiration
- Fails CLOSED on errors (returns False) — never allow unvalidated access
"""
import logging
from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

POS_LICENSE_CACHE_KEY = 'pos_license_valid'
POS_LICENSE_CACHE_TIMEOUT = 86400  # 24 hours
POS_GRACE_PERIOD_DAYS = 14


def pos_license_is_valid():
    """
    Check if a valid POS license is active.

    Returns True if:
    - A POS license key is configured and validated
    - The license hasn't expired (or is within the 14-day grace period)

    Returns False if:
    - No POS license configured
    - License expired beyond grace period
    - License revoked
    - Validation fails (fail closed)
    """
    # Community edition: POS is a paid module and never unlocks under Community.
    # The admin surfaces an "Upgrade to enable POS" CTA instead.
    try:
        from core.license import get_license_manager
        if get_license_manager().is_community():
            cache.set(POS_LICENSE_CACHE_KEY, False, POS_LICENSE_CACHE_TIMEOUT)
            return False
    except Exception:
        pass

    # Sandbox/development mode: POS works without a license (with sandbox indicators).
    # Applies only to explicit dev/staging licences, not to a missing licence file.
    try:
        from core.license import is_sandbox_mode
        if is_sandbox_mode():
            cache.set(POS_LICENSE_CACHE_KEY, True, POS_LICENSE_CACHE_TIMEOUT)
            return True
    except Exception:
        pass

    # Check cache first
    cached = cache.get(POS_LICENSE_CACHE_KEY)
    if cached is not None:
        return cached

    try:
        from component_updates.models import UpdateServerConfig
        config = UpdateServerConfig.get_instance()

        pos_license_key = config.pos_license_key
        if not pos_license_key:
            # Also check legacy location in SiteSettings
            try:
                from core.models import SiteSettings
                site_settings = SiteSettings.objects.first()
                if site_settings:
                    pos_license_key = (site_settings.extra_settings or {}).get('pos_license_key', '')
                    if pos_license_key:
                        # Migrate to proper field
                        config.pos_license_key = pos_license_key
                        config.save(update_fields=['pos_license_key'])
            except Exception:
                pass

        if not pos_license_key:
            config.pos_license_status = 'not_configured'
            config.save(update_fields=['pos_license_status'])
            cache.set(POS_LICENSE_CACHE_KEY, False, POS_LICENSE_CACHE_TIMEOUT)
            return False

        # Check local validation state first
        is_valid = _check_local_validity(config)

        # If locally valid and validated recently (< 24h), trust local state
        if is_valid and config.pos_license_validated_at:
            hours_since = (timezone.now() - config.pos_license_validated_at).total_seconds() / 3600
            if hours_since < 24:
                cache.set(POS_LICENSE_CACHE_KEY, True, POS_LICENSE_CACHE_TIMEOUT)
                return True

        # Validate against update server
        server_result = _validate_against_server(config)

        if server_result is not None:
            cache.set(POS_LICENSE_CACHE_KEY, server_result, POS_LICENSE_CACHE_TIMEOUT)
            return server_result

        # Server unreachable — trust local state if validated within 7 days
        if config.pos_license_validated_at:
            days_since = (timezone.now() - config.pos_license_validated_at).days
            if days_since < 7 and config.pos_license_status in ('active', 'grace'):
                cache.set(POS_LICENSE_CACHE_KEY, True, POS_LICENSE_CACHE_TIMEOUT)
                return True

        # Fail closed: can't validate, no recent local validation
        cache.set(POS_LICENSE_CACHE_KEY, False, POS_LICENSE_CACHE_TIMEOUT)
        return False

    except Exception as e:
        logger.error("POS license check failed: %s", e)
        # Fail closed
        cache.set(POS_LICENSE_CACHE_KEY, False, POS_LICENSE_CACHE_TIMEOUT)
        return False


def _check_local_validity(config):
    """Check local POS license validity based on stored state."""
    if config.pos_license_status == 'active':
        if config.pos_license_expires_at and config.pos_license_expires_at < timezone.now():
            # Expired — enter grace period
            config.pos_license_status = 'grace'
            config.save(update_fields=['pos_license_status'])
            return True  # Grace period just started
        return True

    if config.pos_license_status == 'grace':
        if config.pos_license_expires_at:
            grace_end = config.pos_license_expires_at + timedelta(days=POS_GRACE_PERIOD_DAYS)
            if timezone.now() < grace_end:
                return True  # Still in grace period
            # Grace period expired
            config.pos_license_status = 'expired'
            config.save(update_fields=['pos_license_status'])
        return False

    return False


def _validate_against_server(config):
    """
    Validate POS license key against the update server.

    Returns True/False on success, None if server is unreachable.
    """
    try:
        import requests

        response = requests.post(
            f"{config.server_url.rstrip('/')}/api/v1/licenses/validate-pos/",
            json={
                'license_key': config.pos_license_key,
                'installation_uuid': str(config.installation_uuid),
            },
            timeout=10,
            headers={'Content-Type': 'application/json'},
        )

        if response.status_code == 200:
            data = response.json()
            is_valid = data.get('valid', False)
            expires_at = data.get('expires_at')
            status = data.get('status', 'active')

            if is_valid:
                config.pos_license_status = 'active'
                config.pos_license_validated_at = timezone.now()
                if expires_at:
                    from django.utils.dateparse import parse_datetime
                    parsed = parse_datetime(expires_at)
                    if parsed is None and expires_at.endswith('Z'):
                        # Handle malformed ISO strings like "...+00:00Z"
                        parsed = parse_datetime(expires_at.rstrip('Z'))
                    config.pos_license_expires_at = parsed
                config.save(update_fields=[
                    'pos_license_status', 'pos_license_validated_at',
                    'pos_license_expires_at',
                ])
                return True
            else:
                # Server says invalid
                reason = data.get('reason', 'unknown')
                logger.warning(f"POS license invalid: {reason}")
                if status == 'expired' and config.pos_license_expires_at:
                    grace_end = config.pos_license_expires_at + timedelta(days=POS_GRACE_PERIOD_DAYS)
                    if timezone.now() < grace_end:
                        config.pos_license_status = 'grace'
                        config.save(update_fields=['pos_license_status'])
                        return True
                config.pos_license_status = status if status in ('expired', 'grace') else 'expired'
                config.save(update_fields=['pos_license_status'])
                return False

        elif response.status_code == 404:
            # License key not found on server
            logger.warning("POS license key not found on update server")
            config.pos_license_status = 'expired'
            config.save(update_fields=['pos_license_status'])
            return False

        else:
            # Server error — return None to fall back to local state
            logger.warning(f"Update server returned {response.status_code} for POS validation")
            return None

    except requests.exceptions.RequestException as e:
        logger.warning(f"Cannot reach update server for POS validation: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error validating POS license: {e}")
        return None


def clear_pos_license_cache():
    """Clear the POS license cache to force re-validation."""
    cache.delete(POS_LICENSE_CACHE_KEY)


def get_pos_license_status():
    """
    Get detailed POS license status.

    Returns dict with:
    - valid: bool
    - license_key: str or None (masked)
    - status: 'active' | 'grace' | 'expired' | 'not_configured'
    - expires_at: datetime or None
    - grace_period_ends: datetime or None
    - days_remaining: int or None
    """
    result = {
        'valid': False,
        'license_key': None,
        'status': 'not_configured',
        'expires_at': None,
        'grace_period_ends': None,
        'days_remaining': None,
    }

    try:
        from component_updates.models import UpdateServerConfig
        config = UpdateServerConfig.get_instance()

        if config.pos_license_key:
            # Mask the key for display: POS-XXXX-****-****-XXXX
            key = config.pos_license_key
            if len(key) > 12:
                result['license_key'] = f"{key[:8]}{'*' * (len(key) - 12)}{key[-4:]}"
            else:
                result['license_key'] = key

            result['status'] = config.pos_license_status
            result['valid'] = config.pos_license_status in ('active', 'grace')

            if config.pos_license_expires_at:
                result['expires_at'] = config.pos_license_expires_at
                grace_end = config.pos_license_expires_at + timedelta(days=POS_GRACE_PERIOD_DAYS)
                result['grace_period_ends'] = grace_end

                if config.pos_license_status == 'active':
                    days = (config.pos_license_expires_at - timezone.now()).days
                    result['days_remaining'] = max(0, days)
                elif config.pos_license_status == 'grace':
                    days = (grace_end - timezone.now()).days
                    result['days_remaining'] = max(0, days)

    except Exception as e:
        logger.warning("POS license status check failed: %s", e)

    return result


def activate_pos_license(license_key: str) -> dict:
    """
    Activate a POS license key.

    Validates format, then validates against the update server.

    Args:
        license_key: POS license key (POS-XXXX-XXXX-XXXX-XXXX format)

    Returns:
        dict with 'success', 'message', and optionally 'status', 'expires_at'
    """
    import re

    # Validate format
    if not re.match(r'^POS-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$', license_key):
        return {
            'success': False,
            'message': 'Invalid license key format. Expected: POS-XXXX-XXXX-XXXX-XXXX',
        }

    try:
        from component_updates.models import UpdateServerConfig
        config = UpdateServerConfig.get_instance()

        # Store the key
        config.pos_license_key = license_key
        config.save(update_fields=['pos_license_key'])

        # Validate against server
        result = _validate_against_server(config)

        if result is True:
            clear_pos_license_cache()
            return {
                'success': True,
                'message': 'POS license activated successfully.',
                'status': config.pos_license_status,
                'expires_at': config.pos_license_expires_at.isoformat() if config.pos_license_expires_at else None,
            }
        elif result is False:
            # Invalid key — remove it
            config.pos_license_key = ''
            config.pos_license_status = 'not_configured'
            config.save(update_fields=['pos_license_key', 'pos_license_status'])
            clear_pos_license_cache()
            return {
                'success': False,
                'message': 'License key is invalid or expired. Please check your key and try again.',
            }
        else:
            # Server unreachable — keep key, set validated_at so local trust window works
            config.pos_license_status = 'active'
            config.pos_license_validated_at = timezone.now()
            config.save(update_fields=['pos_license_status', 'pos_license_validated_at'])
            clear_pos_license_cache()
            return {
                'success': True,
                'message': 'License key saved. Could not reach update server for validation — will retry automatically.',
                'status': 'pending_validation',
            }

    except Exception as e:
        logger.error(f"POS license activation failed: {e}")
        return {
            'success': False,
            'message': f'Activation failed: {str(e)}',
        }
