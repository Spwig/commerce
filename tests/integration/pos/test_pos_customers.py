"""
POS Customer API integration tests.

Tests for customer search, creation, and profile retrieval
via the POS API endpoints. Covers query validation, deduplication,
walk-in creation, and order history aggregation.
"""

from decimal import Decimal

import pytest

from tests.factories import OrderFactory, UserFactory
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

SEARCH_URL = "/api/pos/customers/search/"
CREATE_URL = "/api/pos/customers/"


def _detail_url(customer_id):
    return f"/api/pos/customers/{customer_id}/"


# ============================================================
# TestCustomerSearch
# ============================================================


class TestCustomerSearch:
    """Tests for GET /api/pos/customers/search/?q=..."""

    def test_search_by_email(self, pos_client, site_settings):
        """Search by email returns the matching customer."""
        customer = UserFactory(
            email="jane.doe@example.com",
            first_name="Jane",
            last_name="Doe",
            is_staff=False,
        )
        response = pos_client.get(SEARCH_URL, {"q": "jane.doe@example"})
        data = assert_pos_success(response)

        assert data["count"] >= 1
        emails = [r["email"] for r in data["results"]]
        assert customer.email in emails

    def test_search_by_name(self, pos_client, site_settings):
        """Search by first or last name returns matching customers."""
        customer = UserFactory(
            first_name="Alejandro",
            last_name="Montoya",
            is_staff=False,
        )
        response = pos_client.get(SEARCH_URL, {"q": "Alejandro"})
        data = assert_pos_success(response)

        assert data["count"] >= 1
        ids = [r["id"] for r in data["results"]]
        assert customer.id in ids

    def test_search_by_phone(self, pos_client, site_settings):
        """
        Phone-based search does not match because the current search
        filters on User fields (email, first_name, last_name) only.
        Phone is stored on CustomerProfile, not queried by the search view.
        """
        from accounts.models import CustomerProfile

        customer = UserFactory(
            first_name="Phone",
            last_name="User",
            is_staff=False,
        )
        CustomerProfile.objects.update_or_create(
            user=customer, defaults={"phone": "+1-555-987-6543"}
        )
        # Searching by the phone number alone should yield no results
        response = pos_client.get(SEARCH_URL, {"q": "555-987"})
        data = assert_pos_success(response)
        ids = [r["id"] for r in data["results"]]
        assert customer.id not in ids

    def test_min_query_length(self, pos_client, site_settings):
        """Query shorter than 2 characters returns QUERY_TOO_SHORT error."""
        response = pos_client.get(SEARCH_URL, {"q": "a"})
        assert_pos_error(response, "QUERY_TOO_SHORT", http_status=400)

    def test_empty_results(self, pos_client, site_settings):
        """A query with no matches returns an empty results list."""
        response = pos_client.get(SEARCH_URL, {"q": "zznonexistent99"})
        data = assert_pos_success(response)

        assert data["count"] == 0
        assert data["results"] == []


# ============================================================
# TestCustomerCreate
# ============================================================


class TestCustomerCreate:
    """Tests for POST /api/pos/customers/."""

    def test_create_walk_in(self, pos_client, site_settings):
        """Create a walk-in customer with minimal data (first_name only)."""
        response = pos_client.post(
            CREATE_URL,
            {
                "first_name": "Walk-In",
            },
        )
        data = assert_pos_success(response, http_status=201)

        assert data["is_existing"] is False
        assert data["customer"]["first_name"] == "Walk-In"
        assert data["customer"]["id"] is not None

    def test_email_dedup(self, pos_client, site_settings):
        """Creating with an existing email returns the existing customer (200, not 201)."""
        existing = UserFactory(
            email="dedup@example.com",
            first_name="Existing",
            last_name="Customer",
            is_staff=False,
        )
        response = pos_client.post(
            CREATE_URL,
            {
                "email": "dedup@example.com",
                "first_name": "New",
            },
        )
        data = assert_pos_success(response, http_status=200)

        assert data["is_existing"] is True
        assert data["customer"]["id"] == existing.id
        assert data["customer"]["first_name"] == "Existing"

    def test_phone_only(self, pos_client, site_settings):
        """Create with a phone number and first_name but no email."""
        response = pos_client.post(
            CREATE_URL,
            {
                "first_name": "PhoneCustomer",
                "phone": "+1-555-123-4567",
            },
        )
        data = assert_pos_success(response, http_status=201)

        assert data["is_existing"] is False
        assert data["customer"]["first_name"] == "PhoneCustomer"
        assert data["customer"]["phone"] == "+1-555-123-4567"

    def test_first_name_required(self, pos_client, site_settings):
        """Omitting first_name returns a validation error."""
        response = pos_client.post(
            CREATE_URL,
            {
                "email": "nofirst@example.com",
            },
        )
        assert response.status_code == 400


# ============================================================
# TestCustomerDetail
# ============================================================


class TestCustomerDetail:
    """Tests for GET /api/pos/customers/<id>/."""

    def test_profile(self, pos_client, site_settings):
        """Returns basic customer profile fields."""
        customer = UserFactory(
            first_name="Detail",
            last_name="Test",
            email="detail@test.com",
            is_staff=False,
        )
        response = pos_client.get(_detail_url(customer.id))
        data = assert_pos_success(response)

        assert data["customer"]["id"] == customer.id
        assert data["customer"]["first_name"] == "Detail"
        assert data["customer"]["last_name"] == "Test"
        assert data["customer"]["email"] == "detail@test.com"

    def test_includes_order_history(self, pos_client, site_settings):
        """Profile includes total_orders count and total_spent."""
        customer = UserFactory(
            first_name="Shopper",
            last_name="Jones",
            is_staff=False,
        )
        OrderFactory(user=customer, total_amount=Decimal("50.00"))
        OrderFactory(user=customer, total_amount=Decimal("30.00"))

        response = pos_client.get(_detail_url(customer.id))
        data = assert_pos_success(response)

        assert data["customer"]["total_orders"] == 2
        assert Decimal(data["customer"]["total_spent"]) == Decimal("80.00")

    def test_loyalty_points(self, pos_client, site_settings):
        """
        When a customer is enrolled in loyalty, the detail response
        still works (loyalty data is on a separate endpoint).
        Verify the profile loads without error for loyalty members.
        """
        from loyalty.models import LoyaltyBalance, LoyaltyMember

        customer = UserFactory(
            first_name="Loyal",
            last_name="Member",
            is_staff=False,
        )
        # Non-staff users get auto-enrolled via post_save signal, so
        # use get_or_create to avoid IntegrityError on duplicate key.
        member, _ = LoyaltyMember.objects.get_or_create(
            customer=customer,
            defaults={"is_active": True},
        )
        LoyaltyBalance.objects.update_or_create(
            member=member,
            defaults={"available_points": 250},
        )

        response = pos_client.get(_detail_url(customer.id))
        data = assert_pos_success(response)

        # The customer detail endpoint returns profile data;
        # loyalty info is fetched via the loyalty endpoints.
        assert data["customer"]["id"] == customer.id
        assert data["customer"]["first_name"] == "Loyal"

    def test_not_found(self, pos_client, site_settings):
        """404 for a customer ID that does not exist."""
        response = pos_client.get(_detail_url(999999))
        assert_pos_error(response, "NOT_FOUND", http_status=404)
