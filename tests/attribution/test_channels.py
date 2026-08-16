"""Channel resolution is a pure function of the extracted signal.

These assert the collision hierarchy (constants.CHANNEL_PRIORITY) made concrete
in services.channels.resolve_channel — no DB, no request.
"""

from attribution.constants import (
    CHANNEL_CAMPAIGN,
    CHANNEL_DIRECT,
    CHANNEL_EMAIL,
    CHANNEL_ORGANIC_SEARCH,
    CHANNEL_ORGANIC_SOCIAL,
    CHANNEL_PAID_SEARCH,
    CHANNEL_PAID_SOCIAL,
    CHANNEL_REFERRAL_EXTERNAL,
)
from attribution.services.channels import resolve_channel


def test_gclid_is_paid_search():
    assert resolve_channel(gclid="abc123") == CHANNEL_PAID_SEARCH


def test_fbclid_is_paid_social():
    assert resolve_channel(fbclid="xyz") == CHANNEL_PAID_SOCIAL


def test_paid_click_id_beats_organic_referrer():
    # Collision: a Google referrer AND a gclid — paid wins.
    assert resolve_channel(gclid="g", referrer_host="www.google.com") == CHANNEL_PAID_SEARCH


def test_email_medium():
    assert resolve_channel(utm_medium="email", utm_source="newsletter") == CHANNEL_EMAIL


def test_cpc_medium_is_paid_search():
    assert resolve_channel(utm_medium="cpc", utm_source="google") == CHANNEL_PAID_SEARCH


def test_organic_social_medium():
    assert resolve_channel(utm_medium="social", utm_source="instagram") == CHANNEL_ORGANIC_SOCIAL


def test_bare_campaign_tag_is_campaign():
    assert resolve_channel(utm_campaign="spring_sale") == CHANNEL_CAMPAIGN


def test_search_engine_referrer_is_organic_search():
    assert resolve_channel(referrer_host="www.google.com") == CHANNEL_ORGANIC_SEARCH


def test_social_referrer_is_organic_social():
    assert resolve_channel(referrer_host="l.facebook.com") == CHANNEL_ORGANIC_SOCIAL


def test_other_external_referrer_is_referral_external():
    assert resolve_channel(referrer_host="someblog.com") == CHANNEL_REFERRAL_EXTERNAL


def test_internal_referrer_is_direct():
    # Own-site navigation carries no attribution signal.
    assert resolve_channel(referrer_host="myshop.com", referrer_is_internal=True) == CHANNEL_DIRECT


def test_nothing_is_direct():
    assert resolve_channel() == CHANNEL_DIRECT
