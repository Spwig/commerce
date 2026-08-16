"""Reporting reads the current batch, reconciles, and never double-counts."""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from attribution.models import AttributionSettings, Campaign, TouchPoint
from attribution.services import reporting
from attribution.services.resolution import resolve_order
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db

User = get_user_model()


def _touch(user, channel, minutes_ago, campaign_ref=None):
    tp = TouchPoint.objects.create(
        visitor_key=f"vk-{user.pk}-{channel}-{minutes_ago}",
        customer=user,
        channel=channel,
        medium=channel,
        campaign_ref=campaign_ref,
    )
    TouchPoint.objects.filter(pk=tp.pk).update(
        occurred_at=timezone.now() - timedelta(minutes=minutes_ago)
    )
    tp.refresh_from_db()
    return tp


def _order(total="100.00", username="u"):
    user = User.objects.create_user(username=username, email=f"{username}@x.com", password="x")
    order = OrderFactory(user=user, status="processing", total_amount=Decimal(total))
    return order, user


def _set_model(name):
    s = AttributionSettings.get_settings()
    s.active_model = name
    s.save()


def test_revenue_by_channel_and_summary_reconcile():
    for i, ch in enumerate(["email", "organic_search", "paid_social"]):
        order, user = _order("100.00", username=f"u{i}")
        _touch(user, ch, 30)
        resolve_order(order)

    channels = {r["channel"]: r for r in reporting.revenue_by_channel()}
    assert channels["email"]["revenue"] == Decimal("100.00")
    assert channels["organic_search"]["revenue"] == Decimal("100.00")
    assert channels["paid_social"]["revenue"] == Decimal("100.00")
    assert channels["email"]["share_pct"] == Decimal("33.3")

    s = reporting.summary()
    assert s["attributed_revenue"] == Decimal("300.00")
    assert s["orders"] == 3


def test_revenue_by_campaign():
    campaign = Campaign.objects.create(name="Spring", slug="spring")
    order, user = _order("200.00", username="c1")
    _touch(user, "email", 30, campaign_ref=campaign)
    resolve_order(order)

    rows = reporting.revenue_by_campaign()
    assert len(rows) == 1
    assert rows[0]["slug"] == "spring"
    assert rows[0]["revenue"] == Decimal("200.00")


def test_model_switch_does_not_double_count():
    # Two touches; last-non-direct credits social, then switch to linear.
    _set_model("last_non_direct")
    order, user = _order("100.00", username="sw")
    _touch(user, "email", 90)
    _touch(user, "paid_social", 5)
    resolve_order(order)
    by_channel = {r["channel"]: r["revenue"] for r in reporting.revenue_by_channel()}
    assert by_channel == {"paid_social": Decimal("100.00")}

    _set_model("linear")
    resolve_order(order)
    by_channel = {r["channel"]: r["revenue"] for r in reporting.revenue_by_channel()}
    # Current batch is linear (50/50); the old last-non-direct batch is excluded.
    assert by_channel == {"email": Decimal("50.00"), "paid_social": Decimal("50.00")}
    assert reporting.summary()["attributed_revenue"] == Decimal("100.00")


def test_influenced_revenue_credits_every_touched_channel_fully():
    _set_model("linear")
    order, user = _order("100.00", username="inf")
    _touch(user, "email", 90)
    _touch(user, "paid_social", 5)
    resolve_order(order)

    influenced = {
        r["channel"]: r["influenced_revenue"] for r in reporting.influenced_revenue_by_channel()
    }
    # Both channels influenced the full £100 order (assisted lens exceeds 100%).
    assert influenced["email"] == Decimal("100.00")
    assert influenced["paid_social"] == Decimal("100.00")


def test_backfill_migration_marks_only_latest_batch_current():
    # Reproduces the pre-0003 corruption (every batch is_current=True) and proves
    # the backfill leaves exactly the newest batch current, so reporting no longer
    # double-counts. Covers the Codex-flagged migration data bug.
    import importlib

    from django.apps import apps as django_apps

    from attribution.models import Attribution

    order, user = _order("100.00", username="bf")
    _touch(user, "email", 30)
    resolve_order(order)
    v2 = resolve_order(order, force=True)  # second batch; resolver marks it current

    # Corrupt: mark every batch current (the buggy default=True state).
    Attribution.objects.filter(order=order).update(is_current=True)
    assert Attribution.objects.filter(order=order, is_current=True).count() == 2

    backfill = importlib.import_module("attribution.migrations.0003_backfill_is_current")
    backfill.mark_latest_batch_current(django_apps, None)

    current = Attribution.objects.filter(order=order, is_current=True)
    assert current.count() == 1
    assert current.first().model_version == v2
    assert reporting.summary()["attributed_revenue"] == Decimal("100.00")


def test_time_series_buckets_by_day():
    order, user = _order("100.00", username="ts")
    _touch(user, "email", 30)
    resolve_order(order)
    series = reporting.time_series(bucket="day")
    assert len(series) == 1
    assert series[0]["channel"] == "email"
    assert series[0]["revenue"] == Decimal("100.00")
