"""
Management command to check for and apply platform hotfixes.

Usage:
    python manage.py check_hotfixes                # Check for hotfixes
    python manage.py check_hotfixes --apply        # Check and apply if available
    python manage.py check_hotfixes --rollback     # Remove applied hotfixes
    python manage.py check_hotfixes --status       # Show current hotfix status
"""

import json
from pathlib import Path

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from component_updates.services import PlatformUpdateError, PlatformUpdateService

_UPGRADER_URL = getattr(django_settings, "UPGRADER_URL", "http://upgrader:8080")


class Command(BaseCommand):
    help = "Check for and manage platform hotfixes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Automatically apply available hotfix via the upgrader service",
        )
        parser.add_argument(
            "--rollback",
            action="store_true",
            help="Remove applied hotfixes and restart with base image code",
        )
        parser.add_argument(
            "--status",
            action="store_true",
            help="Show current hotfix status only",
        )

    def handle(self, *args, **options):
        if options["status"]:
            self._show_status()
            return

        if options["rollback"]:
            self._rollback_hotfix()
            return

        self._check_and_optionally_apply(apply=options["apply"])

    def _get_current_hotfix_number(self):
        """Read the currently applied hotfix number from the marker file."""
        marker = Path("/app/hotfixes/.applied")
        if not marker.exists():
            return 0
        try:
            content = marker.read_text().strip()
            if "-hf" in content:
                return int(content.split("-hf")[1])
        except (ValueError, IndexError):
            pass
        return 0

    def _get_platform_version(self):
        """Get the current platform version."""
        try:
            import core

            return getattr(core, "__version__", "unknown")
        except ImportError:
            return "unknown"

    def _show_status(self):
        """Display current hotfix status."""
        version = self._get_platform_version()
        hotfix_num = self._get_current_hotfix_number()

        self.stdout.write(f"Platform version: v{version}")

        if hotfix_num > 0:
            self.stdout.write(self.style.WARNING(f"Applied hotfix:   hf{hotfix_num}"))
            # Read manifest for details
            manifest_path = Path(f"/app/hotfixes/{version}/hf{hotfix_num}/hotfix_manifest.json")
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)
                file_count = len(manifest.get("files", []))
                changelog = manifest.get("changelog", "")
                self.stdout.write(f"Files patched:    {file_count}")
                if changelog:
                    self.stdout.write(f"Changelog:        {changelog}")
        else:
            self.stdout.write(self.style.SUCCESS("No hotfixes applied (running base image code)"))

    def _check_and_optionally_apply(self, apply=False):
        """Check for available hotfixes and optionally apply."""
        service = PlatformUpdateService()
        version = service.get_current_version()
        current_hf = service.get_current_hotfix_number()

        self.stdout.write(f"Checking hotfixes for v{version} (current: hf{current_hf})...\n")

        try:
            data = service.check_for_hotfix()
        except PlatformUpdateError as e:
            self.stderr.write(self.style.ERROR(f"Failed to check for hotfixes: {e}"))
            return

        if not data.get("hotfix_available"):
            if data.get("maintenance_required"):
                self.stdout.write(
                    self.style.WARNING("Hotfixes available but require active maintenance.")
                )
            else:
                self.stdout.write(self.style.SUCCESS("No new hotfixes available."))
            return

        hotfix = data["latest_hotfix"]
        hf_num = hotfix["hotfix_number"]
        size_kb = hotfix.get("package_size_bytes", 0) / 1024

        self.stdout.write(self.style.WARNING(f"\nHotfix available: v{version}-hf{hf_num}"))
        if hotfix.get("security_update"):
            self.stdout.write(self.style.ERROR("  Type: SECURITY"))
        self.stdout.write(f"  Size: {size_kb:.1f} KB")
        if hotfix.get("changelog"):
            self.stdout.write(f"  Changelog: {hotfix['changelog']}")
        if hotfix.get("requires_migration"):
            self.stdout.write(self.style.WARNING("  Requires database migration"))

        if not apply:
            self.stdout.write("\nRun with --apply to apply this hotfix via the upgrader.")
            return

        # Apply via upgrader service
        self._apply_via_upgrader(version, hf_num)

    def _apply_via_upgrader(self, version, hotfix_number):
        """Send apply request to the upgrader service."""
        import requests

        self.stdout.write(f"\nApplying hotfix v{version}-hf{hotfix_number}...")

        try:
            payload = {
                "version": version,
                "hotfix_number": hotfix_number,
            }
            if getattr(django_settings, "FLEET_INSTANCE_NAME", ""):
                payload["instance"] = getattr(django_settings, "FLEET_INSTANCE_NAME", "")

            response = requests.post(
                f"{_UPGRADER_URL}/hotfixes/apply",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                self.stdout.write(
                    self.style.SUCCESS(
                        "Hotfix apply started. Containers will restart to apply the patch."
                    )
                )
            else:
                self.stderr.write(self.style.ERROR(f"Upgrader error: {data.get('error')}"))

        except requests.ConnectionError:
            self.stderr.write(
                self.style.ERROR(
                    "Could not connect to upgrader service. Is the upgrader container running?"
                )
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed: {e}"))

    def _rollback_hotfix(self):
        """Remove hotfixes via the upgrader service."""
        import requests

        self.stdout.write("Rolling back hotfixes...")

        try:
            payload = {}
            if getattr(django_settings, "FLEET_INSTANCE_NAME", ""):
                payload["instance"] = getattr(django_settings, "FLEET_INSTANCE_NAME", "")

            response = requests.post(
                f"{_UPGRADER_URL}/hotfixes/rollback",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                self.stdout.write(
                    self.style.SUCCESS(
                        "Hotfix rollback started. Containers will restart with base image code."
                    )
                )
            else:
                self.stderr.write(self.style.ERROR(f"Upgrader error: {data.get('error')}"))

        except requests.ConnectionError:
            self.stderr.write(self.style.ERROR("Could not connect to upgrader service."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed: {e}"))
