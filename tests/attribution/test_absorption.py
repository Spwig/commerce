"""Absorption: affiliate/referral clicks surface as their own channel, and the
unified orchestrator populates Order.source.

Complements the payout gate (test_payout_invariants.py): that proves payout is
unchanged; this proves affiliate/referral revenue now *also* appears in the
unified attribution reporting, which is the whole point of absorbing them.
"""

import json
from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory
from django.utils import timezone

from affiliate.models import Affiliate, AffiliateProgramMembership, Click, Link, Program
from attribution.models import Attribution, TouchPoint
from attribution.services import identity
from attribution.services.capture import record_channel_touch
from core.models import SiteSettings
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture(autouse=True)
def _enable_consent_banner():
    ss = SiteSettings.get_settings()
    ss.cookie_consent_enabled = True
    ss.save(update_fields=["cookie_consent_enabled"])
    yield


def _request(consent=True):
    req = RequestFactory().get("/go/", HTTP_USER_AGENT="Mozilla/5.0")
    req.session = SessionStore()
    req.session.create()
    req.user = AnonymousUser()
    if consent:
        req.COOKIES["spwig_cookie_consent"] = json.dumps({"analytics": True})
    return req


def _affiliate_click():
    merchant = User.objects.create_user(username="m", email="m@example.com", password="x")
    program = Program.objects.create(
        name="P",
        slug="p",
        merchant=merchant,
        commission_type="fixed",
        commission_value=Decimal("5.00"),
        status="active",
    )
    aff_user = User.objects.create_user(username="a", email="a@example.com", password="x")
    affiliate = Affiliate.objects.create(
        user=aff_user, affiliate_code="AFFX", payment_email="a@example.com", status="active"
    )
    AffiliateProgramMembership.objects.create(
        affiliate=affiliate, program=program, status="approved"
    )
    link = Link.objects.create(
        affiliate=affiliate, program=program, destination_url="https://s.example.com/"
    )
    return Click.objects.create(
        link=link,
        cookie_value="cv1",
        session_id="s",
        ip_address="203.0.113.7",
        user_agent="Mozilla/5.0",
    )


def test_record_channel_touch_creates_affiliate_touch():
    click = _affiliate_click()
    touch = record_channel_touch(_request(), "affiliate", affiliate_click=click)
    assert touch is not None
    assert touch.channel == "affiliate"
    assert touch.affiliate_click_id == click.id


def test_channel_touch_respects_consent():
    click = _affiliate_click()
    assert record_channel_touch(_request(consent=False), "affiliate", affiliate_click=click) is None
    assert TouchPoint.objects.count() == 0


def test_affiliate_order_attributes_to_affiliate_channel_and_sets_source():
    click = _affiliate_click()
    req = _request()
    touch = record_channel_touch(req, "affiliate", affiliate_click=click)
    # Backdate so the touch precedes the order.
    TouchPoint.objects.filter(pk=touch.pk).update(occurred_at=timezone.now() - timedelta(minutes=5))

    buyer = User.objects.create_user(username="buyer", email="buyer@example.com", password="x")
    identity.bind_customer(req.attribution_visitor_key, buyer)

    # Completing the order fires the unified orchestrator.
    order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("100.00"))

    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "affiliate"
    assert row.amount == Decimal("100.00")
    order.refresh_from_db()
    assert order.source == "referral"  # affiliate maps to the 'referral' source bucket


def test_logged_out_affiliate_click_binds_at_checkout(monkeypatch):
    # Codex-flagged gap: a shopper who clicks an affiliate link while logged out
    # and then checks out must NOT be reported as Direct. The orchestrator binds
    # the visitor stream to the order's customer at resolution time via the
    # thread-local request, so the anonymous affiliate touch attributes.
    click = _affiliate_click()
    req = _request()
    touch = record_channel_touch(req, "affiliate", affiliate_click=click)
    TouchPoint.objects.filter(pk=touch.pk).update(occurred_at=timezone.now() - timedelta(minutes=5))
    assert touch.customer_id is None  # captured anonymously

    buyer = User.objects.create_user(username="guest", email="guest@example.com", password="x")

    # Simulate the checkout request carrying the visitor cookie, exposed via the
    # same thread-local the referral middleware populates.
    from threading import current_thread

    checkout_req = RequestFactory().get("/checkout/")
    checkout_req.COOKIES[identity.VISITOR_COOKIE] = req.attribution_visitor_key
    current_thread().request = checkout_req
    try:
        order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("80.00"))
    finally:
        delattr(current_thread(), "request")

    row = Attribution.objects.get(order=order, role="primary")
    assert row.channel == "affiliate"  # not "direct"
    assert row.amount == Decimal("80.00")


def test_direct_order_sets_source_direct():
    buyer = User.objects.create_user(username="b2", email="b2@example.com", password="x")
    order = OrderFactory(user=buyer, status="completed", total_amount=Decimal("50.00"))
    order.refresh_from_db()
    assert order.source == "direct"
