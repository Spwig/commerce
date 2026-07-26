"""
Client-side telemetry tests.
"""

import contextlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@contextlib.contextmanager
def fake_path_exists(existing):
    """
    Patch pathlib.Path.exists so that ONLY the paths in ``existing`` report
    True. Lets us drive each branch of detect_install_source() deterministically
    without depending on the real filesystem (e.g. a stray /.dockerenv).
    """
    wanted = {str(p) for p in existing}

    def _exists(self):
        return str(self) in wanted

    with patch.object(Path, "exists", _exists):
        yield


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


# ---------------------------------------------------------------------------
# Install-source detection
# ---------------------------------------------------------------------------


def test_detect_install_source_official_image_via_manifest_real_file(settings, tmp_path):
    """An integrity manifest at the project root marks an official image."""
    from core.telemetry.client import detect_install_source

    settings.BASE_DIR = str(tmp_path)
    (tmp_path / ".integrity_manifest.json").write_text("{}")

    assert detect_install_source() == "official-image"


def test_detect_install_source_official_image_via_manifest(settings):
    """The manifest check short-circuits before any other signal is examined."""
    from core.telemetry.client import detect_install_source

    settings.BASE_DIR = "/srv/app"
    with fake_path_exists({"/srv/app/.integrity_manifest.json"}):
        assert detect_install_source() == "official-image"


def test_detect_install_source_official_image_via_compiled_license(settings, monkeypatch):
    """
    Belt-and-braces: with no manifest, a core.license compiled to a native
    extension (.so) still classifies the install as an official image.
    """
    import core.license as license_module
    from core.telemetry.client import detect_install_source

    settings.BASE_DIR = "/srv/app"
    monkeypatch.setattr(license_module, "__file__", "/srv/app/core/license.so")

    # No manifest, not in Docker — the .so signal must carry the decision.
    with fake_path_exists(set()):
        assert detect_install_source() == "official-image"


def test_detect_install_source_source_docker(settings):
    """Public source tree running inside Docker → source-docker."""
    from core.telemetry.client import detect_install_source

    settings.BASE_DIR = "/srv/app"
    # No manifest; real core.license is a .py module; /.dockerenv present.
    with fake_path_exists({"/.dockerenv"}):
        assert detect_install_source() == "source-docker"


def test_detect_install_source_bare_metal(settings):
    """Public source tree on bare metal (no manifest, no Docker) → source."""
    from core.telemetry.client import detect_install_source

    settings.BASE_DIR = "/srv/app"
    with fake_path_exists(set()):
        assert detect_install_source() == "source"


def test_detect_install_source_unknown_on_failure(settings):
    """Detection never raises — an internal error yields 'unknown'."""
    from core.telemetry.client import detect_install_source

    # Path(None) raises TypeError inside the try block.
    settings.BASE_DIR = None
    assert detect_install_source() == "unknown"


# ---------------------------------------------------------------------------
# Install method
# ---------------------------------------------------------------------------


def test_get_install_method_reads_setting(settings):
    from core.telemetry.client import get_install_method

    settings.SPWIG_INSTALL_METHOD = "installer"
    assert get_install_method() == "installer"


def test_get_install_method_defaults_blank(settings):
    from core.telemetry.client import get_install_method

    settings.SPWIG_INSTALL_METHOD = ""
    assert get_install_method() == ""


def test_get_install_method_none_becomes_blank(settings):
    """A None setting must not leak into the payload as the string 'None'."""
    from core.telemetry.client import get_install_method

    settings.SPWIG_INSTALL_METHOD = None
    assert get_install_method() == ""


# ---------------------------------------------------------------------------
# Payload — install provenance is carried through
# ---------------------------------------------------------------------------


def test_build_payload_includes_install_provenance(settings):
    """metrics carries install_source and install_method from the new helpers."""
    from core.telemetry.client import build_payload

    settings.SPWIG_INSTALL_METHOD = "installer"

    with (
        patch("core.license.get_license_manager") as get_lm,
        patch("core.telemetry.client.detect_install_source", return_value="source-docker"),
    ):
        get_lm.return_value.get_edition.return_value = "community"
        payload = build_payload()

    metrics = payload["metrics"]
    assert metrics["install_source"] == "source-docker"
    assert metrics["install_method"] == "installer"


# ---------------------------------------------------------------------------
# Regression: the payload enumerates REAL DB rows.
#
# _installed_components() and _payment_providers_configured() previously
# imported nonexistent models and always returned empty. These tests create
# real rows and assert they surface in the payload, so a re-broken import
# (which the try/except would silently swallow) turns the build red.
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_build_payload_lists_installed_components():
    from core.telemetry.client import build_payload
    from tests.factories import ComponentRegistryFactory

    ComponentRegistryFactory(
        component_type="widget",
        slug="hero-banner",
        name="Hero Banner",
        current_version="2.1.0",
    )

    with patch("core.license.get_license_manager") as get_lm:
        get_lm.return_value.get_edition.return_value = "community"
        payload = build_payload()

    assert payload["installed_components"].get("hero-banner") == "2.1.0"


@pytest.mark.django_db
def test_build_payload_lists_active_payment_providers():
    from core.telemetry.client import build_payload
    from tests.factories import ComponentRegistryFactory, PaymentProviderAccountFactory

    active = PaymentProviderAccountFactory(is_active=True)  # component slug "stripe"

    inactive_component = ComponentRegistryFactory(
        component_type="payment_provider",
        slug="paypal_checkout",
        name="PayPal Checkout",
    )
    PaymentProviderAccountFactory(
        is_active=False,
        is_default=False,
        component=inactive_component,
    )

    with patch("core.license.get_license_manager") as get_lm:
        get_lm.return_value.get_edition.return_value = "community"
        payload = build_payload()

    configured = payload["metrics"]["payment_providers_configured"]
    assert active.component.slug in configured  # active provider surfaces
    assert "paypal_checkout" not in configured  # inactive account is filtered out
