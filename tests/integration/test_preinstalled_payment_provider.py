"""
Regression coverage for today's preinstalled payment-provider pipeline.

Three fixes are pinned here:

1. ``build_preinstalled_packages`` now packages ``integrations/payments``
   providers into ZIPs, and a *partial* build (``--type payment_provider``)
   MERGES the master manifest instead of clobbering the entries of types that
   weren't rebuilt.

2. ``installers.install_provider_from_package`` lays a provider down in the
   marketplace's symlink-versioned shape
   (``.../payment_provider/<slug>/v<version>`` + ``current`` symlink) and
   registers it in ``ComponentRegistry``.

3. ``install_bundled_components._ensure_test_gateway_account`` bootstraps a
   ``PaymentProviderAccount`` for the Test Gateway — active iff sandbox mode,
   with ``{"_global": ["card"]}`` methods and encrypted ``{"test_mode": True}``
   credentials — and never duplicates an existing account.

``INTEGRATIONS_DIR`` / ``CACHE_MARKERS_DIR`` are module-level constants derived
from ``settings.BASE_DIR`` (not settings-overridable), and
``install_provider_from_package`` imports them lazily from
``component_updates.integration_paths`` at call time — so we monkeypatch the
module attributes to keep every filesystem write inside ``tmp_path``.
"""

import json
import os
import zipfile
from pathlib import Path

import pytest
from django.core.management import call_command

from tests.factories import ComponentRegistryFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _write_source_tree(components_dir: Path):
    """A minimal spwig-components source tree for the test_gateway provider."""
    provider = components_dir / "integrations" / "payments" / "test_gateway"
    provider.mkdir(parents=True)
    (provider / "manifest.json").write_text(
        json.dumps(
            {
                "slug": "test_gateway",
                "name": "Test Gateway",
                "version": "1.0.0",
                "author": "Spwig",
                "description": "Simulated test payment gateway",
                "entry_point": "provider",
            }
        )
    )
    (provider / "provider.py").write_text("class TestGatewayProvider:\n    pass\n")
    # An excluded directory to prove PROVIDER_PACKAGE_EXCLUDES is honoured.
    tests_dir = provider / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_thing.py").write_text("# must be excluded from the package\n")


# ============================================================
# 1. build_preinstalled_packages — packaging + manifest merge
# ============================================================


class TestBuildPreinstalledProviderPackages:
    def test_build_packages_provider_and_merges_manifest(self, tmp_path):
        components_dir = tmp_path / "components"
        output_dir = tmp_path / "preinstalled"
        _write_source_tree(components_dir)

        # Pre-seed the master manifest with an unrelated theme entry. A partial
        # --type payment_provider build must PRESERVE it (the merge fix).
        output_dir.mkdir(parents=True)
        (output_dir / "manifest.json").write_text(
            json.dumps(
                {
                    "platform_version": "1.0.0",
                    "components": [
                        {
                            "type": "theme",
                            "slug": "starter",
                            "version": "1.0.0",
                            "package": "themes/starter-1.0.0.zip",
                            "checksum": "deadbeef",
                        }
                    ],
                }
            )
        )

        call_command(
            "build_preinstalled_packages",
            "--type",
            "payment_provider",
            "--components-dir",
            str(components_dir),
            "--output-dir",
            str(output_dir),
        )

        # ZIP built at integrations/<slug>-<version>.zip with the right contents.
        zip_path = output_dir / "integrations" / "test_gateway-1.0.0.zip"
        assert zip_path.exists()
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
        assert "manifest.json" in names
        assert "provider.py" in names
        assert not any(n.startswith("tests/") for n in names)  # excluded dir

        # Master manifest carries the new payment_provider entry AND still the
        # pre-existing theme entry (merge, not clobber).
        manifest = json.loads((output_dir / "manifest.json").read_text())
        by_type = {}
        for c in manifest["components"]:
            by_type.setdefault(c["type"], []).append(c)
        assert "theme" in by_type, "partial build clobbered the theme entry"
        assert "payment_provider" in by_type
        pp = by_type["payment_provider"][0]
        assert pp["slug"] == "test_gateway"
        assert pp["version"] == "1.0.0"
        assert pp["package"] == "integrations/test_gateway-1.0.0.zip"


# ============================================================
# 2. install_provider_from_package — versioned layout + registry
# ============================================================


