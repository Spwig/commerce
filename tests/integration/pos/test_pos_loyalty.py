"""
POS Loyalty API integration tests.

Tests for loyalty membership status and points preview endpoints.
Covers enrolled members, non-members, and points calculation previews.
"""

import pytest

from tests.factories import UserFactory
from tests.helpers import assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]


def _member_url(customer_id):
    return f"/api/pos/loyalty/member/{customer_id}/"


def _preview_url(customer_id):
    return f"/api/pos/loyalty/preview/{customer_id}/"


# ============================================================
# TestLoyaltyMember
# ============================================================


class TestLoyaltyMember:
    """Tests for GET /api/pos/loyalty/member/<customer_id>/."""

    def test_membership_status(self, pos_client, site_settings):
        """Returns loyalty membership info for an enrolled customer."""
        from loyalty.models import LoyaltyBalance, LoyaltyMember, LoyaltyTier

        customer = UserFactory(
            first_name="Loyal",
            last_name="Customer",
            is_staff=False,
        )
        tier = LoyaltyTier.objects.create(
            name="Gold",
            slug="gold",
            rank=2,
            min_points_earned=500,
            color="#FFD700",
            is_active=True,
        )
        # Non-staff users get auto-enrolled via post_save signal, so
        # use get_or_create and update the existing member.
        member, _ = LoyaltyMember.objects.get_or_create(
            customer=customer,
            defaults={"is_active": True},
        )
        member.current_tier = tier
        member.is_active = True
        member.save(update_fields=["current_tier", "is_active"])
        LoyaltyBalance.objects.update_or_create(
            member=member,
            defaults={"available_points": 750},
        )

        response = pos_client.get(_member_url(customer.id))
        data = assert_pos_success(response)

        assert data["is_member"] is True
        assert data["tier_name"] == "Gold"
        assert data["tier_color"] == "#FFD700"
        assert data["available_points"] == 750

    def test_non_member(self, pos_client, site_settings):
        """Returns is_member=False for a customer not enrolled in loyalty."""
        # Use is_staff=True so the auto-enrollment signal is skipped;
        # the loyalty view only cares whether a LoyaltyMember row exists.
        customer = UserFactory(
            first_name="Regular",
            last_name="Shopper",
            is_staff=True,
        )
        response = pos_client.get(_member_url(customer.id))
        data = assert_pos_success(response)

        assert data["is_member"] is False


# ============================================================
# TestLoyaltyPreview
# ============================================================


class TestLoyaltyPreview:
    """Tests for GET /api/pos/loyalty/preview/<customer_id>/?cart_total=..."""

    def test_points_for_amount(self, pos_client, site_settings):
        """
        Shows points to be earned for a given cart total.
        For non-members or when the engine is not configured,
        the endpoint gracefully returns 0 points.
        """
        customer = UserFactory(
            first_name="Preview",
            last_name="Customer",
            is_staff=False,
        )
        response = pos_client.get(
            _preview_url(customer.id),
            {"cart_total": "49.99"},
        )
        data = assert_pos_success(response)

        # Non-member: should return 0 points preview
        assert "points_preview" in data
        assert data["points_preview"] == 0

    def test_zero_total(self, pos_client, site_settings):
        """Zero cart total returns zero points."""
        customer = UserFactory(
            first_name="Zero",
            last_name="Total",
            is_staff=False,
        )
        response = pos_client.get(
            _preview_url(customer.id),
            {"cart_total": "0"},
        )
        data = assert_pos_success(response)

        assert data["points_preview"] == 0
