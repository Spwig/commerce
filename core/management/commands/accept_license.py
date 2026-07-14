"""
Management command to accept the Spwig Software License Agreement.

Usage:
    # Interactive mode (default) - displays license, prompts for acceptance
    python manage.py accept_license

    # Auto-accept mode (for Docker/CI)
    python manage.py accept_license --auto-accept

    # Via environment variable
    SPWIG_ACCEPT_LICENSE=true python manage.py accept_license

    # Check current status
    python manage.py accept_license --status
"""

import os
import pydoc

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Accept the Spwig Software License Agreement"

    def add_arguments(self, parser):
        parser.add_argument(
            "--auto-accept",
            action="store_true",
            help="Automatically accept the license (for unattended installs)",
        )
        parser.add_argument(
            "--status",
            action="store_true",
            help="Show current license acceptance status",
        )

    def handle(self, *args, **options):
        from core.license_acceptance import get_license_acceptance_service

        service = get_license_acceptance_service()

        # Status check mode
        if options["status"]:
            self._show_status(service)
            return

        # Check if already accepted
        if service.is_accepted():
            needs_reaccept, change_type = service.needs_reacceptance()
            if not needs_reaccept:
                info = service.get_acceptance_info()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"License v{info.get('license_version', '?')} already accepted "
                        f"on {info.get('timestamp', 'unknown date')}"
                    )
                )
                return

            self.stdout.write(
                self.style.WARNING("License agreement has been updated. Re-acceptance required.")
            )

        # Load license text
        license_text = service.get_license_text()
        if not license_text:
            self.stderr.write(
                self.style.ERROR("LICENSE.txt not found. Cannot proceed with license acceptance.")
            )
            return

        license_version = service.extract_license_version(license_text) or "1.0.0"

        # Determine acceptance mode
        auto_accept = (
            options["auto_accept"] or os.environ.get("SPWIG_ACCEPT_LICENSE", "").lower() == "true"
        )

        if auto_accept:
            self._auto_accept(service, license_version)
        else:
            self._interactive_accept(service, license_text, license_version)

    def _show_status(self, service):
        """Display current acceptance status."""
        info = service.get_acceptance_info()

        if not info or not info.get("accepted"):
            self.stdout.write(
                self.style.WARNING(
                    "License has NOT been accepted.\nRun: python manage.py accept_license"
                )
            )
            return

        self.stdout.write(self.style.SUCCESS("License Acceptance Status"))
        self.stdout.write(f"  License version:  {info.get('license_version', '?')}")
        self.stdout.write(f"  Software version: {info.get('software_version', '?')}")
        self.stdout.write(f"  Accepted at:      {info.get('timestamp', '?')}")
        self.stdout.write(f"  Accepted via:     {info.get('accepted_via', '?')}")
        self.stdout.write(f"  Installation ID:  {info.get('installation_id', '?')}")

        if info.get("accepted_by_email"):
            self.stdout.write(f"  Accepted by:      {info['accepted_by_email']}")

        # Check if re-acceptance is needed
        needs_reaccept, _ = service.needs_reacceptance()
        if needs_reaccept:
            self.stdout.write(
                self.style.WARNING("\nLicense has been updated — re-acceptance required.")
            )

    def _interactive_accept(self, service, license_text, license_version):
        """Interactive license acceptance with paging."""
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("  SPWIG SOFTWARE LICENSE AGREEMENT")
        self.stdout.write(f"  Version: {license_version}")
        self.stdout.write("=" * 60)
        self.stdout.write("")
        self.stdout.write("The license will now be displayed. Press 'q' to exit the viewer.")
        self.stdout.write("")

        # Display license with paging
        try:
            pydoc.pager(license_text)
        except Exception:
            # Fallback: print directly if pager fails
            self.stdout.write(license_text)

        self.stdout.write("")

        # Prompt for acceptance
        try:
            response = (
                input(
                    f"Do you accept the Spwig Software License Agreement "
                    f"v{license_version}? (yes/no): "
                )
                .strip()
                .lower()
            )
        except (EOFError, KeyboardInterrupt):
            self.stdout.write("")
            self.stderr.write(self.style.ERROR("License acceptance cancelled."))
            return

        if response != "yes":
            self.stderr.write(
                self.style.ERROR(
                    "License must be accepted to use Spwig.\n"
                    "Run this command again when ready to accept."
                )
            )
            return

        # Record acceptance
        service.record_acceptance(accepted_via="cli")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nLicense v{license_version} accepted. You may now proceed with setup."
            )
        )

    def _auto_accept(self, service, license_version):
        """Auto-accept license (unattended mode)."""
        self.stdout.write(f"Auto-accepting license v{license_version}...")

        service.record_acceptance(accepted_via="env")

        self.stdout.write(
            self.style.SUCCESS(f"License v{license_version} auto-accepted. Proceeding with setup.")
        )
