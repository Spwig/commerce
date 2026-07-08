"""
API Token Generation and Validation Utilities

This module provides utilities for generating secure API tokens
and validating them against database records.
"""
import secrets
import string
from django.utils import timezone
from core.models import APIToken


def generate_secure_token(length=64):
    """
    Generate a cryptographically secure random token

    Args:
        length: Length of the token (default: 64 characters)

    Returns:
        str: Random token string containing letters and digits
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_api_token(name, token_type='custom', description='', created_by=None, expires_at=None):
    """
    Create a new API token

    Args:
        name: Descriptive name for the token
        token_type: Type of token (help_system, integration, webhook, custom)
        description: Optional description
        created_by: User creating the token
        expires_at: Optional expiration datetime

    Returns:
        APIToken: The created token object
    """
    token_string = generate_secure_token()

    api_token = APIToken.objects.create(
        name=name,
        token=token_string,
        token_type=token_type,
        description=description,
        created_by=created_by,
        expires_at=expires_at,
        is_active=True
    )

    return api_token


def validate_api_token(token_string, token_type=None, record_usage=True, ip_address=None):
    """
    Validate an API token and optionally record its usage

    Args:
        token_string: The token string to validate
        token_type: Optional token type to filter by
        record_usage: Whether to record this usage (default: True)
        ip_address: Optional IP address for usage tracking

    Returns:
        APIToken or None: The token object if valid, None otherwise
    """
    if not token_string:
        return None

    try:
        # Build query
        query = APIToken.objects.filter(token=token_string, is_active=True)

        if token_type:
            query = query.filter(token_type=token_type)

        api_token = query.first()

        if not api_token:
            return None

        # Check if expired
        if api_token.is_expired:
            return None

        # Check IP restrictions if configured
        if api_token.allowed_ips and ip_address:
            if ip_address not in api_token.allowed_ips:
                return None

        # Record usage
        if record_usage:
            api_token.record_usage(ip_address=ip_address)

        return api_token

    except Exception:
        return None


def revoke_token(token_id):
    """
    Revoke (deactivate) an API token

    Args:
        token_id: ID of the token to revoke

    Returns:
        bool: True if successfully revoked, False otherwise
    """
    try:
        token = APIToken.objects.get(id=token_id)
        token.is_active = False
        token.save(update_fields=['is_active'])
        return True
    except APIToken.DoesNotExist:
        return False


def get_active_tokens_by_type(token_type):
    """
    Get all active tokens of a specific type

    Args:
        token_type: Type of tokens to retrieve

    Returns:
        QuerySet: Active tokens of the specified type
    """
    return APIToken.objects.filter(
        token_type=token_type,
        is_active=True
    ).exclude(
        expires_at__lt=timezone.now()
    )
