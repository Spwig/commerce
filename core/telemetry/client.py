"""
Anonymous deployment telemetry client.

Sends a small once-daily payload to the update server so we can track
adoption of ``Spwig/commerce`` across the OSS release. The payload is:

- platform_version   (already known to the server via registration, but re-sent
                      so telemetry rows are self-contained)
- installed_components — {slug: version} of components installed today
- metrics — a flexible bag including:
    - edition (community | pro | enterprise | dev | trial)
    - install_source (official-image | source-docker | source | unknown)
    - install_method (installer | "" for manual installs)
    - active_theme
    - payment_providers_configured — list of provider slugs
    - themes_installed — list of theme slugs
    - products_count_bucket — bucketed count, never raw
    - orders_count_bucket — bucketed count, never raw

Privacy notes:
- All counts are bucketed to reduce fingerprinting on tiny stores
- No merchant identity, no domain, no PII sent
- The install UUID (already sent at registration) is the only linkage
- Opt out entirely with the SPWIG_TELEMETRY env var

Sending is fire-and-forget: any network failure logs at DEBUG level and
returns. Telemetry must never block or slow a merchant's own request.
"""

import logging
from pathlib import Path

from django.conf import settings

import core

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Install provenance — how was this instance built and installed
# ---------------------------------------------------------------------------


def detect_install_source() -> str:
    """
    Classify how this installation was built and deployed.

    - "official-image": the compiled image from registry.spwig.com. It ships
      an integrity manifest at the project root, and its sensitive modules
      are compiled to native extensions.
    - "source-docker": built from the public source tree, running in Docker.
    - "source": built from the public source tree on bare metal.

    Never raises — returns "unknown" if detection itself fails.
    """
    try:
        if (Path(settings.BASE_DIR) / ".integrity_manifest.json").exists():
            return "official-image"

        # Belt-and-braces: protected builds compile core.license to a native
        # extension even if the manifest were ever missing.
        from core import license as _license_module

        if str(getattr(_license_module, "__file__", "")).endswith(".so"):
            return "official-image"

        if Path("/.dockerenv").exists():
            return "source-docker"
        return "source"
    except Exception as e:
        logger.debug("Install source detection failed: %s", e)
        return "unknown"


def get_install_method() -> str:
    """
    How the merchant installed Spwig ("installer" for the one-line installer,
    "" for manual installs that predate or skip the marker).
    """
    return str(getattr(settings, "SPWIG_INSTALL_METHOD", "") or "")


# ---------------------------------------------------------------------------
# Bucketing — never send raw counts
# ---------------------------------------------------------------------------

_COUNT_BUCKETS = [
    (0, 0, "0"),
    (1, 9, "1-9"),
    (10, 99, "10-99"),
    (100, 999, "100-999"),
    (1_000, 9_999, "1k-10k"),
    (10_000, 99_999, "10k-100k"),
    (100_000, 999_999, "100k-1M"),
    (1_000_000, float("inf"), "1M+"),
]


def bucket_count(n: int) -> str:
    """Map a raw count to a coarse bucket label. Never sends raw numbers."""
    if n is None:
        return "unknown"
    for lo, hi, label in _COUNT_BUCKETS:
        if lo <= n <= hi:
            return label
    return "unknown"


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------


def _installed_components() -> dict:
    """Return {slug: version} for currently installed components."""
    try:
        from component_updates.models import ComponentRegistry

        qs = ComponentRegistry.objects.values("slug", "current_version")
        return {row["slug"]: row["current_version"] for row in qs}
    except Exception as e:
        logger.debug("Could not enumerate installed components: %s", e)
        return {}


def _payment_providers_configured() -> list:
    """Return a list of payment provider slugs that have credentials configured."""
    try:
        from payment_providers.models import PaymentProviderAccount

        return sorted(
            set(
                PaymentProviderAccount.objects.filter(is_active=True).values_list(
                    "component__slug", flat=True
                )
            )
        )
    except Exception as e:
        logger.debug("Could not enumerate payment providers: %s", e)
        return []


def _themes_installed() -> list:
    """Return a list of installed theme slugs."""
    try:
        from design.models import Theme

        return list(Theme.objects.values_list("slug", flat=True))
    except Exception as e:
        logger.debug("Could not enumerate themes: %s", e)
        return []


def _active_theme() -> str:
    """Return the slug of the currently active theme, or '' if unknown."""
    try:
        from design.models import Theme

        active = Theme.objects.filter(is_active=True).first()
        return active.slug if active else ""
    except Exception as e:
        logger.debug("Could not read active theme: %s", e)
        return ""


def _products_count_bucket() -> str:
    try:
        from catalog.models import Product

        return bucket_count(Product.objects.count())
    except Exception:
        return "unknown"


def _orders_count_bucket() -> str:
    try:
        from orders.models import Order

        return bucket_count(Order.objects.count())
    except Exception:
        return "unknown"


def build_payload() -> dict:
    """Build the telemetry payload sent to /api/v1/telemetry/."""
    from core.license import get_license_manager

    return {
        "platform_version": core.__version__,
        "installed_components": _installed_components(),
        "metrics": {
            "edition": get_license_manager().get_edition(),
            "install_source": detect_install_source(),
            "install_method": get_install_method(),
            "active_theme": _active_theme(),
            "payment_providers_configured": _payment_providers_configured(),
            "themes_installed": _themes_installed(),
            "products_count_bucket": _products_count_bucket(),
            "orders_count_bucket": _orders_count_bucket(),
        },
    }


# ---------------------------------------------------------------------------
# Sender
# ---------------------------------------------------------------------------


def telemetry_enabled() -> bool:
    """Return whether the SPWIG_TELEMETRY_ENABLED setting is on."""
    return bool(getattr(settings, "SPWIG_TELEMETRY_ENABLED", True))


def send_telemetry() -> bool:
    """
    Build the payload and POST it to the update server.

    Returns True on success, False on any failure or when telemetry is
    disabled. Failures log at DEBUG level — never raises.
    """
    if not telemetry_enabled():
        logger.debug("Telemetry disabled via SPWIG_TELEMETRY_ENABLED; skipping")
        return False

    try:
        from component_updates.services import UpdateManager

        manager = UpdateManager()

        if not manager._ensure_authenticated():
            logger.debug("Telemetry skipped: not authenticated with update server")
            return False

        payload = build_payload()

        response = manager.session.post(
            f"{manager.config.server_url}/api/v1/telemetry/",
            json=payload,
            timeout=10,
        )
        if response.status_code >= 400:
            logger.debug(
                "Telemetry POST returned %s: %s",
                response.status_code,
                response.text[:200],
            )
            return False

        logger.debug("Telemetry sent successfully")
        return True
    except Exception as e:
        logger.debug("Telemetry send failed: %s", e)
        return False
