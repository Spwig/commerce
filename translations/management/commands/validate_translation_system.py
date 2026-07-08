from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from translations.utils import SystemValidator
from translations.client import get_translator_client


class Command(BaseCommand):
    help = _('Validate translation system requirements and configuration')

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help=_('Show detailed information')
        )

    def handle(self, *args, **options):
        verbose = options['verbose']

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                _('Translation System Validation')
            )
        )
        self.stdout.write('=' * 50)

        # Check system requirements
        validator = SystemValidator()
        check_result = validator.check_requirements()

        # Display system info
        self.stdout.write(
            _('\nSystem Information:')
        )
        self.stdout.write(
            _('  CPU Cores: %(cores)d') % {'cores': check_result['cpu_cores']}
        )
        self.stdout.write(
            _('  RAM: %(ram).1f GB') % {'ram': check_result['ram_gb']}
        )
        self.stdout.write(
            _('  Free Disk: %(disk).1f GB') % {'disk': check_result['disk_free_gb']}
        )

        # Check Docker
        if check_result['docker_available']:
            self.stdout.write(
                self.style.SUCCESS(
                    _('  Docker: ✓ Available')
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    _('  Docker: ✗ Not Available')
                )
            )

        # Check requirements
        self.stdout.write(_('\nRequirements Check:'))

        if check_result['meets_requirements']:
            self.stdout.write(
                self.style.SUCCESS(
                    _('  ✓ Minimum requirements met')
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    _('  ✗ Minimum requirements NOT met')
                )
            )
            for warning in check_result['warnings']:
                self.stdout.write(
                    self.style.WARNING(f'    - {warning}')
                )

        if check_result['meets_recommended']:
            self.stdout.write(
                self.style.SUCCESS(
                    _('  ✓ Recommended specifications met')
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    _('  ⚠ Recommended specifications not fully met')
                )
            )
            if verbose:
                for rec in check_result.get('recommendations', []):
                    self.stdout.write(f'    - {rec}')

        # Check translator service
        self.stdout.write(_('\nTranslator Service:'))

        client = get_translator_client()
        if client.is_available():
            self.stdout.write(
                self.style.SUCCESS(
                    _('  ✓ Service is online and responding')
                )
            )

            # Get service info
            info = client.get_system_info()
            if info and verbose:
                self.stdout.write(
                    _('    Model: %(model)s') % {
                        'model': info.get('model_name', 'Unknown')
                    }
                )
                self.stdout.write(
                    _('    Languages: %(langs)s') % {
                        'langs': ', '.join(info.get('available_languages', []))
                    }
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    _('  ✗ Service is offline or not responding')
                )
            )

        # Check GPU if available
        gpu_info = validator.get_gpu_info()
        if gpu_info['available']:
            self.stdout.write(_('\nGPU Information:'))
            self.stdout.write(
                self.style.SUCCESS(
                    _('  ✓ GPU Available')
                )
            )
            if verbose:
                for gpu in gpu_info['devices']:
                    self.stdout.write(
                        _('    - %(name)s (%(memory)s)') % gpu
                    )
        else:
            self.stdout.write(
                _('\n  GPU: Not available (CPU mode will be used)')
            )

        # Summary
        self.stdout.write('\n' + '=' * 50)
        if check_result['status'] == 'success':
            self.stdout.write(
                self.style.SUCCESS(
                    _('\n✅ %(message)s') % check_result
                )
            )
        elif check_result['status'] == 'warning':
            self.stdout.write(
                self.style.WARNING(
                    _('\n⚠️  %(message)s') % check_result
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    _('\n❌ %(message)s') % check_result
                )
            )