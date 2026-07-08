"""
Shared fixtures for Community edition tests.

Provides a locally-signed Community licence file plus a public key override
that ``LicenseManager`` uses, so tests don't depend on Spwig's real private
key.
"""

import base64
import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


@pytest.fixture
def rsa_keypair():
    """Generate a fresh RSA-2048 key pair for the test session."""
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = private.public_key()
    return private, public


@pytest.fixture
def signed_community_licence(rsa_keypair):
    """Build a Community licence JSON dict signed by the test key pair."""
    private, _public = rsa_keypair

    licence_obj = {
        "license_type": "community",
        "edition": "community",
        "environment_type": "production",
        "is_active": True,
        "issued_to": "Community Edition (test)",
        "issued_at": "2026-07-05T00:00:00Z",
        "expires_at": None,
        "hosting_type": "self_hosted",
        "major_version": 1,
        "license_key": "COMMUNITY-EDITION-TEST",
        "entitlements": [
            {"slug": "edition", "value_type": "string", "value": "community"},
            {"slug": "pos_module", "value_type": "boolean", "value": False},
            {"slug": "spwig_hosted_services", "value_type": "boolean", "value": False},
            {"slug": "payment_processing", "value_type": "boolean", "value": True},
            {"slug": "major_version", "value_type": "numeric", "value": 1},
        ],
    }

    payload = json.dumps(licence_obj, sort_keys=True).encode()
    signature = private.sign(
        payload,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return {
        "license": licence_obj,
        "signature": base64.b64encode(signature).decode(),
    }


@pytest.fixture
def licence_file_path(tmp_path):
    """A writable path for the licence file, in a per-test temp directory."""
    return tmp_path / "license.json"


@pytest.fixture
def community_licence_at_path(licence_file_path, signed_community_licence):
    """Write the signed Community licence to disk and return its path."""
    licence_file_path.write_text(json.dumps(signed_community_licence))
    return licence_file_path


@pytest.fixture
def licence_manager(rsa_keypair, licence_file_path, tmp_path, settings):
    """
    A LicenseManager pointed at the test licence file, using the test public key.

    Callers may or may not have written a licence file yet — the manager
    reads on demand.
    """
    from django.core.cache import cache
    from core.license import LicenseManager

    _, public = rsa_keypair

    # Write public key to disk so LicenseManager can load it
    pub_pem = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    pub_key_path = tmp_path / "test-public-key.pem"
    pub_key_path.write_bytes(pub_pem)

    settings.LICENSE_PATH = str(licence_file_path)

    # LicenseManager caches licence data in the Django cache under CACHE_KEY.
    # Between tests that cache would leak stale data across the LICENSE_PATH
    # changes we make in each test. Clear before and after.
    cache.delete(LicenseManager.CACHE_KEY)

    mgr = LicenseManager()
    mgr.public_key_path = pub_key_path

    yield mgr

    cache.delete(LicenseManager.CACHE_KEY)
