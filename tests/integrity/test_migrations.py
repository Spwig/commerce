"""
Migration Safety Tests

Validates Django migrations can be safely applied and rolled back.
Includes static analysis (fast) and database integration tests (slow).
"""

import os
import re
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.db.migrations.loader import MigrationLoader

pytestmark = [pytest.mark.django_db, pytest.mark.integrity]


def _is_third_party_app(app_config) -> bool:
    """Return True if this app is a third-party dependency (not part of Spwig)."""
    app_path = Path(app_config.path).resolve()
    project_root = Path(settings.BASE_DIR).resolve()
    try:
        app_path.relative_to(project_root)
    except ValueError:
        return True  # Outside project root — third-party
    # Anything under site-packages counts as third-party even if project_root
    # is elsewhere.
    return "site-packages" in app_path.parts


class TestMigrationStaticAnalysis:
    """Fast checks that don't require DB access"""

    def test_migration_naming_convention(self):
        """All migrations follow NNNN_{descriptive_name}.py pattern.

        Only checks Spwig apps; third-party migration filenames are out of
        our control.
        """
        issues = []

        for app_config in apps.get_app_configs():
            if _is_third_party_app(app_config):
                continue
            migrations_dir = Path(app_config.path) / "migrations"
            if not migrations_dir.exists():
                continue

            for migration_file in migrations_dir.glob("0*.py"):
                if migration_file.name == "__init__.py":
                    continue

                # Pattern: 0001_initial.py, 0002_add_provider_metadata.py
                if not re.match(r"^\d{4}_[a-z0-9_]+\.py$", migration_file.name):
                    issues.append(f"{app_config.label}: {migration_file.name}")

        assert not issues, (
            "Invalid migration names:\n  "
            + "\n  ".join(issues)
            + "\n\nMigrations must follow pattern: NNNN_descriptive_name.py"
        )

    def test_no_conflicting_migration_numbers(self):
        """No duplicate migration numbers within the same app.

        Only checks Spwig apps; third-party apps (like django_celery_beat)
        occasionally ship duplicate migration numbers we cannot fix.
        """
        issues = []

        for app_config in apps.get_app_configs():
            if _is_third_party_app(app_config):
                continue
            migrations_dir = Path(app_config.path) / "migrations"
            if not migrations_dir.exists():
                continue

            numbers = {}
            for migration_file in migrations_dir.glob("0*.py"):
                if migration_file.name == "__init__.py":
                    continue

                number = migration_file.name[:4]
                if number in numbers:
                    issues.append(
                        f"{app_config.label}: {number} used by both "
                        f"{numbers[number]} and {migration_file.name}"
                    )
                numbers[number] = migration_file.name

        assert not issues, "Duplicate migration numbers:\n  " + "\n  ".join(issues)

    def test_migration_dependencies_exist(self):
        """All migration dependencies reference existing migrations.

        Django's autodetector inserts synthetic ``__first__`` / ``__latest__``
        pseudo-dependencies to describe "any migration from that app" — those
        never appear in disk_migrations. Skip them here, along with any
        third-party dependency reference.
        """
        loader = MigrationLoader(None, ignore_no_migrations=True)

        # Only Spwig apps (skip third-party) — third-party ``auth`` /
        # ``contenttypes`` etc. do exist but the pseudo names above never
        # match disk_migrations even for third-party apps.
        our_apps = {a.label for a in apps.get_app_configs() if not _is_third_party_app(a)}
        PSEUDO_NAMES = {"__first__", "__latest__"}

        issues = []
        for (app_label, migration_name), migration in loader.disk_migrations.items():
            if app_label not in our_apps:
                continue
            for dep_app, dep_name in migration.dependencies:
                if dep_name in PSEUDO_NAMES:
                    continue
                if dep_app not in our_apps:
                    # Third-party — assume Django/pip resolves it.
                    continue
                if (dep_app, dep_name) not in loader.disk_migrations:
                    issues.append(
                        f"{app_label}.{migration_name} depends on missing {dep_app}.{dep_name}"
                    )

        assert not issues, "Missing dependencies:\n  " + "\n  ".join(issues)

    def test_no_circular_dependencies(self):
        """Migration graph has no circular dependencies"""
        loader = MigrationLoader(None, ignore_no_migrations=True)

        # Django's loader raises on circular deps during construction
        # If we got here, graph is valid
        assert loader.graph is not None


@pytest.mark.slow
class TestMigrationDatabaseSafety:
    """Tests that require database setup/teardown"""

    def test_migrations_apply_cleanly_on_fresh_db(self, db):
        """All migrations can be applied to a fresh database"""
        out = StringIO()

        # This runs in the pytest temp DB
        call_command("migrate", "--verbosity=2", stdout=out)
        output = out.getvalue()

        # Check for errors in output
        assert "error" not in output.lower(), f"Migration errors detected:\n{output}"
        assert "failed" not in output.lower(), f"Migration failures detected:\n{output}"

    def test_no_missing_migrations(self, db):
        """makemigrations --check detects no unmade migrations.

        Must be run as a subprocess: ``core.apps`` monkey-patches every
        MoneyField currency default at import time and only skips that
        patch when ``"makemigrations" in sys.argv``. Calling
        ``call_command("makemigrations", ...)`` inside pytest bypasses
        that guard and produces false-positive "field alter" diffs.
        A subprocess with the real argv restores the guard.
        """
        project_root = Path(settings.BASE_DIR)
        result = subprocess.run(
            [sys.executable, "manage.py", "makemigrations", "--check", "--dry-run", "-v", "0"],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={**os.environ, "DJANGO_SETTINGS_MODULE": "core.settings"},
            timeout=120,
        )
        assert result.returncode == 0, (
            f"Unmade migrations detected (exit {result.returncode}).\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}\n\n"
            f"Run: python manage.py makemigrations"
        )
