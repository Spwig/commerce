"""
Root-level pytest fixtures — apply to every collected test regardless
of which app the test file lives in.

Keep this small. App-scoped fixtures belong in the corresponding
app/tests/conftest.py. Anything here becomes global.
"""

import os

import pytest

# NOTE: per-xdist-worker Redis DB isolation lives in core/settings.py
# (keyed on PYTEST_XDIST_WORKER). It cannot live here: pytest-django
# imports settings before root conftest, so an env override at this
# point arrives too late.


def _test_db_suffix() -> str:
    """
    Pick a suffix that keeps concurrent test runs off each other's database.

    Every run used the same `test_shop_db`, so two simultaneous runs — a person
    in a terminal and an AI agent, two agents, or two terminals — destroyed each
    other. `--create-db` drops a database the other is connected to, and the
    result is hundreds of `DuplicateDatabase` / `ObjectInUse` errors that look
    exactly like a mass regression. It has cost real debugging time and, once,
    someone's in-flight run.

    Resolution order:

    1. ``SPWIG_TEST_DB_SUFFIX`` — explicit wins. Use this for CI matrices, or
       to separate two sessions of the same kind.
    2. ``CLAUDE_CODE_SESSION_ID`` present → ``_agent``. Set inside Claude Code
       shells, so agent runs isolate themselves with nobody having to remember.
       Deliberately a *constant*, not the session id: `--reuse-db` then still
       works across an agent's runs, instead of rebuilding a 3-4 minute
       database every time.
    3. Otherwise no suffix — a human terminal keeps plain `test_shop_db` and
       behaves exactly as before.

    Two agent sessions at once would still share `_agent`; set
    ``SPWIG_TEST_DB_SUFFIX`` in one of them if that ever comes up.
    """
    explicit = os.environ.get("SPWIG_TEST_DB_SUFFIX", "").strip()
    if explicit:
        return explicit if explicit.startswith("_") else f"_{explicit}"
    if os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return "_agent"
    return ""


@pytest.fixture(scope="session")
def django_db_modify_db_settings(
    # Depend on pytest-django's own chain so xdist and tox suffixes still
    # apply; this adds to their behaviour rather than replacing it.
    django_db_modify_db_settings_parallel_suffix: None,
) -> None:
    """Append the isolation suffix to every configured test database name."""
    from django.conf import settings

    suffix = _test_db_suffix()
    if not suffix:
        return

    for db in settings.DATABASES.values():
        test_settings = db.setdefault("TEST", {})
        # TEST["NAME"] is usually unset, in which case Django derives
        # `test_<NAME>`. Derive the same base before suffixing so we extend the
        # real name rather than inventing one.
        base = test_settings.get("NAME") or f"test_{db.get('NAME', '')}"
        test_settings["NAME"] = f"{base}{suffix}"


def _test_wants_db(request) -> bool:
    """True when the test already uses the database, by any of the three routes."""
    if request.node.get_closest_marker("django_db") is not None:
        return True
    if {"db", "transactional_db", "live_server"} & set(request.fixturenames):
        return True
    # unittest-style tests: django.test.TestCase / TransactionTestCase manage
    # their own DB access without pytest fixtures or markers.
    instance = getattr(request, "instance", None)
    if instance is not None:
        from django.test import TransactionTestCase

        return isinstance(instance, TransactionTestCase)
    return False


@pytest.fixture(autouse=True)
def _seed_site_settings(request):
    """
    Guarantee the SiteSettings singleton exists for every DB-using test.

    Middleware (CurrencyMiddleware) and services (address_autocomplete's
    geocoder JWT) call SiteSettings.get_settings() on ordinary requests, and
    its get_or_create(pk=1) cannot succeed on an empty database — admin_email
    is required and save() runs full_clean(). Any test that touches those
    paths without creating the row itself only ever passed by inheriting a
    row leaked into a long-lived --reuse-db database; fresh per-context CI
    databases exposed that.

    Gated on _test_wants_db so pure unit tests don't silently become DB
    tests. Seeding happens per-test rather than at DB creation time because
    TransactionTestCase / live_server teardown flushes all tables — a
    create-time seed row would vanish mid-session and reintroduce
    order-dependent failures.

    Tests that depend on a SPECIFIC settings value must set it explicitly
    (assign and save, or queryset update). Do NOT rely on
    get_or_create(defaults={...}) — with this row already present, those
    defaults are silently ignored.
    """
    if not _test_wants_db(request):
        return
    # No-op inside unittest TestCase (pytest-django skips it there); for
    # marker/fixture-style tests it establishes the transactional wrapper
    # before we write, so the seed rolls back with the test.
    request.getfixturevalue("db")

    from core.models import SiteSettings

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )


@pytest.fixture(autouse=True)
def _bypass_license_acceptance_middleware(monkeypatch):
    """
    Short-circuit LicenseAcceptanceMiddleware so tests hitting storefront /
    admin paths don't get redirected to /license/accept/.

    The middleware gates real installs on first boot until the merchant
    clicks through. Tests never do — stub `is_accepted()` and
    `needs_reacceptance()` so every request passes through.

    Applies to ALL tests, including app-level suites (catalog/tests/,
    referrals/tests/, shipping/tests/ etc.) that don't inherit
    tests/conftest.py.
    """
    from core import license_acceptance as la

    class _StubService:
        def is_accepted(self):
            return True

        def needs_reacceptance(self):
            return (False, None)

    monkeypatch.setattr(la, "get_license_acceptance_service", lambda: _StubService())


@pytest.fixture(scope="session")
def test_gateway_on_disk() -> "object":
    """Materialise the on-disk ``test_gateway`` provider from the tracked
    ``preinstalled/`` bundle.

    ``components_data/`` is gitignored (it's regenerated from the bundled
    packages on real installs), so a fresh clone — CI's act runner, a new dev
    checkout — has NO provider code on disk. Any test that loads the REAL
    provider then fails: the tier2 gateway matrix, and the golden BROWSER flows
    whose checkout renders an empty ``#payment-providers-list`` (the
    ``continue-payment`` button never enables → 30s Playwright timeout).

    Locally this is a no-op (the tree is already unpacked). In CI it extracts
    ``preinstalled/integrations/test_gateway-<v>.zip`` into the marketplace's
    ``…/test_gateway/v{version}/`` + ``current`` symlink layout. Files only —
    the DB ``ComponentRegistry`` row is created by ``ComponentRegistryFactory``
    (tier2 proves the loader needs no ``ComponentVersion`` row), so this stays
    out of the per-test transaction entirely.

    Returns the ``current/`` directory the provider loads from.
    """
    import json
    import zipfile
    from pathlib import Path

    from django.conf import settings

    base = (
        Path(settings.BASE_DIR)
        / "components_data"
        / "integrations"
        / "payment_provider"
        / "test_gateway"
    )
    current = base / "current"
    if (current / "provider.py").exists():
        return current  # already unpacked (local dev)

    bundle_dir = Path(settings.BASE_DIR) / "preinstalled"
    manifest = json.loads((bundle_dir / "manifest.json").read_text())
    entry = next(
        c
        for c in manifest["components"]
        if c["type"] == "payment_provider" and c["slug"] == "test_gateway"
    )
    version = entry["version"]
    version_dir = base / f"v{version}"
    version_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(bundle_dir / entry["package"]) as zf:
        zf.extractall(version_dir)
    if current.exists() or current.is_symlink():
        current.unlink()
    current.symlink_to(f"v{version}")
    return current
