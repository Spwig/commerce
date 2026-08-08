"""
Encryption utilities for securing provider credentials.

Uses Django's SECRET_KEY for symmetric encryption via Fernet.
Credentials are encrypted before storing in PaymentProviderAccount.credentials_encrypted.
"""

import base64
import hashlib
import logging
from typing import Any

from cryptography.fernet import Fernet, MultiFernet
from django.conf import settings

logger = logging.getLogger(__name__)


def _derive_fernet_key(secret_key: str) -> bytes:
    """
    Derive a Fernet key from a single secret key string.

    Returns:
        32-byte url-safe base64-encoded Fernet key
    """
    # Use SHA256 to derive a consistent 32-byte key from the secret
    key = hashlib.sha256(secret_key.encode()).digest()
    return base64.urlsafe_b64encode(key)


def _get_fernet_key() -> bytes:
    """
    Derive a Fernet key from Django's current SECRET_KEY.

    Returns:
        32-byte Fernet key
    """
    return _derive_fernet_key(settings.SECRET_KEY)


def _get_multi_fernet() -> MultiFernet:
    """
    Build a MultiFernet from the current SECRET_KEY followed by SECRET_KEY_FALLBACKS.

    Decryption tries each key in order, so credentials encrypted under a rotated-out
    key remain readable while it stays in SECRET_KEY_FALLBACKS.
    """
    secret_keys = [settings.SECRET_KEY, *getattr(settings, "SECRET_KEY_FALLBACKS", [])]
    return MultiFernet([Fernet(_derive_fernet_key(secret_key)) for secret_key in secret_keys])


def encrypt_credentials(credentials: dict[str, Any]) -> dict[str, Any]:
    """
    Encrypt credential dictionary for storage.

    Args:
        credentials: Plain credential dictionary

    Returns:
        Dictionary with encrypted values:
        {
            'api_key': {'encrypted': True, 'value': 'gAAAAA...'},
            'environment': 'sandbox'  # Non-secret fields not encrypted
        }
    """
    fernet = Fernet(_get_fernet_key())
    encrypted = {}

    for key, value in credentials.items():
        # Determine if field should be encrypted (secret fields)
        # For now, encrypt all string values that look like secrets
        if isinstance(value, str) and len(value) > 0 and _is_secret_field(key):
            encrypted_value = fernet.encrypt(value.encode()).decode()
            encrypted[key] = {"encrypted": True, "value": encrypted_value}
        else:
            # Store non-secret fields in plain text
            encrypted[key] = value

    return encrypted


def decrypt_credentials(encrypted_credentials: dict[str, Any]) -> dict[str, Any]:
    """
    Decrypt credential dictionary for use.

    Args:
        encrypted_credentials: Encrypted credential dictionary from database

    Returns:
        Plain credential dictionary with decrypted values
    """
    fernet = _get_multi_fernet()
    decrypted = {}

    for key, value in encrypted_credentials.items():
        if isinstance(value, dict) and value.get("encrypted"):
            # Decrypt encrypted field
            try:
                decrypted_value = fernet.decrypt(value["value"].encode()).decode()
                decrypted[key] = decrypted_value
            except Exception as e:
                logger.error(f"Failed to decrypt field '{key}': {e}")
                raise ValueError(f"Failed to decrypt credentials: {e}")
        else:
            # Pass through non-encrypted field
            decrypted[key] = value

    return decrypted


def _is_secret_field(field_name: str) -> bool:
    """
    Determine if a field should be encrypted based on its name.

    Args:
        field_name: Credential field name

    Returns:
        True if field should be encrypted
    """
    secret_keywords = [
        "key",
        "secret",
        "token",
        "password",
        "credential",
        "client_id",
        "client_secret",
        "api_key",
        "access_token",
        "refresh_token",
        "private_key",
        "merchant_id",
        "account_id",
    ]

    field_lower = field_name.lower()
    return any(keyword in field_lower for keyword in secret_keywords)


def redact_credentials(credentials: dict[str, Any]) -> dict[str, Any]:
    """
    Redact sensitive credential values for logging.

    Args:
        credentials: Plain credential dictionary

    Returns:
        Dictionary with sensitive values masked (e.g., 'sk_***456')
    """
    redacted = {}

    for key, value in credentials.items():
        if isinstance(value, str) and _is_secret_field(key):
            # Show first 3 and last 3 characters
            if len(value) > 6:
                redacted[key] = f"{value[:3]}***{value[-3:]}"
            else:
                redacted[key] = "***"
        else:
            redacted[key] = value

    return redacted
