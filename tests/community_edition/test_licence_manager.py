"""
LicenseManager behaviour for the Community edition.

Verifies the four core invariants from the plan:
- Community licences pass ``is_valid()``
- Community is detected via ``get_edition() == 'community'`` / ``is_community()``
- Community is NOT sandbox (payments use real credentials)
- Community does NOT unlock Spwig-hosted services
"""

import json

import pytest

pytestmark = pytest.mark.django_db


def test_community_licence_is_valid(licence_manager, community_licence_at_path):
    assert licence_manager.is_valid() is True


def test_community_edition_detected(licence_manager, community_licence_at_path):
    assert licence_manager.get_edition() == "community"
    assert licence_manager.is_community() is True


def test_community_is_not_sandbox(licence_manager, community_licence_at_path):
    assert licence_manager.is_sandbox() is False


def test_community_allows_free_tier_hosted_services(licence_manager, community_licence_at_path):
    """
    Community edition can call GeoIP/Geocoder/Push directly — the hosted
    services enforce a Community-tier rate limit at ingress. Only the
    hosted mail gateway remains paid-only. This is the tiered-free-access
    model introduced in Phase 2.5 (strategy revision 2026-07-06).
    """
    # Free-tier services: Community allowed
    assert licence_manager.is_hosted_service_available("geoip") is True
    assert licence_manager.is_hosted_service_available("geocoder") is True
    assert licence_manager.is_hosted_service_available("push") is True
    # Paid-only: Community still blocked
    assert licence_manager.is_hosted_service_available("mail_gateway") is False

    # Legacy blanket check now returns True (Community can use *some* services)
    assert licence_manager.are_spwig_services_available() is True


def test_missing_licence_file_is_not_sandbox(licence_manager, licence_file_path):
    """A missing licence file no longer implies sandbox mode."""
    assert not licence_file_path.exists()
    assert licence_manager.is_sandbox() is False


def test_missing_licence_file_returns_unlicensed(licence_manager, licence_file_path):
    assert not licence_file_path.exists()
    assert licence_manager.get_edition() == "unlicensed"
    assert licence_manager.is_community() is False


def test_signed_licence_verifies(licence_manager, community_licence_at_path):
    """The RSA signature on the licence must verify with the public key."""
    data = licence_manager.get_license_data()
    assert data is not None
    assert licence_manager.verify_signature(data) is True


def test_tampering_with_licence_invalidates(licence_manager, community_licence_at_path):
    """Editing the licence after signing breaks verification."""
    data = json.loads(community_licence_at_path.read_text())
    data["license"]["edition"] = "enterprise"  # try to upgrade ourselves
    community_licence_at_path.write_text(json.dumps(data))

    # Force a re-read
    licence_manager._license_data = None
    licence_manager._is_valid = None

    assert licence_manager.is_valid() is False
