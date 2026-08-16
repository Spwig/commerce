"""Resolver correctness — reconciliation, the five models, refunds, versioning."""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.db.models import Sum
from django.utils import timezone

from attribution.models import Attribution, AttributionSettings, TouchPoint
from attribution.services.resolution import resolve_order
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db


def _touch(user, channel, minutes_ago):
    tp = TouchPoint.objects.create(
        visitor_key=f"vk-{channel}-{minutes_ago}",
        customer=user,
        channel=channel,
        medium=channel,
    )
    # occurred_at is auto_now_add; rewrite it to place the touch in the past.
    TouchPoint.objects.filter(pk=tp.pk).update(
        occurred_at=timezone.now() - timedelta(minutes=minutes_ago)
    )
    tp.refresh_from_db()
    return tp


def _order(total="100.00", user=None):
    kwargs = {
        "status": "processing",
        "total_amount": Decimal(total),
        "amount_refunded": Decimal("0.00"),
    }
    if user is not None:
        kwargs["user"] = user
    return OrderFactory(**kwargs)


def _set_model(name):
    s = AttributionSettings.get_settings()
    s.active_model = name
    s.save()


def _primary_sum(order, version=None):
    qs = Attribution.objects.filter(order=order, role="primary")
    if version:
        qs = qs.filter(model_version=version)
    return qs.aggregate(s=Sum("amount"))["s"] or Decimal("0")


def _versions(order):
    return list(
        Attribution.objects.filter(order=order)
        .order_by()
        .values_list("model_version", flat=True)
        .distinct()
    )


# --- Reconciliation invariant (the one that earns merchant trust) ----------


def test_single_touch_gets_full_revenue():
    order = _order("100.00")
    _touch(order.user, "email", 60)
    resolve_order(order)
    rows = Attribution.objects.filter(order=order, role="primary")
    assert rows.count() == 1
    assert rows.first().weight == Decimal("1")
    assert _primary_sum(order) == Decimal("100.00")


def test_reconciles_exactly_on_indivisible_split():
    # 100 / 3 does not divide evenly; the batch must still sum to exactly 100.
    _set_model("linear")
    order = _order("100.00")
    for ch, m in [("email", 30), ("organic_search", 20), ("organic_social", 10)]:
        _touch(order.user, ch, m)
    resolve_order(order)
    amounts = sorted(Attribution.objects.filter(order=order).values_list("amount", flat=True))
    assert amounts == [Decimal("33.33"), Decimal("33.33"), Decimal("33.34")]
    assert _primary_sum(order) == Decimal("100.00")


# --- The five models -------------------------------------------------------


def test_last_non_direct_credits_most_recent_touch():
    _set_model("last_non_direct")
    order = _order("100.00")
    _touch(order.user, "email", 90)
    _touch(order.user, "organic_search", 60)
    last = _touch(order.user, "paid_social", 5)
    resolve_order(order)
    winner = Attribution.objects.get(order=order, weight=Decimal("1"))
    assert winner.touchpoint_id == last.id
    assert winner.channel == "paid_social"


def test_first_touch_credits_earliest_touch():
    _set_model("first_touch")
    order = _order("100.00")
    first = _touch(order.user, "email", 90)
    _touch(order.user, "organic_search", 60)
    _touch(order.user, "paid_social", 5)
    resolve_order(order)
    winner = Attribution.objects.get(order=order, weight=Decimal("1"))
    assert winner.touchpoint_id == first.id


def test_linear_splits_evenly():
    _set_model("linear")
    order = _order("100.00")
    for ch, m in [("email", 40), ("organic_search", 30), ("paid_social", 20), ("referral", 10)]:
        _touch(order.user, ch, m)
    resolve_order(order)
    amounts = list(Attribution.objects.filter(order=order).values_list("amount", flat=True))
    assert all(a == Decimal("25.00") for a in amounts)
    assert _primary_sum(order) == Decimal("100.00")


def test_position_based_40_20_40():
    _set_model("position_based")
    order = _order("100.00")
    first = _touch(order.user, "email", 90)
    mid = _touch(order.user, "organic_search", 60)
    last = _touch(order.user, "paid_social", 5)
    resolve_order(order)
    by_touch = {a.touchpoint_id: a.amount for a in Attribution.objects.filter(order=order)}
    assert by_touch[first.id] == Decimal("40.00")
    assert by_touch[mid.id] == Decimal("20.00")
    assert by_touch[last.id] == Decimal("40.00")
    assert _primary_sum(order) == Decimal("100.00")


