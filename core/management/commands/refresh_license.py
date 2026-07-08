"""
Management command to refresh license.json from the update server.

Usage:
    # Normal refresh — updates license.json if data changed
    python manage.py refresh_license

    # Force write even if unchanged (re-signs license)
    python manage.py refresh_license --force

    # Show current vs server status without writing
    python manage.py refresh_license --status
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refresh license.json from the update server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force write license.json even if data is unchanged',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show current license status without refreshing',
        )

    def handle(self, *args, **options):
        from core.license import get_license_manager, is_sandbox_mode

        if is_sandbox_mode():
            self.stdout.write(self.style.WARNING(
                "Sandbox mode — no license to refresh."
            ))
            return

        if options['status']:
            self._show_status()
            return

        self._do_refresh(force=options['force'])

    def _show_status(self):
        """Display current license status."""
        from core.license import get_license_manager

        manager = get_license_manager(force_reload=True)
        info = manager.get_license_info()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Current License Status"))
        self.stdout.write(f"  License key:    {info.get('license_key', 'N/A')}")
        self.stdout.write(f"  License type:   {info.get('license_type', 'N/A')}")
        self.stdout.write(f"  Owner:          {info.get('owner_name', 'N/A')}")
        self.stdout.write(f"  Valid:           {info.get('is_valid', False)}")
        self.stdout.write(f"  Environment:    {info.get('environment_type', 'N/A')}")

        # Maintenance
        self.stdout.write("")
        self.stdout.write("  Maintenance")
        self.stdout.write(f"    Active:        {info.get('maintenance_active', 'N/A')}")
        expires = info.get('maintenance_expires_at')
        if expires:
            self.stdout.write(f"    Expires:       {expires}")
        else:
            self.stdout.write(f"    Expires:       Perpetual")
        days = info.get('maintenance_days_remaining')
        if days is not None:
            self.stdout.write(f"    Days left:     {days}")

        # Revocation
        if info.get('revocation_pending'):
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("  Revocation Pending"))
            self.stdout.write(f"    Reason:        {info.get('revocation_reason')}")
            self.stdout.write(f"    Grace days:    {info.get('revocation_grace_days_remaining')}")

        self.stdout.write("")

    def _do_refresh(self, force=False):
        """Perform the license refresh."""
        from component_updates.services import UpdateManager

        self.stdout.write("Refreshing license from update server...")

        try:
            manager = UpdateManager()
            result = manager.refresh_license(force_write=force)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Refresh failed: {e}"))
            return

        if result.get('error'):
            error = result['error']
            if error in ('license_revoked', 'license_expired'):
                self.stderr.write(self.style.ERROR(
                    f"License {error}: {result.get('message', '')}"
                ))
            elif error == 'sandbox_mode':
                self.stdout.write(self.style.WARNING("Sandbox mode — skipped."))
            elif error.startswith('auth_failed'):
                self.stderr.write(self.style.ERROR(
                    f"Authentication failed: {error}"
                ))
            else:
                self.stderr.write(self.style.WARNING(f"Refresh issue: {error}"))
            return

        if result.get('refreshed'):
            changes = result.get('changes', [])
            self.stdout.write(self.style.SUCCESS(
                f"License refreshed. Changed fields: {', '.join(changes) if changes else 'force_write'}"
            ))

            maint = result.get('maintenance_status', {})
            if maint:
                active = maint.get('active', False)
                style = self.style.SUCCESS if active else self.style.WARNING
                self.stdout.write(style(
                    f"  Maintenance: {'active' if active else 'inactive'}"
                ))
                expires = maint.get('expires_at')
                if expires:
                    self.stdout.write(f"  Expires: {expires}")
                elif active:
                    self.stdout.write(f"  Expires: Perpetual")
        else:
            self.stdout.write("No changes detected — license is up to date.")
