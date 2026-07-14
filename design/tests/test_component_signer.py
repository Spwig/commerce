"""
Tests for ComponentSigner - Component signing and verification system.

Tests cover:
- Key generation and management
- Component package signing
- Signature verification
- Checksum calculation
- Security and integrity checks
"""

import hashlib
import os
from pathlib import Path

import pytest
from django.core.files.base import ContentFile
from django.utils import timezone

from design.component_signer import ComponentSigner, get_component_signer
from design.models import ComponentStore


@pytest.fixture
def temp_media_root(tmp_path):
    """Create temporary media root for testing."""
    media_root = tmp_path / "media"
    media_root.mkdir()
    return media_root


@pytest.fixture
def signer(temp_media_root, settings):
    """Create ComponentSigner with temporary keys directory."""
    settings.MEDIA_ROOT = str(temp_media_root)
    return ComponentSigner()


@pytest.fixture
def sample_component(db):
    """Create a sample component for testing."""
    component = ComponentStore.objects.create(
        component_type="test_banner",
        display_name="Test Banner",
        version="1.0.0",
        author="Test Author",
        description="Test component for signing",
        review_status="pending",
        render_mode="server",
    )

    # Add a package file
    package_content = b"Test package content for signing"
    component.package_file.save("test_package.zip", ContentFile(package_content), save=True)

    return component


@pytest.mark.django_db
class TestComponentSignerInitialization:
    """Test ComponentSigner initialization and setup."""

    def test_creates_keys_directory(self, temp_media_root, settings):
        """Test that ComponentSigner creates keys directory if it doesn't exist."""
        settings.MEDIA_ROOT = str(temp_media_root)

        signer = ComponentSigner()

        assert signer.keys_dir.exists()
        assert signer.keys_dir == temp_media_root / "component_signing"

    def test_generates_keys_on_first_initialization(self, temp_media_root, settings):
        """Test that keys are generated if they don't exist."""
        settings.MEDIA_ROOT = str(temp_media_root)

        signer = ComponentSigner()

        assert signer.private_key_path.exists()
        assert signer.public_key_path.exists()
        assert signer.private_key is not None
        assert signer.public_key is not None

    def test_loads_existing_keys(self, signer):
        """Test that ComponentSigner loads existing keys."""
        # First initialization generates keys
        first_private_key_content = signer.private_key_path.read_bytes()
        first_public_key_content = signer.public_key_path.read_bytes()

        # Second initialization should load the same keys
        signer2 = ComponentSigner()

        assert signer2.private_key_path.read_bytes() == first_private_key_content
        assert signer2.public_key_path.read_bytes() == first_public_key_content

    def test_private_key_has_correct_permissions(self, signer):
        """Test that private key file has 0o600 permissions (owner read/write only)."""
        stat_info = os.stat(signer.private_key_path)
        permissions = stat_info.st_mode & 0o777

        assert permissions == 0o600

    def test_public_key_has_correct_permissions(self, signer):
        """Test that public key file has 0o644 permissions (readable by all)."""
        stat_info = os.stat(signer.public_key_path)
        permissions = stat_info.st_mode & 0o777

        assert permissions == 0o644


@pytest.mark.django_db
class TestKeyGeneration:
    """Test RSA keypair generation."""

    def test_generate_keypair_creates_files(self, signer):
        """Test that generate_keypair creates key files."""
        # Delete existing keys
        signer.private_key_path.unlink()
        signer.public_key_path.unlink()

        private_path, public_path = signer.generate_keypair()

        assert Path(private_path).exists()
        assert Path(public_path).exists()

    def test_generate_keypair_returns_paths(self, signer):
        """Test that generate_keypair returns key file paths."""
        private_path, public_path = signer.generate_keypair()

        assert private_path == str(signer.private_key_path)
        assert public_path == str(signer.public_key_path)

    def test_generated_keys_are_valid_pem(self, signer):
        """Test that generated keys are valid PEM format."""
        private_content = signer.private_key_path.read_text()
        public_content = signer.public_key_path.read_text()

        assert "-----BEGIN PRIVATE KEY-----" in private_content
        assert "-----END PRIVATE KEY-----" in private_content
        assert "-----BEGIN PUBLIC KEY-----" in public_content
        assert "-----END PUBLIC KEY-----" in public_content

    def test_generated_keys_are_rsa_2048(self, signer):
        """Test that generated keys use RSA-2048."""
        key_size = signer.private_key.key_size
        assert key_size == 2048


