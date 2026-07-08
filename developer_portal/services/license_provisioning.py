"""
Developer License Provisioning Service

Handles communication with the update server to create developer licenses
and manage setup tokens. Only active on spwig.com (SPWIG_IS_HQ=True).

Uses existing update server endpoints:
- POST /api/v1/internal/licenses/        — create license
- POST /api/v1/setup-tokens/             — create setup token
- POST /api/v1/setup-tokens/{id}/regenerate/ — regenerate expired token
"""

import logging

import requests
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)


def _api_headers():
    return {'X-API-KEY': settings.UPGRADE_SERVER_INTERNAL_API_KEY}


def provision_dev_license(license_request) -> dict:
    """
    Create a developer license and setup token via the update server.

    Makes two sequential API calls:
    1. POST /api/v1/internal/licenses/ — creates the license record
    2. POST /api/v1/setup-tokens/ — creates a JWT setup token for it

    Updates the license_request in-place on success.

    Args:
        license_request: DeveloperLicenseRequest instance

    Returns:
        dict with license_key, setup_token, setup_token_id, etc.

    Raises:
        ValueError: Business logic error from the update server
        requests.RequestException: Network error
    """
    profile = license_request.developer
    user = profile.user
    owner_name = profile.company_name or profile.display_name

    # --- Step 1: Create the license ---
    license_payload = {
        'owner_name': owner_name,
        'owner_email': user.email,
        'license_type': 'dev',
        'product_type': 'bundle',
        'max_installations': 1,
        'allowed_channels': ['stable', 'beta', 'dev'],
        'metadata': {
            'developer_slug': profile.developer_slug,
            'company_name': profile.company_name,
            'country': str(profile.country) if profile.country else '',
            'license_request_id': str(license_request.id),
            'is_paid': not license_request.is_free,
        },
    }

    license_url = f"{settings.UPGRADE_SERVER_URL}/api/v1/internal/licenses/"

    try:
        resp = requests.post(
            license_url,
            json=license_payload,
            headers=_api_headers(),
            timeout=15,
        )
    except requests.RequestException as e:
        logger.error(f"Update server unreachable for license creation: {e}")
        raise

    if resp.status_code == 409:
        raise ValueError('A license with this key already exists')

    if resp.status_code != 201:
        _log_api_error('license creation', resp)
        raise ValueError('Unable to create developer license')

    license_data = resp.json()
    license_key = license_data['license_key']

    # Save license_key immediately in case step 2 fails
    license_request.license_key = license_key
    license_request.save(update_fields=['license_key'])

    # --- Step 2: Create setup token ---
    token_payload = {
        'license_key': license_key,
        'email': user.email,
        'owner_name': owner_name,
        'company_name': profile.company_name,
    }

    token_url = f"{settings.UPGRADE_SERVER_URL}/api/v1/setup-tokens/"

    try:
        resp = requests.post(
            token_url,
            json=token_payload,
            headers=_api_headers(),
            timeout=15,
        )
    except requests.RequestException as e:
        logger.error(
            f"License {license_key} created but setup token creation failed: {e}. "
            f"Admin can retry via the portal."
        )
        raise

    if resp.status_code != 201:
        _log_api_error('setup token creation', resp)
        raise ValueError(
            'License was created but setup token generation failed. '
            'Please try regenerating the token from your license page.'
        )

    token_data = resp.json()

    # Save everything
    license_request.setup_token = token_data.get('token', '')
    license_request.setup_token_id = token_data.get('token_id')
    license_request.status = license_request.Status.APPROVED
    license_request.reviewed_at = timezone.now()

    token_expires = token_data.get('expires_at')
    if token_expires:
        license_request.setup_token_expires_at = parse_datetime(token_expires)

    license_request.save(update_fields=[
        'license_key', 'setup_token', 'setup_token_id',
        'setup_token_expires_at', 'status', 'reviewed_at',
    ])

    logger.info(
        f"Provisioned dev license for developer={profile.developer_slug} "
        f"license_key={license_key} is_free={license_request.is_free}"
    )

    return {
        'license_key': license_key,
        'setup_token': token_data.get('token', ''),
        'setup_token_id': str(token_data.get('token_id', '')),
        'setup_token_expires_at': token_expires,
    }


