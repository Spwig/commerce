"""
Encryption utilities for securing email provider credentials.

Uses EMAIL_ENCRYPTION_KEY from settings for symmetric encryption via Fernet.
Credentials are encrypted before storing in EmailAccount.credentials.
Pattern follows exchange_rates/utils/encryption.py.
"""
import base64
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_fernet() -> Fernet:
    """
    Get Fernet instance using EMAIL_ENCRYPTION_KEY from settings.

    Returns:
        Fernet instance for encryption/decryption

    Raises:
        ValueError: If EMAIL_ENCRYPTION_KEY is not set
    """
    encryption_key = getattr(settings, 'EMAIL_ENCRYPTION_KEY', None)

    if not encryption_key:
        raise ValueError(
            "EMAIL_ENCRYPTION_KEY not set in settings. "
            "Generate with: from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
        )

    # Ensure key is bytes
    if isinstance(encryption_key, str):
        encryption_key = encryption_key.encode()

    return Fernet(encryption_key)


def encrypt_credentials(credentials: Dict[str, Any]) -> bytes:
    """
    Encrypt credential dictionary for storage in BinaryField.

    Args:
        credentials: Plain credential dictionary

    Returns:
        Encrypted bytes suitable for BinaryField storage

    Raises:
        ValueError: If encryption fails
    """
    import json

    try:
        fernet = _get_fernet()

        # Serialize to JSON then encrypt
        json_data = json.dumps(credentials).encode()
        encrypted_data = fernet.encrypt(json_data)

        return encrypted_data
    except Exception as e:
        logger.error(f"Failed to encrypt credentials: {e}")
        raise ValueError(f"Failed to encrypt credentials: {e}")


def decrypt_credentials(encrypted_data: bytes) -> Dict[str, Any]:
    """
    Decrypt credential data from BinaryField.

    Args:
        encrypted_data: Encrypted bytes from database (may be memoryview)

    Returns:
        Plain credential dictionary with decrypted values

    Raises:
        ValueError: If decryption fails
    """
    import json

    try:
        fernet = _get_fernet()

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
        'refresh_token', 'private_key', 'app_id', 'server_token',
        'webhook_secret', 'signing_secret', 'smtp_password'
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
