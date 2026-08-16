"""Voucher-as-attribution-key: a campaign-linked code REDEEMED on an order
credits its campaign — but a code merely applied and then removed does not.

Crediting happens at order time from VoucherUsage (not at cart-apply), so
apply-then-remove can't misattribute (Codex review).
"""

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from attribution.models import Attribution, Campaign, TouchPoint
from tests.factories import OrderFactory
from vouchers.models import VoucherUsage
from vouchers.tests.factories import make_voucher

pytestmark = pytest.mark.django_db

User = get_user_model()


def _use_voucher(voucher, user, order):
    return VoucherUsage.objects.create(
        voucher=voucher,
        user=user,
        order=order,
        discount_amount=Decimal("10.00"),
        cart_total=Decimal("100.00"),
    )


def _complete(order):
    order.status = "completed"
    order.save()


def test_redeemed_campaign_voucher_attributes_order_to_campaign():
    campaign = Campaign.objects.create(name="Influencer Jo", slug="jo")
    voucher = make_voucher("JO10", attribution_campaign=campaign)
    user = User.objects.create_user(username="b", email="b@example.com", password="x")

    order = OrderFactory(user=user, status="processing", total_amount=Decimal("100.00"))
    _use_voucher(voucher, user, order)
    _complete(order)  # fires the orchestrator

    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "campaign"
    assert row.campaign_ref_id == campaign.id
    assert row.amount == Decimal("100.00")


def test_applied_then_removed_voucher_does_not_credit():
    # No VoucherUsage row (code removed before checkout) => order is Direct.
    campaign = Campaign.objects.create(name="Jo", slug="jo")
    make_voucher("JO10", attribution_campaign=campaign)
    user = User.objects.create_user(username="b2", email="b2@example.com", password="x")

    order = OrderFactory(user=user, status="completed", total_amount=Decimal("100.00"))

    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "direct"


def test_voucher_without_campaign_is_not_credited():
    voucher = make_voucher("PLAIN10")  # no attribution_campaign
    user = User.objects.create_user(username="b3", email="b3@example.com", password="x")
    order = OrderFactory(user=user, status="processing", total_amount=Decimal("100.00"))
    _use_voucher(voucher, user, order)
    _complete(order)

    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "direct"
    assert TouchPoint.objects.filter(channel="campaign").count() == 0


def test_voucher_crediting_is_idempotent():
    campaign = Campaign.objects.create(name="Jo", slug="jo")
    voucher = make_voucher("JO10", attribution_campaign=campaign)
    user = User.objects.create_user(username="b4", email="b4@example.com", password="x")
    order = OrderFactory(user=user, status="processing", total_amount=Decimal("100.00"))
    _use_voucher(voucher, user, order)
    _complete(order)
    order.save()  # re-fire orchestrator

    assert TouchPoint.objects.filter(visitor_key=f"voucher:{order.pk}:{campaign.pk}").count() == 1
