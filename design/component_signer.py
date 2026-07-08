"""
Component signing and verification system.

Uses RSA-2048 + SHA256 to sign component packages, ensuring:
- Package integrity (checksum verification)
- Authenticity (signed by trusted authority)
- Tamper detection (signature verification fails if modified)

The signing process:
1. Calculate SHA256 checksum of the component package file
2. Sign the checksum with RSA private key
3. Store signature and checksum in ComponentStore model
4. Verification checks both signature validity and checksum match

Key Management:
- Private keys stored in MEDIA_ROOT/component_signing/private_key.pem
- Public keys stored in MEDIA_ROOT/component_signing/public_key.pem
- Keys are generated once and reused for all component signing
- IMPORTANT: Keep private key secure and backed up
"""

import hashlib
import os
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.files.base import File

from .models import ComponentStore


class ComponentSigner:
    """
    Signs and verifies component packages using RSA-2048 + SHA256.

    Usage:
        # Sign a component
        signer = ComponentSigner()
        success = signer.sign_component(component)

        # Verify a component
        is_valid = signer.verify_component(component)

        # Generate new keypair (only needed once)
        ComponentSigner.generate_keypair()
    """

    KEY_SIZE = 2048
    HASH_ALGORITHM = hashes.SHA256()

    def __init__(self):
        """Initialize signer with loaded keys."""
        self.keys_dir = Path(settings.MEDIA_ROOT) / 'component_signing'
        self.keys_dir.mkdir(parents=True, exist_ok=True)

        self.private_key_path = self.keys_dir / 'private_key.pem'
        self.public_key_path = self.keys_dir / 'public_key.pem'

        # Load keys (generate if missing)
        if not self.private_key_path.exists() or not self.public_key_path.exists():
            self.generate_keypair()

        self.private_key = self._load_private_key()
        self.public_key = self._load_public_key()

    def sign_component(self, component: ComponentStore) -> Tuple[bool, str]:
        """
        Sign a component package.

        Args:
            component: ComponentStore instance to sign

        Returns:
            Tuple of (success: bool, message: str)

        Process:
            1. Calculate SHA256 checksum of package_file
            2. Sign checksum with private key
            3. Update component.signature and component.checksum_sha256
            4. Update component.signed_at and component.signed_by
            5. Save component
        """
        if not component.package_file:
            return False, str(_("Component has no package file"))

        try:
            # Calculate checksum
            checksum = self._calculate_checksum(component.package_file)

            # Sign the checksum
            signature = self._sign_data(checksum.encode('utf-8'))

            # Update component
            component.checksum_sha256 = checksum
            component.signature = signature.hex()
            component.signed_at = timezone.now()
            component.signed_by = 'Spwig'  # System signing authority

            # Don't save here - let caller save to allow additional updates

            return True, str(_("Component signed successfully"))

        except Exception as e:
            return False, str(_("Signing failed: %(error)s") % {'error': str(e)})

    def verify_component(self, component: ComponentStore) -> Tuple[bool, str]:
        """
        Verify component signature and integrity.

        Args:
            component: ComponentStore instance to verify

        Returns:
            Tuple of (is_valid: bool, message: str)

        Checks:
            1. Component has signature and checksum
            2. Package file exists
            3. Calculated checksum matches stored checksum
            4. Signature is valid for checksum
        """
        # Check prerequisites
        if not component.signature:
            return False, str(_("Component has no signature"))

        if not component.checksum_sha256:
            return False, str(_("Component has no checksum"))

        if not component.package_file:
            return False, str(_("Component has no package file"))

        try:
            # Calculate current checksum
            current_checksum = self._calculate_checksum(component.package_file)

            # Check if checksum matches stored value
            if current_checksum != component.checksum_sha256:
                return False, str(_("Checksum mismatch - package has been modified"))

            # Verify signature
            signature_bytes = bytes.fromhex(component.signature)
            is_valid = self._verify_signature(
                data=current_checksum.encode('utf-8'),
                signature=signature_bytes
            )

            if is_valid:
                return True, str(_("Signature valid - component is authentic and unmodified"))
            else:
                return False, str(_("Invalid signature - component may be tampered"))

        except Exception as e:
            return False, str(_("Verification failed: %(error)s") % {'error': str(e)})

    def _calculate_checksum(self, file_field: File) -> str:
        """
        Calculate SHA256 checksum of a file.

        Args:
            file_field: Django FileField instance

        Returns:
            Hex string of SHA256 checksum
        """
        sha256_hash = hashlib.sha256()

        # Read file in chunks to handle large files
        file_field.seek(0)
        for chunk in file_field.chunks(chunk_size=8192):
            sha256_hash.update(chunk)
        file_field.seek(0)  # Reset file pointer

        return sha256_hash.hexdigest()

    def _sign_data(self, data: bytes) -> bytes:
        """
        Sign data with private key.

        Args:
            data: Bytes to sign

        Returns:
            Signature bytes
        """
        signature = self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(self.HASH_ALGORITHM),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            self.HASH_ALGORITHM
        )
        return signature

    def _verify_signature(self, data: bytes, signature: bytes) -> bool:
        """
        Verify signature with public key.

        Args:
            data: Original data that was signed
            signature: Signature bytes to verify

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            self.public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(self.HASH_ALGORITHM),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                self.HASH_ALGORITHM
            )
            return True
        except Exception:
            return False

    def _load_private_key(self):
        """Load private key from file."""
        with open(self.private_key_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    def _load_public_key(self):
        """Load public key from file."""
        with open(self.public_key_path, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    def generate_keypair(self) -> Tuple[str, str]:
        """
        Generate new RSA keypair for signing.

        Returns:
            Tuple of (private_key_path, public_key_path)

        IMPORTANT: This should only be called once during initial setup.
        If you regenerate keys, all previously signed components will fail verification.
        """
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.KEY_SIZE,
            backend=default_backend()
        )

        # Get public key
        public_key = private_key.public_key()

        # Serialize private key (no password for simplicity - secure via file permissions)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Serialize public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Write keys to files
        with open(self.private_key_path, 'wb') as f:
            f.write(private_pem)
        os.chmod(self.private_key_path, 0o600)  # Read/write for owner only

        with open(self.public_key_path, 'wb') as f:
            f.write(public_pem)
        os.chmod(self.public_key_path, 0o644)  # Read for everyone

        return str(self.private_key_path), str(self.public_key_path)


# Singleton instance for easy access
_signer_instance = None


def get_component_signer() -> ComponentSigner:
    """
    Get singleton ComponentSigner instance.

    Returns:
        ComponentSigner instance
    """
    global _signer_instance
    if _signer_instance is None:
        _signer_instance = ComponentSigner()
    return _signer_instance
