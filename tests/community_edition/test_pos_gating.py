"""
POS gating for the Community edition.

Under Community: ``pos_license_is_valid()`` returns False regardless of any
sandbox state or configured POS licence key. The upgrade CTA replaces the
POS UI.
"""

from unittest.mock import patch

import pytest


def test_pos_is_locked_for_community_edition():
    """Community licence → POS gate returns False."""
    from django.core.cache import cache

    from pos_app.license import pos_license_is_valid, POS_LICENSE_CACHE_KEY

    cache.delete(POS_LICENSE_CACHE_KEY)

    with patch("core.license.get_license_manager") as get_lm:
        get_lm.return_value.is_community.return_value = True
        assert pos_license_is_valid() is False


def test_pos_unlocks_under_sandbox_when_not_community():
    """Explicit dev/staging sandbox still unlocks POS (safety net for internal use)."""
    from django.core.cache import cache

    from pos_app.license import pos_license_is_valid, POS_LICENSE_CACHE_KEY

    cache.delete(POS_LICENSE_CACHE_KEY)

    with patch("core.license.get_license_manager") as get_lm, patch(
        "core.license.is_sandbox_mode", return_value=True
    ):
        get_lm.return_value.is_community.return_value = False
        assert pos_license_is_valid() is True


@pytest.mark.django_db
def test_pos_upgrade_view_renders():
    """The upgrade CTA view renders successfully.

    Uses RequestFactory + a minimal SiteSettings row so the context
    processors that read from SiteSettings don't error. This avoids
    pulling in the full setup wizard middleware.
    """
    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory

    from core.models import SiteSettings
    from pos_app.community_gate import pos_upgrade_required_view

    # Ensure a singleton SiteSettings row exists (required by context processors)
    SiteSettings.objects.get_or_create(
        pk=1, defaults={"admin_email": "admin@example.com"}
    )

    # The view is @staff_member_required (defence in depth on the routed
    # URL). The middleware always invokes it for authenticated staff, so
    # exercise it the same way here.
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.create_user(
        username="pos_admin", email="pos_admin@example.com", password="x",
    )
    user.is_staff = True
    user.save()

    request = RequestFactory().get("/pos-upgrade/")
    request.user = user
    request.session = {}  # Django's admin_theme context processor reads request.session

    resp = pos_upgrade_required_view(request)
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "Unlock Point of Sale" in content
    assert "updates.spwig.com/upgrade/pos/" in content


def test_pos_upgrade_view_rejects_anonymous():
    """The routed URL redirects anonymous users to admin login — defence
    in depth. In production the middleware never invokes this for anon
    since POS paths are gated behind /admin/ already."""
    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory
    from pos_app.community_gate import pos_upgrade_required_view

    request = RequestFactory().get("/pos-upgrade/")
    request.user = AnonymousUser()
    request.session = {}

    resp = pos_upgrade_required_view(request)
    # @staff_member_required redirects unauthenticated to admin login
    assert resp.status_code == 302
    assert "login" in resp.url
