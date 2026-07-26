"""
Tests for `commerce.OrderPlacementService.place_order()` — the drift gate.

The gate re-prices the cart immediately before placement and compares the
fresh figure against the total stored on the session. `create_order` is stubbed
here so these tests exercise the gate in isolation, deterministically; a full
placement through the Test Gateway belongs to the checkout phase.

The behaviours under test:
  - no drift          -> delegates to create_order, returns its result
  - warn-only + drift  -> logs, still delegates (stored total is authoritative,
                          exactly as today)
  - enforce + drift    -> refuses with ok=False, never calls create_order
  - expected_total OK  -> delegates
  - expected_total bad -> raises QuoteDriftError regardless of the flag
"""

from decimal import Decimal
from unittest.mock import patch

import pytest
from django.test import override_settings
from djmoney.money import Money

from cart.services.checkout_service import CheckoutService
from commerce import (
    OrderPlacementService,
    PlacementRequest,
    QuoteDriftError,
)
from tests.factories import CartFactory, CartItemFactory, ProductFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.checkout,
]

SENTINEL_ORDER = object()
CREATE_ORDER = "cart.services.checkout_service.CheckoutService.create_order"


@pytest.fixture
def priced_session(db, customer_user, site_settings):
    """
    A checkout session whose stored total matches a fresh quote ($25).

    No address, so the quote is subtotal-only and fully deterministic.
    """
    cart = CartFactory(user=customer_user)
    CartItemFactory(
        cart=cart,
        product=ProductFactory(name="Widget", price=Decimal("25.00")),
        quantity=1,
        unit_price=Decimal("25.00"),
    )
    session = CheckoutService.get_or_create_session(cart)
    session.recalculate_totals()
    session.refresh_from_db()
    assert session.total_amount.amount == Decimal("25.00")
    return session


def _force_drift(session):
    """Make the stored total disagree with what the cart actually prices to."""
    session.total_amount = Money(Decimal("99.00"), "USD")
    session.save(update_fields=["total_amount"])


class TestNoDrift:
    def test_delegates_to_create_order_and_returns_its_result(self, priced_session):
        with patch(CREATE_ORDER, return_value=(True, "created", SENTINEL_ORDER)) as m:
            result = OrderPlacementService.place_order(PlacementRequest(session=priced_session))

        m.assert_called_once_with(priced_session, clear_session=True, channel="web")
        assert result.ok is True
        assert result.order is SENTINEL_ORDER
        assert result.quote.total_amount.amount == Decimal("25.00")

    def test_passes_clear_session_through(self, priced_session):
        with patch(CREATE_ORDER, return_value=(True, "created", SENTINEL_ORDER)) as m:
            OrderPlacementService.place_order(
                PlacementRequest(session=priced_session, clear_session=False)
            )
        m.assert_called_once_with(priced_session, clear_session=False, channel="web")

    def test_channel_is_forwarded_to_create_order(self, priced_session):
        with patch(CREATE_ORDER, return_value=(True, "created", SENTINEL_ORDER)) as m:
            OrderPlacementService.place_order(
                PlacementRequest(session=priced_session, channel="agent")
            )
        m.assert_called_once_with(priced_session, clear_session=True, channel="agent")


class TestStoredVsFreshDrift:
    def test_warn_only_still_places(self, priced_session, caplog):
        _force_drift(priced_session)

        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=False):
            with patch(CREATE_ORDER, return_value=(True, "created", SENTINEL_ORDER)) as m:
                with caplog.at_level("WARNING"):
                    result = OrderPlacementService.place_order(
                        PlacementRequest(session=priced_session)
                    )

        assert result.ok is True
        m.assert_called_once()
        assert any("Quote drift" in r.message for r in caplog.records)

    def test_enforce_refuses_and_does_not_create(self, priced_session):
        _force_drift(priced_session)

        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=True):
            with patch(CREATE_ORDER) as m:
                result = OrderPlacementService.place_order(PlacementRequest(session=priced_session))

        assert result.ok is False
        assert result.order is None
        assert result.quote.total_amount.amount == Decimal("25.00")
        m.assert_not_called()

    def test_no_drift_is_silent(self, priced_session, caplog):
        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=True):
            with patch(CREATE_ORDER, return_value=(True, "ok", SENTINEL_ORDER)):
                with caplog.at_level("WARNING"):
                    result = OrderPlacementService.place_order(
                        PlacementRequest(session=priced_session)
                    )

        assert result.ok is True
        assert not any("Quote drift" in r.message for r in caplog.records)


