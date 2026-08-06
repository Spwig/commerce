"""Unit tests for the Footprint JSON contract (to_dict / from_dict).

Pure — no Django, no DB. The oracle-parity tests only round-trip an order + one
line, so most of ``from_dict``'s per-collection reconstruction is otherwise
untested and could regress silently. This exercises **every** collection and
every record field through a real ``json.dumps`` → ``json.loads`` → ``from_dict``
cycle and asserts dataclass equality — the exact wire path ``HttpBackend`` uses.
"""

import json
from decimal import Decimal

import pytest

from commerce_footprint.footprint import (
    Amount,
    BookingLineRecord,
    EmailRecord,
    Footprint,
    GiftCardEventRecord,
    IntentRecord,
    OrderLineRecord,
    OrderRecord,
    PaymentRecord,
    StockMovementRecord,
    StockStateRecord,
    VoucherUsageRecord,
    WebhookRecord,
)


def _usd(value: str) -> Amount:
    return Amount(Decimal(value), "USD")


def _full_footprint() -> Footprint:
    """A footprint with every collection non-empty and >1 element where it
    matters, plus edge values (a EUR amount, a null reference_key, empty tags)."""
    return Footprint(
        correlation="ORD-DEADBEEF01",
        orders=(
            OrderRecord(
                number="ORD-DEADBEEF01",
                email="buyer@example.test",
                status="processing",
                payment_status="partially_refunded",
                subtotal=_usd("40.00"),
                tax=_usd("3.20"),
                shipping=_usd("5.99"),
                discount=_usd("5.00"),
                gift_card_discount=_usd("10.00"),
                total=_usd("34.19"),
                amount_paid=_usd("34.19"),
                amount_refunded=_usd("4.19"),
                lines=(
                    OrderLineRecord(
                        sku="SKU-1",
                        name="Widget",
                        quantity=2,
                        unit_price=_usd("10.00"),
                        line_total=_usd("20.00"),
                        variant_sku="SKU-1-M",
                        configuration=(("slot-color", ("opt-red",)), ("slot-size", ("opt-l",))),
                        customization_token="design-tok-123",
                        customizations=(("42", "Happy Birthday"), ("43", "Gold")),
                    ),
                    OrderLineRecord(
                        sku="SKU-2",
                        name="Gadget",
                        quantity=1,
                        unit_price=_usd("20.00"),
                        line_total=_usd("20.00"),
                        is_bundle_component=True,
                        gift_card_recipient="giftee@example.test",
                        booking=BookingLineRecord(
                            start="2026-09-01T10:00:00+00:00",
                            end="2026-09-01T12:00:00+00:00",
                            resource_id=7,
                            persons=(("adult", 2), ("child", 1)),
                            status="confirmed",
                        ),
                    ),
                ),
            ),
        ),
        payments=(
            PaymentRecord(
                reference="txn-1",
                transaction_type="charge",
                tender_type="gateway",
                status="completed",
                amount=_usd("24.19"),
                provider_transaction_id="pi_abc",
            ),
            PaymentRecord(
                reference="txn-2",
                transaction_type="refund",
                tender_type="gateway",
                status="completed",
                amount=_usd("4.19"),  # provider id defaulted
            ),
        ),
        intents=(IntentRecord(reference="pi_abc", status="succeeded", amount=_usd("24.19")),),
        stock_movements=(
            StockMovementRecord(
                stock_item_id=7,
                movement_type="adjustment",
                quantity=-2,
                previous_quantity=10,
                new_quantity=8,
                reference_key="idem-1",
            ),
            StockMovementRecord(
                stock_item_id=7,
                movement_type="return",
                quantity=1,
                previous_quantity=8,
                new_quantity=9,
                reference_key=None,  # null key
            ),
        ),
        stock_state=(StockStateRecord(stock_item_id=7, on_hand=9, allocated=1, available=8),),
        gift_card_events=(
            GiftCardEventRecord(
                gift_card_code="GIFT10",
                transaction_type="redemption",
                amount=_usd("10.00"),
                balance_after=_usd("0.00"),
            ),
        ),
        voucher_usages=(
            VoucherUsageRecord(
                voucher_code="SAVE5", discount_amount=_usd("5.00"), cart_total=_usd("40.00")
            ),
        ),
        emails=(
            EmailRecord(
                to_email="buyer@example.test",
                template_type="order_confirmation",
                subject="Your order",
                status="sent",
                tags=("order", "transactional"),
            ),
            EmailRecord(
                to_email="buyer@example.test",
                template_type="refund",
                subject="Refund issued",
                status="sent",
                tags=(),  # empty tags
            ),
        ),
        webhooks=(
            WebhookRecord(
                provider_slug="test_gateway",
                event_id="evt-1",
                event_type="payment.succeeded",
                processed=True,
            ),
        ),
    )


def test_full_footprint_survives_json_round_trip():
    fp = _full_footprint()
    # Through actual JSON, not just the dict — proves everything is JSON-safe
    # (Decimals became strings, tuples became lists and back).
    rebuilt = Footprint.from_dict(json.loads(json.dumps(fp.to_dict())))
    assert rebuilt == fp


def test_amounts_keep_exact_decimal_across_the_wire():
    fp = _full_footprint()
    rebuilt = Footprint.from_dict(json.loads(json.dumps(fp.to_dict())))
    # A cent-precise value that a float encoding would corrupt.
    assert rebuilt.orders[0].amount_refunded == _usd("4.19")
    assert rebuilt.orders[0].total.value == Decimal("34.19")


@pytest.mark.parametrize(
    "missing",
    [
        "orders",
        "payments",
        "intents",
        "stock_movements",
        "stock_state",
        "gift_card_events",
        "voucher_usages",
        "emails",
        "webhooks",
    ],
)
def test_from_dict_requires_every_top_level_collection(missing):
    """A payload missing any top-level collection fails loudly (KeyError) rather
    than reconstructing a silently-empty-in-that-dimension footprint — the wire
    contract the HttpBackend relies on to not pass assertions vacuously."""
    wire = _full_footprint().to_dict()
    del wire[missing]
    with pytest.raises(KeyError):
        Footprint.from_dict(wire)
