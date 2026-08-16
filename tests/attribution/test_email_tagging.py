"""Email attribution tagging: only marketing links, internal-only, no double-tag.

The email rewriter runs on every email, so the risk here is over-tagging: a
transactional email (order confirmation, password reset) must never carry
attribution UTM, or it would create a spurious "email" touch that misattributes
the customer's next order. These tests pin the classifier and the URL logic.
"""

import pytest
from django.contrib.sites.models import Site
from django.test import override_settings

from email_system.models import EmailOutbox
from email_system.services.tracking_service import (
    TrackingService,
    is_marketing_template_type,
)

# --- Classifier (pure) ------------------------------------------------------


@pytest.mark.parametrize(
    "template_type,expected",
    [
        ("newsletter", True),
        ("cart_abandoned_1h", True),  # prefix
        ("cart_abandoned_discount", True),  # prefix
        ("back_in_stock", True),  # prefix
        ("wishlist_price_drop", True),
        ("loyalty_points_expiring", True),
        ("blog_post_published", True),  # broader scope
        ("review_request", True),  # broader scope
        ("account_welcome", True),  # broader scope
        # Transactional / system — must NOT be tagged
        ("order_confirmation", False),
        ("shipping_confirmation", False),
        ("refund_notification", False),
        ("password_reset", False),
        ("email_verification", False),
        ("admin_new_order", False),
        ("affiliate_commission_earned", False),
        ("wishlist_shared_confirmation", False),  # transactional wishlist
        ("back_in_stock_waitlist_confirmation", False),  # transactional (waitlist join ack)
        ("loyalty_points_earned", False),  # notification, not re-engagement
        ("", False),  # blank
        (None, False),
    ],
)
def test_is_marketing_template_type(template_type, expected):
    assert is_marketing_template_type(template_type) is expected


# --- URL tagging logic (pure, host passed in) -------------------------------

svc = TrackingService()
HOST = "shop.test"


def test_append_utm_internal_relative():
    out = svc._append_attribution_utm("/products/1", "newsletter", HOST)
    assert "utm_source=email" in out
    assert "utm_medium=email" in out
    assert "utm_campaign=newsletter" in out


def test_append_utm_internal_absolute_preserves_query():
    out = svc._append_attribution_utm("https://shop.test/p?ref=x", "newsletter", HOST)
    assert "ref=x" in out
    assert "utm_campaign=newsletter" in out


def test_append_utm_external_is_untouched():
    url = "https://external.com/x"
    assert svc._append_attribution_utm(url, "newsletter", HOST) == url


def test_append_utm_no_campaign_is_untouched():
    assert svc._append_attribution_utm("/p", None, HOST) == "/p"


def test_append_utm_never_double_tags():
    url = "/p?utm_source=affiliate&utm_medium=referral"
    assert svc._append_attribution_utm(url, "newsletter", HOST) == url


def test_append_utm_preserves_duplicate_query_keys():
    # Repeated keys (e.g. a category filter) must survive, not collapse to last.
    out = svc._append_attribution_utm("/shop?filter=a&filter=b", "newsletter", HOST)
    assert out.count("filter=a") == 1
    assert out.count("filter=b") == 1
    assert "utm_campaign=newsletter" in out


# --- End-to-end through the rewriter ---------------------------------------


@override_settings(SITE_URL="https://shop.test")
def test_link_rewriter_tags_only_internal_marketing_links():
    html = (
        '<a href="https://shop.test/products/1">p</a>'
        '<a href="/cart/">cart</a>'
        '<a href="https://external.com/x">ext</a>'
        '<a href="#top">anchor</a>'
    )
    out = svc._add_link_tracking(html, "tid-123", utm_campaign="newsletter")
    # Two internal links tagged (utm encoded inside the wrapped ?url= param).
    assert out.count("utm_source%3Demail") == 2
    # External link is wrapped for click tracking but NOT utm-tagged.
    assert "external.com" in out
    # Anchor untouched.
    assert 'href="#top"' in out


@override_settings(SITE_URL="https://shop.test")
def test_link_rewriter_no_tag_without_campaign():
    html = '<a href="/products/1">p</a>'
    out = svc._add_link_tracking(html, "tid-123", utm_campaign=None)
    assert "utm_source" not in out


# --- Campaign resolution from the outbox ------------------------------------


@pytest.mark.django_db
def test_attribution_campaign_from_outbox():
    site = Site.objects.get_current()

    def _outbox(tt):
        return EmailOutbox.objects.create(
            site=site,
            to_email="c@example.com",
            from_email="s@shop.test",
            subject="s",
            html_body="<a href='/p'>x</a>",
            template_type=tt,
        )

    svc2 = TrackingService()
    assert svc2._attribution_campaign(_outbox("newsletter").id) == "newsletter"
    assert svc2._attribution_campaign(_outbox("order_confirmation").id) is None
    assert svc2._attribution_campaign(_outbox("").id) is None
