"""
Encryption utilities for securing exchange rate provider credentials.

Uses Django's SECRET_KEY for symmetric encryption via Fernet.
Credentials are encrypted before storing in ExchangeRateProviderAccount.credentials.
Pattern follows shipping/utils/encryption.py.
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
    # Use SHA256 to derive a consistent 32-byte key from SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_credentials(credentials: Dict[str, Any]) -> bytes:
    """
    Encrypt credential dictionary for storage in BinaryField.

    Args:
        credentials: Plain credential dictionary

    Returns:
        Encrypted bytes suitable for BinaryField storage
    """
    import json
    fernet = Fernet(_get_fernet_key())

    # Serialize to JSON then encrypt
    json_data = json.dumps(credentials).encode()
    encrypted_data = fernet.encrypt(json_data)

    return encrypted_data


def decrypt_credentials(encrypted_data: bytes) -> Dict[str, Any]:
    """
    Decrypt credential data from BinaryField.

    Args:
        encrypted_data: Encrypted bytes from database (may be memoryview)

    Returns:
        Plain credential dictionary with decrypted values
    """
    import json
    fernet = Fernet(_get_fernet_key())

    try:
        # Convert memoryview to bytes if needed (Django BinaryField returns memoryview)
        if isinstance(encrypted_data, memoryview):
            encrypted_data = bytes(encrypted_data)

        # Decrypt then deserialize from JSON
        decrypted_json = fernet.decrypt(encrypted_data)
        credentials = json.loads(decrypted_json.decode())
        return credentials
    except Exception as e:
        logger.error(f"Failed to decrypt credentials: {e}")
        raise ValueError(f"Failed to decrypt credentials: {e}")


def _is_secret_field(field_name: str) -> bool:
    """
    Determine if a field should be encrypted based on its name.

    Args:
        field_name: Credential field name

    Returns:
        True if field should be encrypted
    """
    secret_keywords = [
        'key', 'secret', 'token', 'password', 'credential',
        'client_id', 'client_secret', 'api_key', 'access_token',
        'refresh_token', 'private_key', 'app_id'
    ]

    field_lower = field_name.lower()
    return any(keyword in field_lower for keyword in secret_keywords)


def redact_credentials(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Redact sensitive credential values for logging.

    Args:
        credentials: Plain credential dictionary

    Returns:
        Dictionary with sensitive values masked (e.g., 'abc***xyz')
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
