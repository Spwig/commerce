"""Admin API: /api/admin/analytics/attribution/ — auth, contract, filters."""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from attribution.models import TouchPoint
from attribution.services.resolution import resolve_order
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db

User = get_user_model()
URL = "/api/admin/analytics/attribution/"


def _superuser():
    return User.objects.create_user(
        username="admin", email="a@example.com", password="x", is_staff=True, is_superuser=True
    )


def _attributed_order():
    user = User.objects.create_user(username="buyer", email="b@example.com", password="x")
    order = OrderFactory(user=user, status="processing", total_amount=Decimal("100.00"))
    tp = TouchPoint.objects.create(
        visitor_key="vk1", customer=user, channel="email", medium="email"
    )
    TouchPoint.objects.filter(pk=tp.pk).update(occurred_at=timezone.now() - timedelta(minutes=30))
    resolve_order(order)


def test_requires_authentication(client):
    assert client.get(URL).status_code in (401, 403)


def test_forbidden_for_non_staff(client):
    user = User.objects.create_user(username="cust", email="c@example.com", password="x")
    client.force_login(user)
    assert client.get(URL).status_code == 403


def test_forbidden_for_staff_without_analytics(client):
    # The API honors the same analytics-category boundary as the web dashboard,
    # not just a bare is_staff check (session/mobile auth).
    staff = User.objects.create_user(
        username="editor", email="e@example.com", password="x", is_staff=True
    )
    client.force_login(staff)
    assert client.get(URL).status_code == 403


def test_invalid_model_is_400(client):
    client.force_login(_superuser())
    resp = client.get(URL + "?period=last_30_days&model=bogus")
    assert resp.status_code == 400


def test_returns_contract(client):
    _attributed_order()
    client.force_login(_superuser())
    resp = client.get(URL + "?period=last_30_days")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    data = body["data"]
    for key in ("period", "currency", "active_model", "models", "totals", "by_model", "journeys"):
        assert key in data
    # all models present by default
    assert set(data["by_model"].keys()) == set(data["models"])
    active = {
        c["channel"]: c["revenue"] for c in data["by_model"][data["active_model"]]["channels"]
    }
    assert active.get("email") == 100.0


def test_model_filter_returns_single_block(client):
    _attributed_order()
    client.force_login(_superuser())
    resp = client.get(URL + "?period=last_30_days&model=linear")
    assert resp.status_code == 200
    assert list(resp.json()["data"]["by_model"].keys()) == ["linear"]


def test_invalid_period_is_400(client):
    client.force_login(_superuser())
    resp = client.get(URL + "?period=nonsense")
    assert resp.status_code == 400
    assert resp.json()["success"] is False


def test_custom_period_requires_dates(client):
    client.force_login(_superuser())
    resp = client.get(URL + "?period=custom")
    assert resp.status_code == 400