def test_time_decay_favours_recent():
    _set_model("time_decay")
    order = _order("100.00")
    old = _touch(order.user, "email", 60 * 24 * 14)  # 14 days ago
    recent = _touch(order.user, "paid_social", 60)  # 1 hour ago
    resolve_order(order)
    a_old = Attribution.objects.get(order=order, touchpoint=old)
    a_recent = Attribution.objects.get(order=order, touchpoint=recent)
    assert a_recent.amount > a_old.amount
    assert _primary_sum(order) == Decimal("100.00")


# --- Refunds, idempotency, versioning --------------------------------------


def test_partial_refund_prorates_to_net_on_reresolution():
    order = _order("100.00")
    _touch(order.user, "email", 60)
    v1 = resolve_order(order)
    assert _primary_sum(order, v1) == Decimal("100.00")

    # A £30 refund lands; net drops to £70.
    order.amount_refunded = Decimal("30.00")
    order.save(update_fields=["amount_refunded"])
    v2 = resolve_order(order)

    assert v2 != v1
    assert len(_versions(order)) == 2  # prior batch retained (forward-only)
    assert _primary_sum(order, v2) == Decimal("70.00")


def test_full_refund_zeroes_attribution():
    order = _order("100.00")
    _touch(order.user, "email", 60)
    resolve_order(order)
    order.amount_refunded = Decimal("100.00")
    order.save(update_fields=["amount_refunded"])
    v2 = resolve_order(order)
    assert _primary_sum(order, v2) == Decimal("0.00")


def test_resolution_is_idempotent_when_nothing_changed():
    order = _order("100.00")
    _touch(order.user, "email", 60)
    v1 = resolve_order(order)
    v2 = resolve_order(order)  # no change → no-op, same version
    assert v1 == v2
    assert len(_versions(order)) == 1


def test_model_switch_writes_new_batch_and_recomputes():
    _set_model("last_non_direct")
    order = _order("100.00")
    _touch(order.user, "email", 90)
    _touch(order.user, "paid_social", 5)
    resolve_order(order)

    _set_model("linear")
    resolve_order(order)

    versions = _versions(order)
    assert len(versions) == 2
    # Newest batch is linear: two rows of 50.
    linear_version = [v for v in versions if v.startswith("linear")][0]
    amounts = list(
        Attribution.objects.filter(order=order, model_version=linear_version).values_list(
            "amount", flat=True
        )
    )
    assert sorted(amounts) == [Decimal("50.00"), Decimal("50.00")]


def test_customer_order_with_no_touches_is_attributed_to_direct():
    # Reconciliation invariant holds store-wide: an order with no tracked touches
    # (pure direct/typed/bookmark) still produces a full-revenue Direct row.
    order = _order("100.00")
    version = resolve_order(order)
    assert version is not None
    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "direct"
    assert row.touchpoint_id is None
    assert row.amount == Decimal("100.00")
    assert _primary_sum(order) == Decimal("100.00")


def test_guest_order_is_attributed_to_direct():
    # A guest (no customer, stream not yet stitched) must not vanish from
    # attribution — its revenue lands in Direct until a later stitch reclassifies.
    order = _order("100.00")
    order.user = None
    order.save(update_fields=["user"])
    version = resolve_order(order)
    assert version is not None
    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "direct"
    assert row.amount == Decimal("100.00")


def test_direct_order_reclassified_when_touch_appears():
    # If a touch later stitches in and we re-resolve, Direct is superseded by the
    # real channel (forward-only: prior Direct batch retained).
    order = _order("100.00")
    v1 = resolve_order(order)
    assert Attribution.objects.get(order=order, model_version=v1).channel == "direct"

    _touch(order.user, "email", 30)
    v2 = resolve_order(order)
    assert v2 != v1
    latest = Attribution.objects.filter(order=order, model_version=v2)
    assert latest.count() == 1
    assert latest.first().channel == "email"
    assert _primary_sum(order, v2) == Decimal("100.00")
