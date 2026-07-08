"""
Create sample update data for testing the admin interface
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from component_updates.models import (
    ComponentRegistry,
    ComponentVersion,
    UpdateLog,
    UpdateServerConfig
)


class Command(BaseCommand):
    help = 'Create sample update data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample update data...\n')

        # Create update server config
        config, created = UpdateServerConfig.objects.get_or_create(
            pk=1,
            defaults={
                'server_url': 'https://updates.spwig.com',
                'api_version': 'v1',
                'is_connected': True,
                'last_check': timezone.now() - timedelta(hours=2),
                'check_interval_hours': 24,
                'auto_download': True,
                'auto_install_security': True,
                'send_telemetry': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created update server config'))

        # Mark some components as having updates available
        components = ComponentRegistry.objects.all()[:5]
        for i, component in enumerate(components):
            component.update_available = True
            component.latest_version = self.bump_version(component.current_version)
            component.last_checked = timezone.now() - timedelta(hours=i)
            component.save()
            self.stdout.write(f'  ✓ {component.name}: v{component.current_version} → v{component.latest_version}')

        # Create some update logs
        self.stdout.write('\n📝 Creating update logs...')

        # Successful update
        component = components[0]
        log = UpdateLog.objects.create(
            component=component,
            action='update',
            status='completed',
            old_version='0.9.0',
            new_version='1.0.0',
            started_at=timezone.now() - timedelta(days=2),
            completed_at=timezone.now() - timedelta(days=2) + timedelta(seconds=15),
            duration_seconds=15,
            is_automatic=False
        )
        self.stdout.write(f'  ✓ Update log: {component.name} (successful)')

        # Failed update
        component = components[1]
        log = UpdateLog.objects.create(
            component=component,
            action='update',
            status='failed',
            old_version='1.0.0',
            new_version='1.1.0',
            started_at=timezone.now() - timedelta(days=1),
            completed_at=timezone.now() - timedelta(days=1) + timedelta(seconds=5),
            duration_seconds=5,
            error_message='Failed to download package: Connection timeout',
            error_traceback='Traceback (most recent call last):\n  File "update.py", line 42, in download\n    raise TimeoutError()',
            is_automatic=True
        )
        self.stdout.write(f'  ✓ Update log: {component.name} (failed)')

        # Rollback
        component = components[2]
        log = UpdateLog.objects.create(
            component=component,
            action='rollback',
            status='completed',
            old_version='1.2.0',
            new_version='1.1.0',
            started_at=timezone.now() - timedelta(hours=6),
            completed_at=timezone.now() - timedelta(hours=6) + timedelta(seconds=3),
            duration_seconds=3,
            is_automatic=False,
            details={'reason': 'Breaking changes detected'}
        )
        self.stdout.write(f'  ✓ Update log: {component.name} (rollback)')

        # Health check
        component = components[3]
        log = UpdateLog.objects.create(
            component=component,
            action='health_check',
            status='completed',
            started_at=timezone.now() - timedelta(hours=1),
            completed_at=timezone.now() - timedelta(hours=1) + timedelta(seconds=1),
            duration_seconds=1,
            is_automatic=True,
            details={'checks_passed': 12, 'checks_failed': 0}
        )
        self.stdout.write(f'  ✓ Update log: {component.name} (health check)')

        # Create additional versions for rollback testing
        self.stdout.write('\n📦 Creating version history...')
        test_component = components[0]

        versions_data = [
            ('0.9.0', 'healthy', False, timezone.now() - timedelta(days=30)),
            ('1.0.0', 'healthy', True, timezone.now() - timedelta(days=2)),
            ('1.1.0', 'unknown', False, None),  # Available but not installed
        ]

        for version, health, is_active, installed_at in versions_data:
            if installed_at:
                v, created = ComponentVersion.objects.update_or_create(
                    component=test_component,
                    version=version,
                    defaults={
                        'is_active': is_active,
                        'health_status': health,
                        'installed_at': installed_at,
                        'rollback_available': True,
                        'install_method': 'update_server',
                        'package_size_bytes': 15360,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Version: {test_component.name} v{version}')

        # Lock one component
        components[4].locked = True
        components[4].lock_reason = 'Custom modifications - do not update'
        components[4].save()
        self.stdout.write(f'\n🔒 Locked: {components[4].name}')

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully'))
        self.stdout.write(f'\n📊 Summary:')
        self.stdout.write(f'  Components with updates: {ComponentRegistry.objects.filter(update_available=True).count()}')
        self.stdout.write(f'  Locked components: {ComponentRegistry.objects.filter(locked=True).count()}')
        self.stdout.write(f'  Total versions: {ComponentVersion.objects.count()}')
        self.stdout.write(f'  Update logs: {UpdateLog.objects.count()}')
        self.stdout.write(f'\n🌐 Admin URL: /admin/component_updates/')

    def bump_version(self, version):
        """Bump the patch version"""
        try:
            major, minor, patch = version.split('.')
            return f'{major}.{minor}.{int(patch) + 1}'
        except:
            return '1.0.1'
