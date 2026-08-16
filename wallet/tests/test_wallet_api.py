"""
Wallet customer API — transaction history (list_transaction_history).

Beyond the happy path: the history must honour type/source/status filters and
offset pagination, return an empty page (not 500) for a customer with no wallet,
and NEVER leak another customer's ledger. The endpoint is authenticated and
scoped to ``request.user`` — these pin that scoping.
"""

from decimal import Decimal

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from tests.factories import UserFactory
from wallet.api.views import WalletTransactionViewSet
from wallet.models import WalletTransaction
from wallet.services import WalletService

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.wallet]


def _list(user, **params):
    request = APIRequestFactory().get("/api/wallet/transactions/", params)
    force_authenticate(request, user=user)
    response = WalletTransactionViewSet.as_view({"get": "list"})(request)
    response.render()
    return response


def _seed(user):
    WalletService.credit(user, Decimal("50.00"), "USD", "referral", "reward")
    WalletService.debit(user, Decimal("10.00"), "USD", "order", "spend")
    WalletService.record_refund_transaction(user, Decimal("5.00"), "USD", "refund")


class TestTransactionHistory:
    def test_lists_newest_first(self):
        user = UserFactory()
        _seed(user)
        data = _list(user).data["data"]
        assert len(data) == 3
        # Most recent (the refund) first.
        assert data[0]["transaction_type"] == WalletTransaction.TYPE_REFUND

    def test_filters_by_type(self):
        user = UserFactory()
        _seed(user)
        data = _list(user, type="refund").data["data"]
        assert len(data) == 1
        assert data[0]["transaction_type"] == "refund"

    def test_filters_by_source(self):
        user = UserFactory()
        _seed(user)
        data = _list(user, source="order").data["data"]
        assert len(data) == 1
        assert data[0]["source"] == "order"

    def test_filters_by_status(self):
        user = UserFactory()
        _seed(user)
        # All seeded rows are completed.
        assert len(_list(user, status="completed").data["data"]) == 3
        assert len(_list(user, status="reversed").data["data"]) == 0

    def test_pagination_limits_and_reports_has_more(self):
        user = UserFactory()
        _seed(user)
        body = _list(user, limit=2, offset=0).data
        assert len(body["data"]) == 2
        assert body["pagination"]["total"] == 3
        assert body["pagination"]["has_more"] is True

        body2 = _list(user, limit=2, offset=2).data
        assert len(body2["data"]) == 1
        assert body2["pagination"]["has_more"] is False

    def test_a_bad_limit_falls_back_to_the_default(self):
        user = UserFactory()
        _seed(user)
        body = _list(user, limit="not-a-number").data
        assert body["pagination"]["limit"] == 20  # default, not a 500

    def test_no_wallet_returns_an_empty_page(self):
        user = UserFactory()  # never touched their wallet
        body = _list(user).data
        assert body["success"] is True
        assert body["data"] == []
        assert body["pagination"]["total"] == 0

    def test_a_customer_never_sees_another_customers_history(self):
        alice = UserFactory()
        bob = UserFactory()
        _seed(alice)
        WalletService.credit(bob, Decimal("999.00"), "USD", "manual", "bob only")

        data = _list(alice).data["data"]
        assert len(data) == 3  # only Alice's three rows
        assert all(row["transaction_type"] != "credit" or row["amount"] != "999.00" for row in data)
