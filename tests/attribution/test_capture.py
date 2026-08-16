"""Capture writes a raw touch only when warranted and consented."""

import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory

from attribution.models import Campaign, TouchPoint, VisitorThread
from attribution.services import capture
from core.models import SiteSettings

pytestmark = pytest.mark.django_db


def _consent_cookie(analytics=True):
    return json.dumps({"necessary": True, "analytics": analytics, "marketing": False})


def _request(path="/products/", params=None, ua="Mozilla/5.0", consent=True, referer=None):
    rf = RequestFactory()
    extra = {"HTTP_USER_AGENT": ua}
    if referer:
        extra["HTTP_REFERER"] = referer
    req = rf.get(path, params or {}, **extra)
    req.session = SessionStore()
    req.session.create()
    req.user = AnonymousUser()
    if consent is not None:
        req.COOKIES["spwig_cookie_consent"] = _consent_cookie(consent)
    return req


@pytest.fixture(autouse=True)
def _enable_consent_banner():
    # Exercise the real gate: banner ON, so capture requires analytics consent.
    ss = SiteSettings.get_settings()
    ss.cookie_consent_enabled = True
    ss.save(update_fields=["cookie_consent_enabled"])
    yield


def test_tagged_email_arrival_is_captured_and_linked_to_campaign():
    Campaign.objects.create(name="Spring Sale", slug="spring-sale")
    req = _request(
        params={"utm_source": "news", "utm_medium": "email", "utm_campaign": "spring-sale"}
    )

    touch = capture.record_touch(req)

    assert touch is not None
    assert touch.channel == "email"
    assert touch.source == "news"
    assert touch.campaign_ref is not None
    assert touch.campaign_ref.slug == "spring-sale"
    # A visitor key + thread are established.
    assert req.attribution_visitor_key
    assert VisitorThread.objects.filter(visitor_key=req.attribution_visitor_key).exists()


def test_unknown_campaign_slug_still_captures_raw_string():
    req = _request(params={"utm_source": "news", "utm_medium": "email", "utm_campaign": "ghost"})
    touch = capture.record_touch(req)
    assert touch is not None
    assert touch.campaign == "ghost"
    assert touch.campaign_ref is None  # no data loss even without a Campaign row


def test_direct_navigation_is_not_recorded():
    assert capture.record_touch(_request(path="/", params={})) is None
    assert TouchPoint.objects.count() == 0


def test_bot_is_not_recorded():
    req = _request(params={"utm_source": "x"}, ua="Googlebot/2.1")
    assert capture.record_touch(req) is None


def test_external_referrer_classified():
    req = _request(referer="https://someblog.com/post")
    touch = capture.record_touch(req)
    assert touch is not None
    assert touch.channel == "referral_external"


def test_search_referrer_is_organic_search():
    req = _request(referer="https://www.google.com/search?q=shoes")
    touch = capture.record_touch(req)
    assert touch.channel == "organic_search"


def test_consent_denied_blocks_capture():
    req = _request(params={"utm_source": "x", "utm_medium": "email"}, consent=False)
    assert capture.record_touch(req) is None
    assert TouchPoint.objects.count() == 0


def test_no_consent_cookie_blocks_capture_when_banner_enabled():
    req = _request(params={"utm_source": "x", "utm_medium": "email"}, consent=None)
    assert capture.record_touch(req) is None


def test_admin_and_api_paths_are_skipped():
    assert capture.record_touch(_request(path="/admin/", params={"utm_source": "x"})) is None
    assert capture.record_touch(_request(path="/en/admin/", params={"utm_source": "x"})) is None
    assert capture.record_touch(_request(path="/api/cart/", params={"utm_source": "x"})) is None
