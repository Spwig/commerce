"""
Platform Secrets Helper

Provides runtime access to platform secrets stored in the database.
Falls back to environment variables for backwards compatibility during
the transition period or for development environments.

Usage:
    from core.platform_secrets import get_geoip_secret, get_push_secret, get_sso_secret

    # In a service that needs the GeoIP JWT secret:
    jwt_secret = get_geoip_secret()
"""

import logging
from functools import lru_cache
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


def _get_platform_secrets():
    """
    Get PlatformSecrets instance from database.
    Returns None if database not available (e.g., during migrations).
    """
    try:
        from core.models import PlatformSecrets
        return PlatformSecrets.get_secrets()
    except Exception as e:
        # Database might not be available during migrations or early startup
        logger.debug(f"Could not load PlatformSecrets from database: {e}")
        return None


def get_geoip_secret() -> str:
    """
    Get the GeoIP service JWT secret.

    Priority:
    1. PlatformSecrets.geoip_jwt_secret (from database)
    2. settings.GEOIP_JWT_SECRET_KEY (from env)
    3. settings.GEOCODER_JWT_SECRET_KEY (legacy fallback)
    4. Empty string (if nothing configured)
    """
    # Try database first
    secrets = _get_platform_secrets()
    if secrets and secrets.geoip_jwt_secret:
        return secrets.geoip_jwt_secret

    # Fall back to settings/env
    return getattr(settings, 'GEOIP_JWT_SECRET_KEY',
                   getattr(settings, 'GEOCODER_JWT_SECRET_KEY', ''))


def get_push_secret() -> str:
    """
    Get the Push notification service JWT secret.

    Priority:
    1. PlatformSecrets.push_jwt_secret (from database)
    2. settings.PUSH_JWT_SECRET_KEY (from env)
    3. Empty string (if nothing configured)
    """
    # Try database first
    secrets = _get_platform_secrets()
    if secrets and secrets.push_jwt_secret:
        return secrets.push_jwt_secret

    # Fall back to settings/env
    return getattr(settings, 'PUSH_JWT_SECRET_KEY', '')


def get_sso_secret() -> str:
    """
    Get the SSO/Community service JWT secret.

    Priority:
    1. PlatformSecrets.sso_jwt_secret (from database)
    2. settings.SSO_REGISTRATION_SECRET (from env)
    3. Empty string (if nothing configured)
    """
    # Try database first
    secrets = _get_platform_secrets()
    if secrets and secrets.sso_jwt_secret:
        return secrets.sso_jwt_secret

    # Fall back to settings/env
    return getattr(settings, 'SSO_REGISTRATION_SECRET', '')


def get_installation_uuid() -> Optional[str]:
    """
    Get the installation UUID assigned by the license server.

    Returns None if not yet registered with license server.
    """
    secrets = _get_platform_secrets()
    if secrets and secrets.installation_uuid:
        return str(secrets.installation_uuid)
    return None


def is_initialized() -> bool:
    """
    Check if platform secrets have been initialized from the license server.

    Returns True if all service secrets are populated.
    """
    secrets = _get_platform_secrets()
    if not secrets:
        return False
    return secrets.is_initialized


def clear_secret_cache():
    """
    Clear any cached secrets. Call this after fetching new secrets
    from the license server to ensure fresh values are used.
    """
    # Currently no caching, but this provides a hook for future optimization
    pass
