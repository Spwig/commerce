"""
Transparent at-rest encryption for sensitive model fields.

``EncryptedCharField`` encrypts on write and decrypts on read so secrets (e.g. a
form's reCAPTCHA secret key) are never stored in plaintext. It is deliberately
non-breaking:

- The Fernet key is derived from ``settings.SECRET_KEY`` (always present), so
  turning a field encrypted needs no new environment variable and can never make
  a save fail for lack of a key.
- Encrypted values carry a marker prefix. A value WITHOUT the prefix is treated
  as legacy plaintext and returned as-is, so existing rows keep working and get
  encrypted the next time they're saved — no data migration required.
- If encryption ever fails it falls back to storing plaintext (logged), never
  raising; if decryption fails (e.g. SECRET_KEY was rotated) it returns "" so
  the merchant simply re-enters the secret rather than seeing ciphertext.
"""

from __future__ import annotations

import base64
import hashlib
import logging

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db import models

logger = logging.getLogger(__name__)

_PREFIX = "fbenc:"  # marks a value as encrypted by this field


def _fernet() -> Fernet:
    """A stable Fernet built from the app SECRET_KEY (always available)."""
    digest = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


class EncryptedCharField(models.CharField):
    """CharField whose value is Fernet-encrypted at rest (transparently)."""

    def from_db_value(self, value, expression, connection):
        if not value or not isinstance(value, str):
            return value
        if value.startswith(_PREFIX):
            try:
                return _fernet().decrypt(value[len(_PREFIX) :].encode()).decode()
            except (InvalidToken, Exception):
                logger.warning(
                    "EncryptedCharField: could not decrypt value (SECRET_KEY "
                    "rotated?); returning blank so it can be re-entered."
                )
                return ""
        return value  # legacy plaintext — returned as-is, re-encrypted on next save

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return value
        if value.startswith(_PREFIX):
            return value  # already encrypted (idempotent)
        try:
            return _PREFIX + _fernet().encrypt(value.encode()).decode()
        except Exception:
            logger.warning(
                "EncryptedCharField: encryption failed; storing plaintext.",
                exc_info=True,
            )
            return value
