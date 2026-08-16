"""
Tests for scoped merchant API tokens (core.APIToken) on the admin API.

Covers:
- Scope-map completeness vs. the live admin_api URLconf (fail-closed contract).
- APITokenAuthentication binding, scope enforcement, expiry/IP, superuser cap,
  namespace isolation, and fall-through for unbindable/mobile/garbage tokens.
- The new combined /api/admin/analytics/traffic/ endpoint.
- APIToken.has_scope() and the registry's HQ filtering.
"""

import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.urls import get_resolver, resolve
from django.utils import timezone
from rest_framework.test import APIClient, APIRequestFactory

from admin_api.scope_map import SCOPE_MAP, TOKEN_FORBIDDEN
from core.api_scopes import get_available_scopes
from core.authentication import APITokenAuthentication
from core.models import APIToken
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db]

TRAFFIC_URL = "/api/admin/analytics/traffic/"


def _token(creator, scopes=None, **kwargs):
    return APIToken.objects.create(
        name=kwargs.pop("name", "test token"),
        token=kwargs.pop("token", f"tok_{uuid.uuid4().hex}"),
        token_type="custom",
        created_by=creator,
        scopes=scopes or {},
        is_active=True,
        **kwargs,
    )


def _client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.token}")
    return client


def _grant_category(user, **categories):
    """Give ``user`` a StaffRole granting the named permission categories.

    The order-status mutation endpoints are gated on
    ``category_permission("orders", "full")`` (added by the A1 mutation-gating
    security hardening) in addition to the token scope. A bare ``is_staff`` user
    holds no category grant, so without this the category gate — not the scope
    gate — is what returns 403. Granting the category isolates the scope-gate
    behaviour these tests mean to prove.
    """
    from django.contrib.auth.models import Group

    from staff_roles.models import StaffRole
    from staff_roles.services import invalidate_user_cache

    group = Group.objects.create(name=f"role-{uuid.uuid4().hex[:8]}")
    user.groups.add(group)
    StaffRole.objects.create(
        group=group,
        display_name=group.name,
        can_access_admin=True,
        permission_categories=categories,
    )
    invalidate_user_cache(user)
    return user


# --------------------------------------------------------------------------- #
# Scope map completeness (the fail-closed contract)
# --------------------------------------------------------------------------- #


def test_scope_map_covers_every_admin_api_url():
    resolver = get_resolver()
    _, patterns = resolver.namespace_dict["admin_api"]
    names = {p.name for p in patterns.url_patterns if getattr(p, "name", None)}

    mapped = set(SCOPE_MAP) | set(TOKEN_FORBIDDEN)
    assert names - mapped == set(), "unmapped admin_api endpoints (fail-closed gap)"
    assert mapped - names == set(), "stale entries not present in the URLconf"


def test_scope_map_only_references_known_scopes():
    available = set(get_available_scopes())
    unknown = {v for v in SCOPE_MAP.values() if v not in available}
    assert unknown == set()


def test_scope_map_and_forbidden_are_disjoint():
    assert set(SCOPE_MAP) & set(TOKEN_FORBIDDEN) == set()


# --------------------------------------------------------------------------- #
# has_scope
# --------------------------------------------------------------------------- #


def test_has_scope_levels():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"analytics.traffic": "read", "orders": "write"})
    assert token.has_scope("analytics.traffic", "read")
    assert not token.has_scope("analytics.traffic", "write")
    assert token.has_scope("orders", "read")  # write implies read
    assert token.has_scope("orders", "write")
    assert not token.has_scope("products", "read")  # not granted


# --------------------------------------------------------------------------- #
# Traffic endpoint via API client
# --------------------------------------------------------------------------- #


def test_traffic_with_scope_returns_200():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"analytics.traffic": "read"})
    resp = _client(token).get(TRAFFIC_URL, {"period": "30_days"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    for key in (
        "overview",
        "traffic_trends",
        "top_pages",
        "geographic_distribution",
        "referrer_stats",
    ):
        assert key in body["data"]


def test_traffic_without_scope_returns_403():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"orders": "read"})  # wrong scope
    resp = _client(token).get(TRAFFIC_URL)
    assert resp.status_code == 403


def test_traffic_bad_period_returns_400():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"analytics.traffic": "read"})
    resp = _client(token).get(TRAFFIC_URL, {"period": "nonsense"})
    assert resp.status_code == 400


def test_session_staff_reaches_traffic_without_token():
    staff = UserFactory(is_staff=True, password="pw12345")
    client = APIClient()
    client.force_authenticate(user=staff)
    resp = client.get(TRAFFIC_URL, {"period": "7_days"})
    assert resp.status_code == 200


# --------------------------------------------------------------------------- #
# Cross-endpoint permission matrix — read vs write derived from HTTP method
# --------------------------------------------------------------------------- #

ORDERS_LIST = "/api/admin/orders/"
ORDER_STATUS = "/api/admin/orders/NOPE-404/status/"  # non-existent order


def test_read_scope_allows_get_but_not_write_on_same_resource():
    # Grant the orders category so the category gate is satisfied and the token
    # SCOPE is the only thing under test here.
    staff = _grant_category(UserFactory(is_staff=True), orders="full")
    token = _token(staff, scopes={"orders": "read"})
    client = _client(token)
    # GET is a read → allowed by the read scope.
    assert client.get(ORDERS_LIST).status_code == 200
    # POST is a write → the read scope must NOT satisfy it.
    assert client.post(ORDER_STATUS, {"status": "processing"}, format="json").status_code == 403


