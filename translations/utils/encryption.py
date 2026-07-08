"""
Encryption utilities for securing translation provider credentials.

Uses Django's SECRET_KEY for symmetric encryption via Fernet.
Reuses the same pattern as payment_providers and shipping encryption.
"""
import base64
import hashlib
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_fernet_key() -> bytes:
    """
    Derive a Fernet key from Django's SECRET_KEY.

    Returns:
        32-byte Fernet key
    """
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_credentials(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypt credential dictionary for storage.

    Args:
        credentials: Plain credential dictionary

    Returns:
        Dictionary with encrypted values:
        {
            'api_key': {'encrypted': True, 'value': 'gAAAAA...'},
            'region': 'us-east-1'  # Non-secret fields not encrypted
        }
    """
    fernet = Fernet(_get_fernet_key())
    encrypted = {}

    for key, value in credentials.items():
        if isinstance(value, str) and len(value) > 0 and _is_secret_field(key):
            encrypted_value = fernet.encrypt(value.encode()).decode()
            encrypted[key] = {
                'encrypted': True,
                'value': encrypted_value
            }
        else:
            encrypted[key] = value

    return encrypted


def decrypt_credentials(encrypted_credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypt credential dictionary for use.

    Args:
        encrypted_credentials: Encrypted credential dictionary from database

    Returns:
        Plain credential dictionary with decrypted values
    """
    fernet = Fernet(_get_fernet_key())
    decrypted = {}

    for key, value in encrypted_credentials.items():
        if isinstance(value, dict) and value.get('encrypted'):
            try:
                decrypted_value = fernet.decrypt(value['value'].encode()).decode()
                decrypted[key] = decrypted_value
            except Exception as e:
                logger.error(f"Failed to decrypt field '{key}': {e}")
                raise ValueError(f"Failed to decrypt credentials: {e}")
        else:
            decrypted[key] = value

    return decrypted


def _is_secret_field(field_name: str) -> bool:
    """
    Determine if a field should be encrypted based on its name.
    """
    secret_keywords = [
        'key', 'secret', 'token', 'password', 'credential',
        'client_id', 'client_secret', 'api_key', 'access_token',
        'refresh_token', 'private_key',
    ]

    field_lower = field_name.lower()
    return any(keyword in field_lower for keyword in secret_keywords)


def redact_credentials(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Redact sensitive credential values for logging.

    Returns:
        Dictionary with sensitive values masked (e.g., 'sk_***456')
    """
    redacted = {}

    for key, value in credentials.items():
        if isinstance(value, str) and _is_secret_field(key):
            if len(value) > 6:
                redacted[key] = f"{value[:3]}***{value[-3:]}"
            else:
                redacted[key] = "***"
        else:
            redacted[key] = value

    return redacted
