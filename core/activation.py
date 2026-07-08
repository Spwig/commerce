"""
Platform Activation Service

Shared logic for activating a Spwig installation using a setup token.
Used by both the /activate/ web view and the activate_with_token management command.

Flow:
1. Validate setup token against update server (POST /api/v1/setup-tokens/validate/)
2. Extract license_key from validated token
3. Activate license via update server (POST /api/v1/licenses/activate/) with challenge-response
4. Verify license signature locally
5. Write license.json to disk
6. Store license_key in UpdateServerConfig
7. Create superuser from token data
8. Clear caches so middleware stops redirecting
"""

import json
import os
import secrets
import hmac
import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests as http_requests
from django.conf import settings
from django.core.cache import cache

import core
from core.license import get_license_manager, reload_license_manager

logger = logging.getLogger(__name__)


@dataclass
class ActivationResult:
    """Result of an activation attempt."""
    success: bool
    error: Optional[str] = None
    admin_username: Optional[str] = None
    admin_password: Optional[str] = None
    license_type: Optional[str] = None
    owner_name: Optional[str] = None


def validate_setup_token(token_str: str) -> dict:
    """
    Validate a setup token against the update server.

    Args:
        token_str: The JWT setup token string

    Returns:
        dict with keys: valid, license_key, email, owner_name, domain, etc.

    Raises:
        ActivationError on network or validation failure
    """
    from component_updates.models import UpdateServerConfig

    update_config = UpdateServerConfig.get_instance()
    validate_url = f"{update_config.server_url}/api/v1/setup-tokens/validate/"

    try:
        response = http_requests.post(
            validate_url,
            json={'token': token_str},
            timeout=30
        )
    except http_requests.exceptions.Timeout:
        raise ActivationError("Connection to update server timed out. Please try again.")
    except http_requests.exceptions.ConnectionError:
        raise ActivationError(
            "Could not connect to update server. Please check your internet connection."
        )

    if response.status_code != 200:
        error_data = _safe_json(response)
        raise ActivationError(
            error_data.get('reason', error_data.get('error', 'Token validation failed'))
        )

    data = response.json()
    if not data.get('valid'):
        raise ActivationError(data.get('reason', 'Invalid setup token'))

    return data


def activate_license(license_key: str, domain: str, setup_token_id: str = '') -> dict:
    """
    Activate a license via the update server using challenge-response.

    Reuses the same pattern as core/admin.py:activate_license_view.

    Args:
        license_key: The license key to activate
        domain: The domain this installation is running on
        setup_token_id: Optional setup token UUID for provenance tracking

    Returns:
        dict with license data and signature

    Raises:
        ActivationError on failure
    """
    from component_updates.models import UpdateServerConfig

    update_config = UpdateServerConfig.get_instance()
    installation_uuid = str(update_config.installation_uuid)

    # Generate random challenge
    challenge = secrets.token_urlsafe(32)
    platform_version = core.__version__

    activation_url = f"{update_config.server_url}/api/v1/licenses/activate/"

    payload = {
        'license_key': license_key,
        'installation_uuid': installation_uuid,
        'domain': domain,
        'platform_version': platform_version,
        'environment_type': 'production',
        'challenge': challenge,
    }

    # Include setup_token_id for provenance tracking (ignored by old servers)
    if setup_token_id:
        payload['setup_token_id'] = setup_token_id

    try:
        response = http_requests.post(activation_url, json=payload, timeout=30)
    except http_requests.exceptions.Timeout:
        raise ActivationError("Connection to update server timed out. Please try again.")
    except http_requests.exceptions.ConnectionError:
        raise ActivationError(
            "Could not connect to update server. Please check your internet connection."
        )

    if response.status_code != 200:
        error_data = _safe_json(response)
        error_msg = error_data.get('message', error_data.get('error', 'Activation failed'))
        raise ActivationError(f"Activation failed: {error_msg}")

    activation_data = response.json()

    # Verify challenge response (prevents MITM)
    expected_response = hmac.new(
        license_key.encode(),
        (challenge + installation_uuid).encode(),
        hashlib.sha256
    ).hexdigest()

    received_response = activation_data.get('challenge_response', '')
    if received_response != expected_response:
        raise ActivationError("Challenge verification failed. Possible security issue.")

    # Build license data object
    license_data = {
        'license': activation_data['license'],
        'signature': activation_data['signature'],
    }

    # Verify signature locally
    license_manager = get_license_manager()
    if not license_manager.verify_signature(license_data):
        raise ActivationError("License signature verification failed.")

    return license_data


def write_license_file(license_data: dict) -> Path:
    """Write license data to the license file path."""
    license_manager = get_license_manager()
    license_path = Path(license_manager.license_path)
    license_path.parent.mkdir(parents=True, exist_ok=True)

    with open(license_path, 'w') as f:
        json.dump(license_data, f, indent=2)

    return license_path


