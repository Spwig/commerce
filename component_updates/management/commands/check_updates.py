"""
Management command to check for component updates.

Usage:
    python manage.py check_updates                    # Check all components
    python manage.py check_updates --install          # Check and auto-install
    python manage.py check_updates --component logo   # Check specific component
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from component_updates.models import ComponentRegistry, UpdateLog
from component_updates.services import UpdateManager, UpdateAuthenticationError


class Command(BaseCommand):
    help = 'Check for component updates from the update server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--component',
            type=str,
            help='Specific component slug to check (e.g., "logo")',
        )
        parser.add_argument(
            '--install',
            action='store_true',
            help='Automatically install available updates',
        )
        parser.add_argument(
            '--auto-only',
            action='store_true',
            help='Only install components with auto_update enabled',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('🔍 Checking for component updates...\n'))

        manager = UpdateManager()

        # Get component(s) to check
        if options['component']:
            component = ComponentRegistry.objects.filter(slug=options['component']).first()
            if not component:
                raise CommandError(f'Component not found: {options["component"]}')
            components = [component]
        else:
            components = None

        try:
            # Check for updates
            result = manager.check_for_updates(component=components[0] if components else None)

            self.stdout.write(
                f'\n📊 Checked {ComponentRegistry.objects.filter(locked=False).count()} components\n'
            )

            if result['updates_found'] == 0:
                self.stdout.write(self.style.SUCCESS('✅ All components are up to date!\n'))
                return

            # Display available updates
            self.stdout.write(
                self.style.WARNING(f'\n⬆️  Found {result["updates_found"]} update(s) available:\n')
            )

            for update in result['updates']:
                comp = update['component']
                self.stdout.write(
                    f'\n  📦 {comp.name} ({comp.component_type})\n'
                    f'     Current: {update["current_version"]}\n'
                    f'     Latest:  {update["latest_version"]}\n'
                )

                if update.get('critical'):
                    self.stdout.write(
                        self.style.ERROR('     ⚠️  CRITICAL UPDATE - Security or stability fix\n')
                    )

                if update.get('changelog'):
                    self.stdout.write(f'     Changes: {update["changelog"]}\n')

            # Install updates if requested
            if options['install']:
                self.stdout.write('\n')
                self._install_updates(manager, result['updates'], options['auto_only'])
            else:
                self.stdout.write(
                    f'\n💡 To install updates, run: python manage.py check_updates --install\n'
                )

        except UpdateAuthenticationError as e:
            raise CommandError(f'Authentication failed: {e}')
        except Exception as e:
            raise CommandError(f'Update check failed: {e}')

    def _install_updates(self, manager: UpdateManager, updates: list, auto_only: bool):
        """Install available updates"""
        self.stdout.write(self.style.HTTP_INFO('📥 Installing updates...\n'))

        installed_count = 0
        skipped_count = 0
        failed_count = 0

        for update in updates:
            component = update['component']

            # Skip if auto_only and component doesn't have auto_update
            if auto_only and not component.auto_update:
                self.stdout.write(
                    self.style.WARNING(f'⏭️  Skipping {component.name} (auto-update disabled)\n')
                )
                skipped_count += 1
                continue

            # Skip if locked
            if component.locked:
                self.stdout.write(
                    self.style.WARNING(f'🔒 Skipping {component.name} (locked)\n')
                )
                skipped_count += 1
                continue

            self.stdout.write(f'\n📦 Installing {component.name} v{update["latest_version"]}...')

            try:
                success = manager.install_update(component, update['latest_version'])

                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f' ✅ Installed successfully\n')
                    )
                    installed_count += 1
                else:
                    self.stdout.write(
                        self.style.ERROR(f' ❌ Installation failed\n')
                    )
                    failed_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f' ❌ Error: {e}\n')
                )
                failed_count += 1

        # Summary
        self.stdout.write(f'\n{"="*60}\n')
        self.stdout.write(f'📊 Installation Summary:\n')
        self.stdout.write(f'   ✅ Installed: {installed_count}\n')
        if skipped_count:
            self.stdout.write(f'   ⏭️  Skipped:   {skipped_count}\n')
        if failed_count:
            self.stdout.write(self.style.ERROR(f'   ❌ Failed:    {failed_count}\n'))
        self.stdout.write(f'{"="*60}\n')
