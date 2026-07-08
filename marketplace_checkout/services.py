"""
Marketplace Checkout Services

Handles communication with the upgrade server for purchase token
validation and entitlement grants. Only active on spwig.com (SPWIG_IS_HQ=True).
"""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# Error messages safe to expose to clients (all others are replaced with generic message)
SAFE_TOKEN_ERRORS = frozenset({
    'Invalid purchase token',
    'Purchase token has expired',
    'This purchase token has expired',
    'Purchase token has already been used',
    'This purchase token has already been used',
    'Component not found',
})


def validate_purchase_token(token_uuid: str) -> dict:
    """
    Validate a purchase token with the upgrade server.

    Args:
        token_uuid: UUID string of the purchase token

    Returns:
        dict with component info, merchant details, etc.

    Raises:
        ValueError: If token is invalid, expired, or already used
        requests.RequestException: If upgrade server is unreachable
    """
    try:
        response = requests.get(
            f"{settings.UPGRADE_SERVER_URL}/api/v1/internal/marketplace/"
            f"purchase-token/{token_uuid}/",
            headers={'X-API-KEY': settings.UPGRADE_SERVER_INTERNAL_API_KEY},
            timeout=10,
        )
    except requests.RequestException as e:
        logger.error(f"Upgrade server unreachable for token validation: {e}")
        raise

    try:
        data = response.json()
    except (ValueError, requests.exceptions.JSONDecodeError):
        logger.error(
            f"Upgrade server returned non-JSON response "
            f"(status={response.status_code}): {response.text[:200]}"
        )
        raise ValueError('Unable to validate purchase token')

    if response.status_code != 200:
        error_msg = data.get('error', 'Invalid purchase token')
        if error_msg not in SAFE_TOKEN_ERRORS:
            logger.warning(f"Unexpected token validation error: {error_msg}")
            error_msg = 'Invalid purchase token'
        raise ValueError(error_msg)

    return data


def grant_component_entitlement(order) -> dict:
    """
    Call upgrade server to grant entitlement after successful payment.

    Args:
        order: Order instance with marketplace metadata

    Returns:
        dict with entitlement details from upgrade server

    Raises:
        ValueError: If marketplace metadata is missing
        requests.RequestException: If upgrade server is unreachable
    """
    metadata = order.metadata
    component_slug = metadata.get('component_slug')
    license_key = metadata.get('license_key')

    if not component_slug or not license_key:
        raise ValueError(
            f"Missing marketplace metadata on order {order.order_number}"
        )

    try:
        response = requests.post(
            f"{settings.UPGRADE_SERVER_URL}/api/v1/internal/marketplace/"
            f"entitlements/grant/",
            json={
                'component_slug': component_slug,
                'license_key': license_key,
                'order_reference': order.order_number,
            },
            headers={'X-API-KEY': settings.UPGRADE_SERVER_INTERNAL_API_KEY},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(
            f"Upgrade server error granting entitlement for "
            f"order {order.order_number}: {e}"
        )
        raise

    try:
        result = response.json()
    except (ValueError, requests.exceptions.JSONDecodeError):
        logger.error(
            f"Upgrade server returned non-JSON for entitlement grant "
            f"(status={response.status_code}): {response.text[:200]}"
        )
        raise ValueError('Entitlement grant returned invalid response')

    logger.info(
        f"Granted entitlement for component={component_slug} "
        f"order={order.order_number}"
    )
    return result