def test_write_scope_passes_scope_gate_on_write_method():
    # Category granted so only the token scope decides; the write scope clears the
    # scope gate and the request then fails downstream for a missing order
    # (404/400), NOT with a scope 403 — proving the gate opened.
    staff = _grant_category(UserFactory(is_staff=True), orders="full")
    token = _token(staff, scopes={"orders": "write"})
    resp = _client(token).post(ORDER_STATUS, {"status": "processing"}, format="json")
    assert resp.status_code != 403


def test_scope_does_not_leak_across_resources():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"orders": "read"})
    # An orders token cannot read products.
    assert _client(token).get("/api/admin/products/").status_code == 403


def test_write_scope_implies_read():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"orders": "write"})
    # A write grant also satisfies GET.
    assert _client(token).get(ORDERS_LIST).status_code == 200


# --------------------------------------------------------------------------- #
# Token rejection / fall-through paths
# --------------------------------------------------------------------------- #


def test_forbidden_endpoint_denies_token():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"staff": "write"})
    # staff_profile is in TOKEN_FORBIDDEN → always denied for tokens.
    resp = _client(token).get("/api/admin/auth/profile/")
    assert resp.status_code == 403


def test_expired_token_is_rejected():
    staff = UserFactory(is_staff=True)
    token = _token(
        staff,
        scopes={"analytics.traffic": "read"},
        expires_at=timezone.now() - timedelta(hours=1),
    )
    resp = _client(token).get(TRAFFIC_URL)
    assert resp.status_code == 401


def test_token_with_no_creator_falls_through():
    # created_by=None (legacy help/sync token) is unbindable → no auth succeeds.
    token = _token(None, scopes={"analytics.traffic": "read"})
    resp = _client(token).get(TRAFFIC_URL)
    assert resp.status_code == 401


def test_token_with_nonstaff_creator_falls_through():
    non_staff = UserFactory(is_staff=False)
    token = _token(non_staff, scopes={"analytics.traffic": "read"})
    resp = _client(token).get(TRAFFIC_URL)
    assert resp.status_code == 401


def test_ip_restriction_enforced():
    staff = UserFactory(is_staff=True)
    token = _token(
        staff,
        scopes={"analytics.traffic": "read"},
        allowed_ips=["10.0.0.1"],
    )
    resp = _client(token).get(TRAFFIC_URL, REMOTE_ADDR="127.0.0.1")
    assert resp.status_code == 401


# --------------------------------------------------------------------------- #
# Authentication-class unit tests (superuser cap, namespace isolation)
# --------------------------------------------------------------------------- #


def _auth_request(path, token):
    factory = APIRequestFactory()
    req = factory.get(path, HTTP_AUTHORIZATION=f"Bearer {token.token}")
    req.resolver_match = resolve(path)
    return req


def test_superuser_created_token_is_capped_to_non_superuser():
    superuser = UserFactory(is_staff=True, is_superuser=True)
    token = _token(superuser, scopes={"analytics.traffic": "read"})
    req = _auth_request(TRAFFIC_URL, token)
    user, auth = APITokenAuthentication().authenticate(req)
    assert auth == token
    assert user.is_superuser is False  # cap applied on the in-memory instance
    # And it is NOT persisted.
    superuser.refresh_from_db()
    assert superuser.is_superuser is True


def test_authentication_inert_outside_admin_api_namespace():
    staff = UserFactory(is_staff=True)
    token = _token(staff, scopes={"analytics.traffic": "read"})
    factory = APIRequestFactory()
    req = factory.get("/somewhere/", HTTP_AUTHORIZATION=f"Bearer {token.token}")

    class _RM:
        namespace = "storefront"
        url_name = "home"

    req.resolver_match = _RM()
    assert APITokenAuthentication().authenticate(req) is None


def test_unknown_bearer_defers_to_next_authenticator():
    staff = UserFactory(is_staff=True)
    _token(staff, scopes={"analytics.traffic": "read"})
    factory = APIRequestFactory()
    req = factory.get(TRAFFIC_URL, HTTP_AUTHORIZATION="Bearer not-a-real-token")
    req.resolver_match = resolve(TRAFFIC_URL)
    # Not one of ours → return None so MobileTokenAuthentication can try.
    assert APITokenAuthentication().authenticate(req) is None


# --------------------------------------------------------------------------- #
# Registry HQ filtering
# --------------------------------------------------------------------------- #


def test_registry_excludes_hq_only_when_not_hq():
    fake = {
        "analytics.traffic": {
            "label": "Web Analytics",
            "group": "analytics",
            "description": "",
            "supports_write": False,
            "hq_only": False,
        },
        "hq_secret": {
            "label": "HQ Secret",
            "group": "analytics",
            "description": "",
            "supports_write": False,
            "hq_only": True,
        },
    }
    with patch("core.api_scopes.SCOPE_REGISTRY", fake):
        with patch("core.api_scopes.settings") as mock_settings:
            mock_settings.SPWIG_IS_HQ = False
            available = get_available_scopes()
            assert "hq_secret" not in available
            assert "analytics.traffic" in available
            mock_settings.SPWIG_IS_HQ = True
            assert "hq_secret" in get_available_scopes()