class TestExpectedTotalAssertion:
    def test_match_delegates(self, priced_session):
        with patch(CREATE_ORDER, return_value=(True, "ok", SENTINEL_ORDER)) as m:
            result = OrderPlacementService.place_order(
                PlacementRequest(
                    session=priced_session,
                    expected_total=Money(Decimal("25.00"), "USD"),
                )
            )
        assert result.ok is True
        m.assert_called_once()

    def test_mismatch_raises_regardless_of_flag(self, priced_session):
        # Even in warn-only mode, an explicit caller assertion is authoritative.
        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=False):
            with patch(CREATE_ORDER) as m:
                with pytest.raises(QuoteDriftError) as exc:
                    OrderPlacementService.place_order(
                        PlacementRequest(
                            session=priced_session,
                            expected_total=Money(Decimal("30.00"), "USD"),
                        )
                    )
        assert exc.value.expected == Money(Decimal("30.00"), "USD")
        assert exc.value.actual == Money(Decimal("25.00"), "USD")
        m.assert_not_called()

    def test_mismatch_raises_before_touching_create_order_even_with_stored_drift(
        self, priced_session
    ):
        # expected_total is checked against the FRESH quote, not the stored
        # total, so it fires even when the stored value is itself wrong.
        _force_drift(priced_session)
        with patch(CREATE_ORDER) as m:
            with pytest.raises(QuoteDriftError):
                OrderPlacementService.place_order(
                    PlacementRequest(
                        session=priced_session,
                        expected_total=Money(Decimal("99.00"), "USD"),
                    )
                )
        m.assert_not_called()


QUOTE_FOR = "commerce.ordering._quote_for"


class TestQuoteFailureIsSafeInWarnOnly:
    """
    The verification quote is an observer. A failure computing it must never
    lose a checkout that would otherwise place — except in enforce mode, or
    when a caller asserted a price we can no longer verify.
    """

    def test_warn_only_places_even_if_quote_raises(self, priced_session, caplog):
        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=False):
            with patch(QUOTE_FOR, side_effect=ValueError("pricing blew up")):
                with patch(CREATE_ORDER, return_value=(True, "created", SENTINEL_ORDER)) as m:
                    with caplog.at_level("ERROR"):
                        result = OrderPlacementService.place_order(
                            PlacementRequest(session=priced_session)
                        )

        # The order still places; the quote failure is swallowed and logged.
        assert result.ok is True
        assert result.order is SENTINEL_ORDER
        assert result.quote is None
        m.assert_called_once()
        assert any("could not compute a verification quote" in r.message for r in caplog.records)

    def test_enforce_refuses_if_quote_raises(self, priced_session):
        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=True):
            with patch(QUOTE_FOR, side_effect=ValueError("pricing blew up")):
                with patch(CREATE_ORDER) as m:
                    result = OrderPlacementService.place_order(
                        PlacementRequest(session=priced_session)
                    )

        assert result.ok is False
        assert result.order is None
        m.assert_not_called()

    def test_asserted_price_refuses_if_quote_raises_even_in_warn_only(self, priced_session):
        # A caller that asserted expected_total is relying on verification; if
        # we cannot produce a quote, we must not place unverified.
        with override_settings(SPWIG_ENFORCE_QUOTE_DRIFT=False):
            with patch(QUOTE_FOR, side_effect=ValueError("pricing blew up")):
                with patch(CREATE_ORDER) as m:
                    result = OrderPlacementService.place_order(
                        PlacementRequest(
                            session=priced_session,
                            expected_total=Money(Decimal("25.00"), "USD"),
                        )
                    )

        assert result.ok is False
        assert result.order is None
        m.assert_not_called()