@pytest.mark.django_db
class TestComponentSigning:
    """Test component package signing functionality."""

    def test_sign_component_success(self, signer, sample_component):
        """Test successfully signing a component."""
        success, message = signer.sign_component(sample_component)

        assert success is True
        assert "successfully" in message.lower()
        assert sample_component.signature
        assert sample_component.checksum_sha256
        assert sample_component.signed_at is not None
        assert sample_component.signed_by == "Spwig"

    def test_sign_component_without_package_file(self, signer, db):
        """Test signing component without package file fails."""
        component = ComponentStore.objects.create(
            component_type="no_package",
            display_name="No Package",
            version="1.0.0",
            author="Test",
            description="Component without package",
            review_status="pending",
        )

        success, message = signer.sign_component(component)

        assert success is False
        assert "no package file" in message.lower()

    def test_signature_is_hex_string(self, signer, sample_component):
        """Test that signature is stored as hex string."""
        signer.sign_component(sample_component)

        # Should be valid hex
        try:
            bytes.fromhex(sample_component.signature)
            is_hex = True
        except ValueError:
            is_hex = False

        assert is_hex

    def test_checksum_is_sha256(self, signer, sample_component):
        """Test that checksum is valid SHA256 hash."""
        signer.sign_component(sample_component)

        # SHA256 hex digest is 64 characters
        assert len(sample_component.checksum_sha256) == 64

        # Should be valid hex
        try:
            bytes.fromhex(sample_component.checksum_sha256)
            is_hex = True
        except ValueError:
            is_hex = False

        assert is_hex

    def test_checksum_matches_file_content(self, signer, sample_component):
        """Test that calculated checksum matches actual file content."""
        signer.sign_component(sample_component)

        # Calculate checksum manually
        sha256_hash = hashlib.sha256()
        sample_component.package_file.seek(0)
        for chunk in sample_component.package_file.chunks(chunk_size=8192):
            sha256_hash.update(chunk)
        expected_checksum = sha256_hash.hexdigest()

        assert sample_component.checksum_sha256 == expected_checksum

    def test_signed_at_is_recent(self, signer, sample_component):
        """Test that signed_at is set to recent timestamp."""
        before = timezone.now()
        signer.sign_component(sample_component)
        after = timezone.now()

        assert before <= sample_component.signed_at <= after

    def test_re_signing_updates_signature(self, signer, sample_component):
        """Test that re-signing a component updates the signature."""
        # First signing
        signer.sign_component(sample_component)
        first_signature = sample_component.signature
        first_signed_at = sample_component.signed_at

        # Modify package file
        sample_component.package_file.save(
            "modified_package.zip", ContentFile(b"Modified package content"), save=True
        )

        # Re-sign
        signer.sign_component(sample_component)

        # Signature should be different
        assert sample_component.signature != first_signature
        assert sample_component.signed_at > first_signed_at


@pytest.mark.django_db
class TestComponentVerification:
    """Test component signature verification."""

    def test_verify_valid_signature(self, signer, sample_component):
        """Test verifying a validly signed component."""
        signer.sign_component(sample_component)

        is_valid, message = signer.verify_component(sample_component)

        assert is_valid is True
        assert "valid" in message.lower()
        assert "authentic" in message.lower()

    def test_verify_component_without_signature(self, signer, sample_component):
        """Test verifying component without signature fails."""
        is_valid, message = signer.verify_component(sample_component)

        assert is_valid is False
        assert "no signature" in message.lower()

    def test_verify_component_without_checksum(self, signer, sample_component):
        """Test verifying component without checksum fails."""
        sample_component.signature = "fake_signature"

        is_valid, message = signer.verify_component(sample_component)

        assert is_valid is False
        assert "no checksum" in message.lower()

    def test_verify_component_without_package_file(self, signer, db):
        """Test verifying component without package file fails."""
        component = ComponentStore.objects.create(
            component_type="no_package",
            display_name="No Package",
            version="1.0.0",
            author="Test",
            description="Component without package",
            review_status="pending",
            signature="fake_signature",
            checksum_sha256="fake_checksum",
        )

        is_valid, message = signer.verify_component(component)

        assert is_valid is False
        assert "no package file" in message.lower()

    def test_verify_modified_package_fails(self, signer, sample_component):
        """Test that verification fails if package file is modified after signing."""
        # Sign component
        signer.sign_component(sample_component)
        sample_component.save()

        # Modify package file (but keep signature)
        original_signature = sample_component.signature
        original_checksum = sample_component.checksum_sha256

        sample_component.package_file.save(
            "modified_package.zip", ContentFile(b"Tampered package content"), save=True
        )

        # Restore signature and checksum (simulating tampering)
        sample_component.signature = original_signature
        sample_component.checksum_sha256 = original_checksum
        sample_component.save()

        # Verification should fail
        is_valid, message = signer.verify_component(sample_component)

        assert is_valid is False
        assert "checksum mismatch" in message.lower() or "modified" in message.lower()

    def test_verify_invalid_signature_fails(self, signer, sample_component):
        """Test that verification fails with invalid signature."""
        # Sign component
        signer.sign_component(sample_component)

        # Corrupt signature
        signature_bytes = bytes.fromhex(sample_component.signature)
        corrupted_signature = bytes(b ^ 0xFF for b in signature_bytes)  # Flip all bits
        sample_component.signature = corrupted_signature.hex()

        # Verification should fail
        is_valid, message = signer.verify_component(sample_component)

        assert is_valid is False
        assert "invalid signature" in message.lower() or "tampered" in message.lower()


@pytest.mark.django_db
class TestSingletonPattern:
    """Test singleton pattern for ComponentSigner."""

    def test_get_component_signer_returns_singleton(self, temp_media_root, settings):
        """Test that get_component_signer() returns the same instance."""
        settings.MEDIA_ROOT = str(temp_media_root)

        # Clear singleton
        import design.component_signer as signer_module

        signer_module._signer_instance = None

        signer1 = get_component_signer()
        signer2 = get_component_signer()

        assert signer1 is signer2

    def test_singleton_instance_is_component_signer(self, temp_media_root, settings):
        """Test that singleton instance is ComponentSigner type."""
        settings.MEDIA_ROOT = str(temp_media_root)

        # Clear singleton
        import design.component_signer as signer_module

        signer_module._signer_instance = None

        signer = get_component_signer()

        assert isinstance(signer, ComponentSigner)