def regenerate_setup_token(license_request) -> dict:
    """
    Regenerate an expired setup token for an existing developer license.

    Calls POST /api/v1/setup-tokens/{token_id}/regenerate/ on the update server.
    The old token is revoked and a new one is created with the same details.

    Args:
        license_request: DeveloperLicenseRequest with setup_token_id set

    Returns:
        dict with setup_token, setup_token_id, setup_token_expires_at

    Raises:
        ValueError: If token_id is missing or license already activated
        requests.RequestException: Network error
    """
    if not license_request.setup_token_id:
        raise ValueError(
            'No setup token ID available for regeneration. '
            'Please contact support.'
        )

    token_id = license_request.setup_token_id
    url = f"{settings.UPGRADE_SERVER_URL}/api/v1/setup-tokens/{token_id}/regenerate/"

    try:
        resp = requests.post(
            url,
            headers=_api_headers(),
            timeout=15,
        )
    except requests.RequestException as e:
        logger.error(f"Update server unreachable for token regeneration: {e}")
        raise

    if resp.status_code == 404:
        raise ValueError(
            'Setup token not found on the update server. '
            'Please contact support.'
        )

    if resp.status_code != 200:
        _log_api_error('token regeneration', resp)
        raise ValueError('Unable to regenerate setup token')

    data = resp.json()

    # Update with the new token details
    license_request.setup_token = data.get('token', '')
    license_request.setup_token_id = data.get('token_id')

    token_expires = data.get('expires_at')
    if token_expires:
        license_request.setup_token_expires_at = parse_datetime(token_expires)

    license_request.save(update_fields=[
        'setup_token', 'setup_token_id', 'setup_token_expires_at',
    ])

    logger.info(
        f"Regenerated setup token for license_key={license_request.license_key} "
        f"developer={license_request.developer.developer_slug} "
        f"new_token_id={data.get('token_id')}"
    )

    return data


def provision_paid_dev_license(order) -> None:
    """
    Provision a developer license after a successful Airwallex payment.

    Called from the post-payment hook in PaymentOrchestrationService.

    Args:
        order: Order instance with dev_license_purchase metadata
    """
    from developer_portal.models import DeveloperProfile, DeveloperLicenseRequest
    from developer_portal.services.email_service import DeveloperEmailService

    developer_profile_id = order.metadata.get('developer_profile_id')
    if not developer_profile_id:
        logger.error(f"No developer_profile_id in order {order.order_number} metadata")
        return

    try:
        profile = DeveloperProfile.objects.get(id=developer_profile_id)
    except DeveloperProfile.DoesNotExist:
        logger.error(
            f"DeveloperProfile {developer_profile_id} not found "
            f"for order {order.order_number}"
        )
        return

    # Create the license request record
    license_request = DeveloperLicenseRequest.objects.create(
        developer=profile,
        is_free=False,
        license_type=DeveloperLicenseRequest.LicenseType.BOTH,
        reason=f'Paid additional developer license (Order {order.order_number})',
        order=order,
    )

    # Provision via update server
    try:
        provision_dev_license(license_request)
    except Exception as e:
        logger.error(
            f"Failed to provision paid dev license for "
            f"developer={profile.developer_slug} order={order.order_number}: {e}"
        )
        # License request stays as pending — admin can retry manually
        return

    # Send confirmation email
    try:
        DeveloperEmailService.send_license_approved(license_request)
    except Exception as e:
        logger.error(f"Failed to send license approval email: {e}")


def _log_api_error(operation, response):
    """Log a non-success API response with details."""
    try:
        body = response.json()
        error = body.get('error', '')
        message = body.get('message', '')
        logger.error(
            f"Update server {operation} failed "
            f"(status={response.status_code}): error={error} message={message}"
        )
    except (ValueError, requests.exceptions.JSONDecodeError):
        logger.error(
            f"Update server {operation} returned non-JSON "
            f"(status={response.status_code}): {response.text[:200]}"
        )
