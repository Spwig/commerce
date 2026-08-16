"""Smoke tests for the Revenue Attribution admin dashboard view + data endpoint."""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from attribution.models import TouchPoint
from attribution.services.resolution import resolve_order
from tests.factories import OrderFactory

pytestmark = pytest.mark.django_db

User = get_user_model()


def _staff():
    # Superuser bypasses the analytics category gate.
    return User.objects.create_user(
        username="staff", email="staff@example.com", password="x", is_staff=True, is_superuser=True
    )


def _attributed_order():
    user = User.objects.create_user(username="buyer", email="b@example.com", password="x")
    order = OrderFactory(user=user, status="processing", total_amount=Decimal("100.00"))
    tp = TouchPoint.objects.create(
        visitor_key="vk1", customer=user, channel="email", medium="email"
    )
    TouchPoint.objects.filter(pk=tp.pk).update(occurred_at=timezone.now() - timedelta(minutes=30))
    resolve_order(order)


def test_dashboard_requires_staff(client):
    resp = client.get(reverse("attribution:dashboard"))
    assert resp.status_code == 302  # redirected to admin login


def test_dashboard_forbidden_for_staff_without_analytics(client):
    # Staff without the analytics category (and not superuser) must be refused.
    plain = User.objects.create_user(
        username="plain", email="plain@example.com", password="x", is_staff=True
    )
    client.force_login(plain)
    assert client.get(reverse("attribution:dashboard")).status_code == 403


def test_dashboard_renders_for_staff(client):
    _attributed_order()
    client.force_login(_staff())
    resp = client.get(reverse("attribution:dashboard"))
    assert resp.status_code == 200
    assert b'id="attr-payload"' in resp.content
    assert b"Revenue Attribution" in resp.content


def test_dashboard_empty_state_when_no_data(client):
    client.force_login(_staff())
    resp = client.get(reverse("attribution:dashboard"))
    assert resp.status_code == 200
    assert b"No attributed revenue yet" in resp.content


def test_data_endpoint_returns_contract(client):
    _attributed_order()
    client.force_login(_staff())
    resp = client.get(
        reverse("attribution:dashboard_data") + "?period=last_30_days",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    assert resp.status_code == 200
    data = resp.json()
    for key in (
        "period",
        "currency",
        "active_model",
        "models",
        "totals",
        "by_model",
        "journeys",
        "campaigns",
    ):
        assert key in data
    assert data["active_model"] in data["models"]
    # active model has the email channel we attributed
    active = {
        c["channel"]: c["revenue"] for c in data["by_model"][data["active_model"]]["channels"]
    }
    assert active.get("email") == 100.0


def test_data_endpoint_rejects_non_ajax(client):
    client.force_login(_staff())
    resp = client.get(reverse("attribution:dashboard_data"))
    assert resp.status_code == 400


def test_export_returns_csv(client):
    _attributed_order()
    client.force_login(_staff())
    resp = client.get(reverse("attribution:dashboard_export") + "?period=last_30_days")
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    assert "attachment" in resp["Content-Disposition"]
    body = resp.content.decode()
    assert "Channel,Revenue,Orders,Share %" in body
    assert "Email" in body


def test_export_forbidden_for_staff_without_analytics(client):
    plain = User.objects.create_user(
        username="plain2", email="plain2@example.com", password="x", is_staff=True
    )
    client.force_login(plain)
    assert client.get(reverse("attribution:dashboard_export")).status_code == 403
