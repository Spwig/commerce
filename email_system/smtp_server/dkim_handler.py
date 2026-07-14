"""
DKIM Handler for Email Signing

Manages DKIM key generation, storage, and email signature generation
using the dkimpy library.
"""

import logging

import dkim
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.core.cache import cache

from email_system.models import EmailAccount
from email_system.utils.encryption import decrypt_credentials, encrypt_credentials

logger = logging.getLogger(__name__)


class DKIMHandler:
    """
    Handles DKIM key management and email signing for the built-in SMTP server.

    Features:
    - Auto-generates RSA 2048-bit key pairs
    - Encrypts private keys using EMAIL_ENCRYPTION_KEY
    - Caches keys for performance
    - Signs outgoing emails with DKIM signatures
    """

    # DKIM configuration
    DEFAULT_SELECTOR = "mail"
    KEY_SIZE = 2048
    CACHE_TTL = 3600  # 1 hour

    def __init__(self, domain: str, selector: str | None = None):
        """
        Initialize DKIM handler for a domain.

        Args:
            domain: The sending domain (e.g., 'example.com')
            selector: DKIM selector (default: 'mail')
        """
        self.domain = domain.lower().strip()
        self.selector = selector or self.DEFAULT_SELECTOR
        self.cache_key = f"dkim_keys_{self.domain}_{self.selector}"

    def generate_key_pair(self) -> tuple[bytes, bytes]:
        """
        Generate a new RSA 2048-bit DKIM key pair.

        Returns:
            Tuple of (private_key_pem, public_key_pem)
        """
        logger.info(
            f"Generating new DKIM key pair for domain: {self.domain}, selector: {self.selector}"
        )

        # Generate RSA private key
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=self.KEY_SIZE, backend=default_backend()
        )

        # Serialize private key to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        # Get public key and serialize
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        logger.info(f"DKIM key pair generated successfully for {self.domain}")
        return private_pem, public_pem

    def store_keys(
        self, private_key: bytes, public_key: bytes, account: EmailAccount | None = None
    ):
        """
        Store DKIM keys in the database.

        Note: The entire credentials dict is encrypted by encrypt_credentials(),
        so we don't need to encrypt individual keys separately.

        Args:
            private_key: Private key PEM bytes
            public_key: Public key PEM bytes
            account: EmailAccount to associate keys with (optional)
        """
        # Store in EmailAccount credentials
        if account:
            credentials = decrypt_credentials(account.credentials) if account.credentials else {}
            credentials["dkim_private_key"] = private_key.decode("utf-8")
            credentials["dkim_public_key"] = public_key.decode("utf-8")
            credentials["dkim_selector"] = self.selector
            account.credentials = encrypt_credentials(credentials)
            account.save()
            logger.info(f"DKIM keys stored for account: {account.name}")
        else:
            # Store in Django settings (for default built-in server)
            # In production, this should be stored in database or secure key management
            logger.warning(
                "Storing DKIM keys without EmailAccount - consider using database storage"
            )

        # Clear cache
        cache.delete(self.cache_key)

    def get_private_key(self, account: EmailAccount | None = None) -> bytes | None:
        """
        Retrieve the private key from decrypted credentials.

        Args:
            account: EmailAccount to get keys from

        Returns:
            Private key PEM bytes or None if not found
        """
        # Check cache first
        cached = cache.get(f"{self.cache_key}_private")
        if cached:
            return cached

        if account:
            try:
                # Decrypt the entire credentials dict
                credentials = (
                    decrypt_credentials(account.credentials) if account.credentials else {}
                )
                private_key_str = credentials.get("dkim_private_key")

                if private_key_str:
                    private_key = private_key_str.encode("utf-8")
                    # Cache for performance
                    cache.set(f"{self.cache_key}_private", private_key, self.CACHE_TTL)
                    return private_key
            except Exception as e:
                logger.error(f"Failed to retrieve DKIM private key: {e}")
                return None

        return None

    def get_public_key(self, account: EmailAccount | None = None) -> str | None:
        """
        Retrieve the public key from decrypted credentials.

        Args:
            account: EmailAccount to get keys from

        Returns:
            Public key PEM string or None if not found
        """
        # Check cache first
        cached = cache.get(f"{self.cache_key}_public")
        if cached:
            return cached

        if account:
            try:
                # Decrypt the entire credentials dict
                credentials = (
                    decrypt_credentials(account.credentials) if account.credentials else {}
                )
                public_key = credentials.get("dkim_public_key")

                if public_key:
                    # Cache for performance
                    cache.set(f"{self.cache_key}_public", public_key, self.CACHE_TTL)
                    return public_key
            except Exception as e:
                logger.error(f"Failed to retrieve DKIM public key: {e}")
                return None

        return None

    def get_dns_record(self, account: EmailAccount | None = None) -> str | None:
        """
        Generate the DNS TXT record value for DKIM.

        Args:
            account: EmailAccount to get public key from

        Returns:
            DNS TXT record value (e.g., "v=DKIM1; k=rsa; p=MIGfMA0GCSq...")
        """
        public_key = self.get_public_key(account)
        if not public_key:
            return None

        # Extract the base64 portion (remove PEM headers/footers and newlines)
        lines = public_key.split("\n")
        key_data = "".join([line for line in lines if line and not line.startswith("-----")])

        # Format as DKIM DNS record
        dns_record = f"v=DKIM1; k=rsa; p={key_data}"

        return dns_record

    def sign_message(self, message: bytes, account: EmailAccount | None = None) -> bytes:
        """
        Sign an email message with DKIM.

        Args:
            message: RFC822 formatted email message bytes
            account: EmailAccount to get private key from

        Returns:
            Signed message with DKIM-Signature header
        """
        private_key = self.get_private_key(account)

        if not private_key:
            logger.warning(f"No DKIM private key found for domain {self.domain}, sending unsigned")
            return message

        try:
            # Sign the message using dkimpy
            signature = dkim.sign(
                message=message,
                selector=self.selector.encode("utf-8"),
                domain=self.domain.encode("utf-8"),
                privkey=private_key,
                include_headers=[
                    b"from",
                    b"to",
                    b"subject",
                    b"date",
                    b"message-id",
                    b"content-type",
                ],
            )

            # Prepend DKIM-Signature header to message
            signed_message = signature + message

            logger.debug(f"Message signed with DKIM for {self.selector}._domainkey.{self.domain}")
            return signed_message

        except Exception as e:
            logger.error(f"DKIM signing failed: {e}", exc_info=True)
            # Return unsigned message on error
            return message

    def validate_signature(self, message: bytes) -> bool:
        """
        Validate a DKIM signature on a message.

        Args:
            message: RFC822 formatted email message bytes with DKIM-Signature

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            result = dkim.verify(message)
            return result
        except Exception as e:
            logger.error(f"DKIM verification failed: {e}")
            return False

    @classmethod
    def ensure_keys_exist(
        cls, domain: str, selector: str | None = None, account: EmailAccount | None = None
    ) -> "DKIMHandler":
        """
        Ensure DKIM keys exist for a domain, generating them if needed.

        Args:
            domain: The sending domain
            selector: DKIM selector (optional)
            account: EmailAccount to store keys in (optional)

        Returns:
            DKIMHandler instance with keys ready
        """
        handler = cls(domain=domain, selector=selector)

        # Check if keys already exist
        if handler.get_private_key(account) and handler.get_public_key(account):
            logger.info(f"DKIM keys already exist for {domain}")
            return handler

        # Generate new keys
        private_key, public_key = handler.generate_key_pair()
        handler.store_keys(private_key, public_key, account)

        return handler
