"""What-if preview: all-model compute that reconciles with the stored numbers."""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone

from attribution.models import AttributionSettings, TouchPoint
from attribution.services import reporting
from attribution.services.preview import journeys, preview_by_model
from attribution.services.resolution import resolve_order
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db

User = get_user_model()


def _touch(user, channel, minutes_ago):
    tp = TouchPoint.objects.create(
        visitor_key=f"vk-{user.pk}-{channel}-{minutes_ago}",
        customer=user,
        channel=channel,
        medium=channel,
    )
    TouchPoint.objects.filter(pk=tp.pk).update(
        occurred_at=timezone.now() - timedelta(minutes=minutes_ago)
    )
    tp.refresh_from_db()
    return tp


def _order(total, username):
    user = User.objects.create_user(username=username, email=f"{username}@x.com", password="x")
    return OrderFactory(user=user, status="processing", total_amount=Decimal(total)), user


def _set_model(name):
    s = AttributionSettings.get_settings()
    s.active_model = name
    s.save()


def _scenario():
    # A: email(90m) then paid_social(5m); B: organic_search only; C: no touches (direct)
    oa, ua = _order("100.00", "ua")
    _touch(ua, "email", 90)
    _touch(ua, "paid_social", 5)
    resolve_order(oa)
    ob, ub = _order("100.00", "ub")
    _touch(ub, "organic_search", 30)
    resolve_order(ob)
    oc, _uc = _order("100.00", "uc")
    resolve_order(oc)  # direct fallback


def _chan(p, model):
    return {c["channel"]: c["revenue"] for c in p["by_model"][model]["channels"]}


def test_preview_reconciles_with_summary():
    _set_model("last_non_direct")
    _scenario()
    p = preview_by_model(use_cache=False)
    assert p["totals"]["attributed"] == Decimal("300.00")
    assert p["totals"]["attributed"] == reporting.summary()["attributed_revenue"]


def test_active_model_matches_stored_channels():
    _set_model("last_non_direct")
    _scenario()
    p = preview_by_model(use_cache=False)
    preview_active = _chan(p, "last_non_direct")
    stored = {c["channel"]: c["revenue"] for c in reporting.revenue_by_channel()}
    assert preview_active == stored
    assert stored == {
        "paid_social": Decimal("100.00"),
        "organic_search": Decimal("100.00"),
        "direct": Decimal("100.00"),
    }


def test_every_model_total_reconciles_to_net():
    _set_model("last_non_direct")
    _scenario()
    p = preview_by_model(use_cache=False)
    for m in p["models"]:
        total = sum(c["revenue"] for c in p["by_model"][m]["channels"])
        assert total == Decimal("300.00"), m


def test_models_credit_differently():
    _set_model("last_non_direct")
    _scenario()
    p = preview_by_model(use_cache=False)
    # Last touch: order A -> paid_social; email absent.
    last = _chan(p, "last_non_direct")
    assert last.get("paid_social") == Decimal("100.00")
    assert "email" not in last
    # First touch: order A -> email.
    first = _chan(p, "first_touch")
    assert first.get("email") == Decimal("100.00")
    assert "paid_social" not in first
    # Linear: order A splits 50/50.
    linear = _chan(p, "linear")
    assert linear.get("email") == Decimal("50.00")
    assert linear.get("paid_social") == Decimal("50.00")


def test_direct_order_credited_in_every_model():
    _set_model("last_non_direct")
    _scenario()
    p = preview_by_model(use_cache=False)
    for m in p["models"]:
        assert _chan(p, m).get("direct") == Decimal("100.00"), m


def test_journeys_aggregates_first_to_last():
    _set_model("last_non_direct")
    _scenario()
    flows = {(f["from"], f["to"]): f["revenue"] for f in journeys()}
    assert flows[("email", "paid_social")] == Decimal("100.00")
    assert flows[("organic_search", "organic_search")] == Decimal("100.00")
    assert flows[("direct", "direct")] == Decimal("100.00")


def test_fractional_cent_split_matches_stored_exactly():
    # 3-touch linear split of £100 -> 33.33 / 33.33 / 33.34 (drift on last).
    # Preview must quantize + reconcile per order like the resolver, not sum raw.
    _set_model("linear")
    o, u = _order("100.00", "frac")
    _touch(u, "email", 90)
    _touch(u, "organic_search", 60)
    _touch(u, "paid_social", 30)
    resolve_order(o)

    p = preview_by_model(use_cache=False)
    preview_active = _chan(p, "linear")
    stored = {c["channel"]: c["revenue"] for c in reporting.revenue_by_channel()}
    assert preview_active == stored
    assert sum(preview_active.values()) == Decimal("100.00")
    assert set(preview_active.values()) == {Decimal("33.33"), Decimal("33.34")}


def test_cache_busts_when_active_model_changes():
    _set_model("last_non_direct")
    _scenario()
    p1 = preview_by_model(use_cache=True)
    assert p1["active_model"] == "last_non_direct"
    # Changing the model must not serve a stale cached payload.
    _set_model("linear")
    p2 = preview_by_model(use_cache=True)
    assert p2["active_model"] == "linear"


@override_settings(ATTRIBUTION_PREVIEW_MAX_ORDERS=1)
def test_truncation_guard_serves_canonical_only():
    _set_model("last_non_direct")
    _scenario()  # 3 orders > cap of 1
    p = preview_by_model(use_cache=False)
    assert p["truncated"] is True
    assert p["truncated_count"] == 3
    # Only the stored/active model is present.
    assert list(p["by_model"].keys()) == ["last_non_direct"]
    assert p["totals"]["attributed"] == Decimal("300.00")
