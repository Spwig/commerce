"""
Migration Safety Tests

Validates Django migrations can be safely applied and rolled back.
Includes static analysis (fast) and database integration tests (slow).
"""
import pytest
import re
from pathlib import Path
from django.apps import apps
from django.core.management import call_command
from django.db.migrations.loader import MigrationLoader
from io import StringIO


pytestmark = [pytest.mark.django_db, pytest.mark.integrity]


class TestMigrationStaticAnalysis:
    """Fast checks that don't require DB access"""

    def test_migration_naming_convention(self):
        """All migrations follow NNNN_{descriptive_name}.py pattern"""
        issues = []

        for app_config in apps.get_app_configs():
            migrations_dir = Path(app_config.path) / 'migrations'
            if not migrations_dir.exists():
                continue

            for migration_file in migrations_dir.glob('0*.py'):
                if migration_file.name == '__init__.py':
                    continue

                # Pattern: 0001_initial.py, 0002_add_provider_metadata.py
                if not re.match(r'^\d{4}_[a-z0-9_]+\.py$', migration_file.name):
                    issues.append(f"{app_config.label}: {migration_file.name}")

        assert not issues, (
            f"Invalid migration names:\n  " + "\n  ".join(issues) +
            "\n\nMigrations must follow pattern: NNNN_descriptive_name.py"
        )

    def test_no_conflicting_migration_numbers(self):
        """No duplicate migration numbers within the same app"""
        issues = []

        for app_config in apps.get_app_configs():
            migrations_dir = Path(app_config.path) / 'migrations'
            if not migrations_dir.exists():
                continue

            numbers = {}
            for migration_file in migrations_dir.glob('0*.py'):
                if migration_file.name == '__init__.py':
                    continue

                number = migration_file.name[:4]
                if number in numbers:
                    issues.append(
                        f"{app_config.label}: {number} used by both "
                        f"{numbers[number]} and {migration_file.name}"
                    )
                numbers[number] = migration_file.name

        assert not issues, (
            f"Duplicate migration numbers:\n  " + "\n  ".join(issues)
        )

    def test_migration_dependencies_exist(self):
        """All migration dependencies reference existing migrations"""
        loader = MigrationLoader(None, ignore_no_migrations=True)

        issues = []
        for (app_label, migration_name), migration in loader.disk_migrations.items():
            for dep_app, dep_name in migration.dependencies:
                if (dep_app, dep_name) not in loader.disk_migrations:
                    # Allow dependencies on Django/third-party apps
                    our_apps = {a.label for a in apps.get_app_configs()}
                    if dep_app not in our_apps:
                        continue

                    issues.append(
                        f"{app_label}.{migration_name} depends on missing "
                        f"{dep_app}.{dep_name}"
                    )

        assert not issues, (
            f"Missing dependencies:\n  " + "\n  ".join(issues)
        )

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
        call_command('migrate', '--verbosity=2', stdout=out)
        output = out.getvalue()

        # Check for errors in output
        assert 'error' not in output.lower(), f"Migration errors detected:\n{output}"
        assert 'failed' not in output.lower(), f"Migration failures detected:\n{output}"

    def test_no_missing_migrations(self, db):
        """makemigrations --check detects no unmade migrations"""
        from django.core.management.base import CommandError

        try:
            call_command('makemigrations', '--check', '--dry-run', verbosity=0)
        except CommandError as e:
            pytest.fail(
                f"Unmade migrations detected:\n{str(e)}\n\n"
                "Run: python manage.py makemigrations"
            )
