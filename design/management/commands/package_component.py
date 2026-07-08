"""
Management command for packaging components.

Provides command-line interface for:
- Packaging component directories into ZIP files
- Validating component structure
- Generating manifest files
- Calculating package statistics

Examples:
    # Package component directory
    ./shop_venv/bin/python manage.py package_component --path=./my_component

    # Package with custom output directory
    ./shop_venv/bin/python manage.py package_component --path=./my_component --output=/tmp

    # Validate component structure without packaging
    ./shop_venv/bin/python manage.py package_component --path=./my_component --validate-only

    # Show package statistics
    ./shop_venv/bin/python manage.py package_component --path=./my_component --stats
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _

from design.component_packager import ComponentPackager, package_component


class Command(BaseCommand):
    help = 'Package component directories for distribution'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            required=True,
            help='Path to component directory to package',
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Output directory for package ZIP (default: component parent dir)',
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate structure, do not create package',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show package statistics',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        """Execute the command."""
        component_path = Path(options['path'])
        output_dir = Path(options['output']) if options['output'] else None
        validate_only = options['validate_only']
        show_stats = options['stats']
        verbose = options['verbose']

        # Check if component directory exists
        if not component_path.exists():
            raise CommandError(f"Component directory does not exist: {component_path}")

        # Create packager
        packager = ComponentPackager(component_path)

        # Validate structure
        self.stdout.write("🔍 Validating component structure...")
        is_valid, errors, warnings = packager.validate_structure()

        if not is_valid:
            self.stdout.write(self.style.ERROR("❌ Validation failed"))
            for error in errors:
                self.stdout.write(self.style.ERROR(f"  Error: {error}"))
            return

        self.stdout.write(self.style.SUCCESS("✅ Structure validation passed"))

        # Show warnings
        if warnings:
            for warning in warnings:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠️  {warning}")
                )

        # Show manifest info
        if verbose and packager.manifest:
            self.stdout.write("\n📋 Manifest:")
            self.stdout.write(f"  Component: {packager.manifest.get('component_type')}")
            self.stdout.write(f"  Version: {packager.manifest.get('version')}")
            self.stdout.write(f"  Author: {packager.manifest.get('author')}")

        # Show statistics
        if show_stats:
            self.stdout.write("\n📊 Package Statistics:")
            stats = packager.calculate_package_stats()
            self.stdout.write(f"  Total files: {stats['total_files']}")
            self.stdout.write(f"  Total size: {stats['total_size_kb']:.2f} KB")
            self.stdout.write(f"  Assets: {stats['asset_count']} files ({stats['asset_size_kb']:.2f} KB)")
            self.stdout.write(f"  Template: {stats['template_size_kb']:.2f} KB")

        # Validate only mode
        if validate_only:
            self.stdout.write(
                self.style.SUCCESS("\n✅ Validation complete (--validate-only)")
            )
            return

        # Create package
        self.stdout.write("\n📦 Creating package...")
        try:
            package_path = packager.package(output_dir=output_dir)
            package_size = package_path.stat().st_size / 1024  # KB

            self.stdout.write(
                self.style.SUCCESS(f"✅ Package created successfully")
            )
            self.stdout.write(f"  Path: {package_path}")
            self.stdout.write(f"  Size: {package_size:.2f} KB")

            if verbose:
                self.stdout.write(f"\n📦 Package contents:")
                import zipfile
                with zipfile.ZipFile(package_path, 'r') as zf:
                    for name in zf.namelist():
                        info = zf.getinfo(name)
                        self.stdout.write(
                            f"  {name} ({info.file_size} bytes)"
                        )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to create package: {e}")
            )
