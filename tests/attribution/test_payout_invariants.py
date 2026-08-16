"""Payout regression gate for the affiliate/referral absorption (invariant #5).

Absorbing the affiliate and referral engines into the unified order-completion
orchestrator must NOT change what anyone is paid. Affiliate commissions have no
dedicated signal coverage in the repo, so this pins the current behaviour:
a commission is created on completion with the exact amount/currency/status,
and is reversed on a full refund. These tests must be green BEFORE the refactor
(against the existing affiliate signals) and remain green AFTER (against the
orchestrator) — byte-for-byte identical payout.

The referral side is already pinned by referrals/tests/test_signals.py (20
tests); this file adds the missing affiliate half.
"""

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from affiliate.models import (
    Affiliate,
    AffiliateProgramMembership,
    Click,
    Commission,
    Link,
    Program,
)
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db

User = get_user_model()


def _build_affiliate(commission_type="fixed", commission_value="10.00"):
    merchant = User.objects.create_user(username="merch", email="merch@example.com", password="x")
    program = Program.objects.create(
        name="Main",
        slug="main",
        merchant=merchant,
        commission_type=commission_type,
        commission_value=Decimal(commission_value),
        cookie_lifetime_days=30,
        status="active",
    )
    aff_user = User.objects.create_user(username="aff", email="aff@example.com", password="x")
    affiliate = Affiliate.objects.create(
        user=aff_user,
        affiliate_code="AFF123",
        payment_email="aff@example.com",
        status="active",
    )
    AffiliateProgramMembership.objects.create(
        affiliate=affiliate, program=program, status="approved"
    )
    link = Link.objects.create(
        affiliate=affiliate, program=program, destination_url="https://shop.example.com/"
    )
    return program, affiliate, link


def _click(link, cookie_value="cookie-abc"):
    return Click.objects.create(
        link=link,
        cookie_value=cookie_value,
        session_id="sess-1",
        ip_address="203.0.113.7",
        user_agent="Mozilla/5.0",
        referrer="",
    )


def test_fixed_commission_created_on_completed_order():
    program, affiliate, link = _build_affiliate("fixed", "10.00")
    _click(link)
    buyer = User.objects.create_user(username="buyer", email="buyer@example.com", password="x")

    # Completing the order triggers the affiliate signal (current behaviour).
    order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("100.00"))

    commissions = Commission.objects.filter(order=order)
    assert commissions.count() == 1
    c = commissions.first()
    assert c.affiliate_id == affiliate.id
    assert c.amount == Decimal("10.00")
    assert c.status == "pending"


def test_commission_reversed_on_full_refund():
    program, affiliate, link = _build_affiliate("fixed", "10.00")
    _click(link)
    buyer = User.objects.create_user(username="buyer2", email="buyer2@example.com", password="x")
    order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("100.00"))
    assert Commission.objects.get(order=order).status == "pending"

    order.status = "refunded"
    order.save()

    assert Commission.objects.get(order=order).status == "rejected"


def test_no_commission_without_a_click():
    _build_affiliate("fixed", "10.00")
    buyer = User.objects.create_user(username="buyer3", email="buyer3@example.com", password="x")
    order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("100.00"))
    assert Commission.objects.filter(order=order).count() == 0


def test_commission_not_created_twice_on_resave():
    program, affiliate, link = _build_affiliate("fixed", "10.00")
    _click(link)
    buyer = User.objects.create_user(username="buyer4", email="buyer4@example.com", password="x")
    order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("100.00"))
    # Re-save the completed order: must not double-credit.
    order.save()
    assert Commission.objects.filter(order=order).count() == 1
