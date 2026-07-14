"""
Client-side telemetry tests.
"""

from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Bucket function
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, "0"),
        (1, "1-9"),
        (9, "1-9"),
        (10, "10-99"),
        (99, "10-99"),
        (100, "100-999"),
        (999, "100-999"),
        (1_000, "1k-10k"),
        (9_999, "1k-10k"),
        (10_000, "10k-100k"),
        (100_000, "100k-1M"),
        (1_000_000, "1M+"),
        (None, "unknown"),
    ],
)
def test_bucket_count(n, expected):
    from core.telemetry.client import bucket_count

    assert bucket_count(n) == expected


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------


def test_build_payload_shape_and_edition():
    """Payload structure matches what the server expects."""
    from core.telemetry.client import build_payload

    with patch("core.license.get_license_manager") as get_lm:
        get_lm.return_value.get_edition.return_value = "community"
        payload = build_payload()

    assert set(payload.keys()) == {"platform_version", "installed_components", "metrics"}
    assert isinstance(payload["platform_version"], str)
    assert isinstance(payload["installed_components"], dict)
    metrics = payload["metrics"]
    assert metrics["edition"] == "community"
    assert "active_theme" in metrics
    assert "payment_providers_configured" in metrics
    assert "themes_installed" in metrics
    # Counts must be bucketed, never raw ints
    assert isinstance(metrics["products_count_bucket"], str)
    assert isinstance(metrics["orders_count_bucket"], str)


# ---------------------------------------------------------------------------
# Sender
# ---------------------------------------------------------------------------


def test_send_telemetry_respects_opt_out(settings):
    """SPWIG_TELEMETRY_ENABLED=False → send_telemetry() returns False without doing anything."""
    from core.telemetry.client import send_telemetry

    settings.SPWIG_TELEMETRY_ENABLED = False

    with patch("component_updates.services.UpdateManager") as UM:
        result = send_telemetry()

    assert result is False
    UM.assert_not_called()


def test_send_telemetry_skips_when_auth_fails(settings):
    """If UpdateManager can't authenticate, telemetry silently returns False."""
    from core.telemetry.client import send_telemetry

    settings.SPWIG_TELEMETRY_ENABLED = True

    with patch("component_updates.services.UpdateManager") as UM:
        manager = UM.return_value
        manager._ensure_authenticated.return_value = False
        result = send_telemetry()

    assert result is False
    manager.session.post.assert_not_called()


def test_send_telemetry_posts_when_authenticated(settings):
    """Happy path: build payload, POST to update server."""
    from core.telemetry.client import send_telemetry

    settings.SPWIG_TELEMETRY_ENABLED = True

    with (
        patch("component_updates.services.UpdateManager") as UM,
        patch("core.license.get_license_manager") as get_lm,
    ):
        manager = UM.return_value
        manager._ensure_authenticated.return_value = True
        manager.config.server_url = "https://updates.example.com"

        response = MagicMock()
        response.status_code = 200
        manager.session.post.return_value = response

        get_lm.return_value.get_edition.return_value = "community"

        result = send_telemetry()

    assert result is True
    manager.session.post.assert_called_once()
    call_kwargs = manager.session.post.call_args
    assert call_kwargs.args[0].endswith("/api/v1/telemetry/")
    payload = call_kwargs.kwargs["json"]
    assert "platform_version" in payload
    assert payload["metrics"]["edition"] == "community"


def test_send_telemetry_swallows_network_errors(settings):
    """Connection errors are logged, not raised — telemetry must never break the caller."""
    from core.telemetry.client import send_telemetry

    settings.SPWIG_TELEMETRY_ENABLED = True

    with patch("component_updates.services.UpdateManager") as UM:
        manager = UM.return_value
        manager._ensure_authenticated.return_value = True
        manager.config.server_url = "https://updates.example.com"
        manager.session.post.side_effect = Exception("connection refused")

        result = send_telemetry()

    assert result is False  # graceful failure, no exception