def create_admin_user(email: str, owner_name: str) -> tuple:
    """
    Create a superuser account for the merchant.

    Returns:
        tuple of (username, password)
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Generate username from email (before @)
    username = email.split('@')[0].lower()
    # Ensure it's unique
    base_username = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # Generate a random password
    password = secrets.token_urlsafe(12)

    # Split owner_name into first/last
    name_parts = owner_name.strip().split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    logger.info(f"Created admin user: {username}")
    return username, password


def activate_with_token(token_str: str, domain: str = 'localhost') -> ActivationResult:
    """
    Full activation flow: validate token → activate license → create admin user.

    Args:
        token_str: The JWT setup token
        domain: The domain this installation runs on

    Returns:
        ActivationResult with success status and admin credentials
    """
    try:
        # Step 1: Validate the setup token
        token_data = validate_setup_token(token_str.strip())

        license_key = token_data.get('license_key')
        email = token_data.get('email', '')
        owner_name = token_data.get('owner_name', '')
        setup_token_id = token_data.get('token_id', '')

        if not license_key:
            return ActivationResult(success=False, error="Setup token does not contain a license key.")

        # Step 2: Activate the license (pass setup_token_id for provenance tracking)
        license_data = activate_license(license_key, domain, setup_token_id=setup_token_id)

        # Step 3: Write license file
        write_license_file(license_data)

        # Step 4: Store license key in UpdateServerConfig
        from component_updates.models import UpdateServerConfig
        update_config = UpdateServerConfig.get_instance()
        update_config.license_key = license_key
        update_config.jwt_token = token_str.strip()
        update_config.save()

        # Step 5: Reload license manager
        reload_license_manager()

        # Step 6: Clear activation cache
        from core.middleware.activation import ACTIVATION_CACHE_KEY
        cache.set(ACTIVATION_CACHE_KEY, True, 60 * 60 * 24)

        # Step 7: Create admin user (skip for hosted — merchant-ctl handles it
        # with the merchant's actual password from checkout)
        admin_username = None
        admin_password = None
        if email and not os.environ.get('SPWIG_HOSTED'):
            try:
                admin_username, admin_password = create_admin_user(email, owner_name)
            except Exception as e:
                logger.warning(f"Could not create admin user: {e}")
                # Don't fail activation because of user creation issues

        # Step 8: Store token-derived settings for setup wizard
        _store_setup_defaults(token_data)

        license_info = license_data.get('license', {})
        return ActivationResult(
            success=True,
            admin_username=admin_username,
            admin_password=admin_password,
            license_type=license_info.get('license_type', 'unknown'),
            owner_name=owner_name,
        )

    except ActivationError as e:
        logger.error(f"Activation failed: {e}")
        return ActivationResult(success=False, error=str(e))
    except Exception as e:
        logger.exception(f"Unexpected activation error: {e}")
        return ActivationResult(success=False, error=f"Unexpected error: {str(e)}")


def _store_setup_defaults(token_data: dict):
    """Store token-derived settings so the setup wizard can pre-populate fields."""
    try:
        from core.models import SiteSettings
        from django.contrib.sites.models import Site

        site_settings = SiteSettings.get_settings()
        if not site_settings:
            return

        update_fields = []

        # site_name: use token's site_name, fall back to "{owner_name}'s Store"
        token_site_name = token_data.get('site_name', '').strip()
        if token_site_name and site_settings.site_name == 'My E-commerce Store':
            site_settings.site_name = token_site_name
            update_fields.append('site_name')
        elif token_data.get('owner_name') and site_settings.site_name == 'My E-commerce Store':
            site_settings.site_name = f"{token_data['owner_name']}'s Store"
            update_fields.append('site_name')

        # admin_email
        email = token_data.get('email', '').strip()
        if email and not site_settings.admin_email:
            site_settings.admin_email = email
            update_fields.append('admin_email')

        # site_url from domain
        domain = token_data.get('domain', '').strip()
        if domain and site_settings.site_url == 'https://example.com':
            site_settings.site_url = f"https://{domain}"
            update_fields.append('site_url')

        # default_language from shop_language
        shop_lang = token_data.get('shop_language', '').strip()
        if shop_lang and site_settings.default_language == 'en':
            site_settings.default_language = shop_lang
            update_fields.append('default_language')

        if update_fields:
            site_settings.save(update_fields=update_fields)

        # Update Django Site object (used by allauth) with domain and name
        if domain:
            site = Site.objects.get(pk=1)
            changed = False
            if site.domain == 'example.com':
                site.domain = domain
                changed = True
            if site.name == 'My E-commerce Store' and (token_site_name or token_data.get('owner_name')):
                site.name = token_site_name or f"{token_data['owner_name']}'s Store"
                changed = True
            if changed:
                site.save()

        # For hosted instances: configure SSL as managed externally (Cloudflare)
        if os.environ.get('SPWIG_HOSTED'):
            try:
                from domain_ssl.models import DomainConfiguration
                config = DomainConfiguration.get_instance()
                if config.ssl_mode == DomainConfiguration.SSLMode.NONE:
                    config.ssl_mode = DomainConfiguration.SSLMode.MANAGED_EXTERNALLY
                    config.cert_domain = '*.myspwig.com'
                    config.cert_issuer = 'Cloudflare Origin CA'
                    config.status = DomainConfiguration.Status.IDLE
                    config.last_error = ''
                    if domain:
                        config.domain = domain
                    config.save(update_fields=[
                        'ssl_mode', 'cert_domain', 'cert_issuer',
                        'status', 'last_error', 'domain',
                    ])
                    logger.info('SSL configured as managed externally (hosted)')
            except Exception as ssl_err:
                logger.debug(f"Could not configure hosted SSL: {ssl_err}")

    except Exception as e:
        logger.debug(f"Could not store setup defaults: {e}")


def _safe_json(response) -> dict:
    """Safely parse JSON from a response, returning empty dict on failure."""
    try:
        if response.headers.get('content-type', '').startswith('application/json'):
            return response.json()
    except Exception:
        pass
    return {}


class ActivationError(Exception):
    """Raised when activation fails."""
    pass