class TestInstallProviderFromPackage:
    def test_creates_version_dir_symlink_and_registry(self, tmp_path, monkeypatch):
        from component_updates import integration_paths
        from component_updates.installers import install_provider_from_package
        from component_updates.models import ComponentRegistry

        integrations_dir = tmp_path / "components_data" / "integrations"
        markers_dir = tmp_path / "components_data" / ".cache_markers"
        monkeypatch.setattr(integration_paths, "INTEGRATIONS_DIR", integrations_dir)
        monkeypatch.setattr(integration_paths, "CACHE_MARKERS_DIR", markers_dir)

        # The "extracted package": a directory holding manifest.json + code.
        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()
        (extract_dir / "manifest.json").write_text(
            json.dumps({"slug": "test_gateway", "name": "Test Gateway", "version": "1.0.0"})
        )
        (extract_dir / "provider.py").write_text("X = 1\n")
        manifest = {"slug": "test_gateway", "name": "Test Gateway", "version": "1.0.0"}

        result = install_provider_from_package(
            extract_dir, manifest, component_type="payment_provider"
        )
        assert result["success"] is True, result

        base = integrations_dir / "payment_provider" / "test_gateway"
        version_dir = base / "v1.0.0"
        assert (version_dir / "manifest.json").exists()
        assert (version_dir / "provider.py").exists()

        current = base / "current"
        assert current.is_symlink()
        assert os.readlink(current) == "v1.0.0"

        reg = ComponentRegistry.objects.get(component_type="payment_provider", slug="test_gateway")
        assert reg.current_version == "1.0.0"


# ============================================================
# 3. _ensure_test_gateway_account — account bootstrap
# ============================================================


def _make_command():
    from component_updates.management.commands.install_bundled_components import Command

    return Command()


# Regression context: the first version of ``_ensure_test_gateway_account``
# omitted the required ``user`` FK and the create raised IntegrityError, which
# ``handle()`` swallowed — files + registry installed, account silently never
# created. The account is now owned by the first active superuser, and the
# bootstrap defers (without raising) when no admin exists yet.


class TestEnsureTestGatewayAccount:
    def _seed_registry(self):
        return ComponentRegistryFactory(
            slug="test_gateway",
            component_type="payment_provider",
            name="Test Gateway",
        )

    def _seed_owner(self):
        from django.contrib.auth import get_user_model

        return get_user_model().objects.create_superuser(
            username="storeowner",
            email="owner@example.com",
            password="testpass123",
        )

    def test_account_created_active_in_sandbox_mode(self, monkeypatch):
        """In sandbox mode the account is created ACTIVE, owned by the store
        owner, with the documented global card methods and encrypted
        test-mode credentials."""
        import core.license
        from payment_providers.models import PaymentProviderAccount

        self._seed_registry()
        owner = self._seed_owner()
        monkeypatch.setattr(core.license, "is_sandbox_mode", lambda: True)

        _make_command()._ensure_test_gateway_account()

        acct = PaymentProviderAccount.objects.get(component__slug="test_gateway")
        assert acct.user_id == owner.id
        assert acct.is_active is True
        assert acct.connection_status == "connected"
        assert acct.available_payment_methods == {"_global": ["card"]}
        assert acct.enabled_payment_methods == {"_global": ["card"]}
        # Credentials are stored encrypted; test_mode is a non-secret flag kept
        # in the clear by encrypt_credentials.
        assert acct.credentials_encrypted.get("test_mode") is True
        assert acct.test_mode is True

    def test_account_created_disabled_outside_sandbox(self, monkeypatch):
        """A production licence (not sandbox) still pre-creates the account but
        DISABLED, so enabling the simulated gateway is a deliberate action."""
        import core.license
        from payment_providers.models import PaymentProviderAccount

        self._seed_registry()
        self._seed_owner()
        monkeypatch.setattr(core.license, "is_sandbox_mode", lambda: False)

        _make_command()._ensure_test_gateway_account()

        acct = PaymentProviderAccount.objects.get(component__slug="test_gateway")
        assert acct.is_active is False

    def test_bootstrap_is_idempotent(self, monkeypatch):
        """Running twice must not create a second account for the same
        component."""
        import core.license
        from payment_providers.models import PaymentProviderAccount

        self._seed_registry()
        self._seed_owner()
        monkeypatch.setattr(core.license, "is_sandbox_mode", lambda: True)

        cmd = _make_command()
        cmd._ensure_test_gateway_account()
        cmd._ensure_test_gateway_account()

        assert PaymentProviderAccount.objects.filter(component__slug="test_gateway").count() == 1

    def test_bootstrap_defers_without_admin_user(self, monkeypatch):
        """First boot may run before the merchant admin exists: the bootstrap
        must skip quietly (it reruns on every boot) rather than raise."""
        import core.license
        from payment_providers.models import PaymentProviderAccount

        self._seed_registry()
        monkeypatch.setattr(core.license, "is_sandbox_mode", lambda: True)

        _make_command()._ensure_test_gateway_account()

        assert not PaymentProviderAccount.objects.filter(component__slug="test_gateway").exists()
