"""Blog social auto-share links carry social attribution UTM (and are absolute)."""

from types import SimpleNamespace

import pytest

from blog.tasks import _social_share_url

pytestmark = pytest.mark.django_db


def test_social_share_url_tags_and_absolutizes():
    post = SimpleNamespace(get_absolute_url=lambda: "/blog/my-post/", slug="my-post")
    account = SimpleNamespace(provider_key="facebook_page")

    url = _social_share_url(post, account)

    assert url.startswith("https://")  # absolute, not the relative get_absolute_url
    assert "/blog/my-post/" in url
    assert "utm_source=facebook_page" in url
    assert "utm_medium=social" in url
    assert "utm_campaign=blog_my-post" in url


def test_social_share_url_falls_back_to_social_source():
    post = SimpleNamespace(get_absolute_url=lambda: "/blog/x/", slug="x")
    account = SimpleNamespace(provider_key="")

    url = _social_share_url(post, account)
    assert "utm_source=social" in url
