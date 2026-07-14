"""
Management command for signing components.

Provides command-line interface for:
- Signing individual components by ID or type
- Generating RSA keypair for signing
- Verifying component signatures
- Bulk signing operations

Examples:
    # Sign component by ID
    ./shop_venv/bin/python manage.py sign_component --component-id=1

    # Sign component by type
    ./shop_venv/bin/python manage.py sign_component --component-type=hero_banner

    # Sign all unsigned components
    ./shop_venv/bin/python manage.py sign_component --all

    # Generate new RSA keypair
    ./shop_venv/bin/python manage.py sign_component --generate-keys

    # Verify component signature
    ./shop_venv/bin/python manage.py sign_component --verify --component-id=1
"""

from django.core.management.base import BaseCommand, CommandError

from design.component_signer import get_component_signer
from design.models import ComponentStore


class Command(BaseCommand):
    help = "Sign component packages for distribution"

    def add_arguments(self, parser):
        parser.add_argument(
            "--component-id",
            type=int,
            help="Sign component by ID",
        )
        parser.add_argument(
            "--component-type",
            type=str,
            help="Sign component by type",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Sign all unsigned approved components",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-sign components that are already signed",
        )
        parser.add_argument(
            "--generate-keys",
            action="store_true",
            help="Generate new RSA keypair for signing",
        )
        parser.add_argument(
            "--verify",
            action="store_true",
            help="Verify component signature instead of signing",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed output",
        )

    def handle(self, *args, **options):
        """Execute the command."""

        # Generate keys
        if options["generate_keys"]:
            self._generate_keys()
            return

        # Verify signature
        if options["verify"]:
            self._verify_signature(options)
            return

        # Sign components
        if options["all"]:
            self._sign_all(options)
        elif options["component_id"]:
            self._sign_by_id(options["component_id"], options)
        elif options["component_type"]:
            self._sign_by_type(options["component_type"], options)
        else:
            raise CommandError(
                "Please specify --component-id, --component-type, --all, "
                "--generate-keys, or --verify"
            )

    def _generate_keys(self):
        """Generate new RSA keypair."""
        self.stdout.write(
            self.style.WARNING(
                "⚠️  WARNING: Generating new keys will invalidate all existing signatures!"
            )
        )
        confirm = input("Are you sure you want to continue? (yes/no): ")

        if confirm.lower() != "yes":
            self.stdout.write(self.style.ERROR("Aborted."))
            return

        signer = get_component_signer()
        private_key_path, public_key_path = signer.generate_keypair()

        self.stdout.write(self.style.SUCCESS("✅ RSA keypair generated successfully"))
        self.stdout.write(f"  Private key: {private_key_path}")
        self.stdout.write(f"  Public key: {public_key_path}")
        self.stdout.write(self.style.WARNING("\n⚠️  Keep the private key secure and backed up!"))

    def _verify_signature(self, options):
        """Verify component signature."""
        if options["component_id"]:
            component = self._get_component_by_id(options["component_id"])
        elif options["component_type"]:
            component = self._get_component_by_type(options["component_type"])
        else:
            raise CommandError("Please specify --component-id or --component-type with --verify")

        if not component.is_signed():
            self.stdout.write(self.style.ERROR(f"❌ Component '{component}' is not signed"))
            return

        is_valid, message = component.verify_integrity()

        if is_valid:
            self.stdout.write(self.style.SUCCESS(f"✅ {message}"))
            if options["verbose"]:
                self.stdout.write(f"  Component: {component}")
                self.stdout.write(f"  Checksum: {component.checksum_sha256}")
                self.stdout.write(f"  Signed by: {component.signed_by}")
                self.stdout.write(f"  Signed at: {component.signed_at}")
        else:
            self.stdout.write(self.style.ERROR(f"❌ {message}"))

    def _sign_all(self, options):
        """Sign all unsigned approved components."""
        force = options["force"]
        verbose = options["verbose"]

        # Get components to sign
        if force:
            components = ComponentStore.objects.filter(review_status="approved")
            self.stdout.write(f"🔍 Found {components.count()} approved components")
        else:
            components = ComponentStore.objects.filter(
                review_status="approved",
                signature="",
            )
            self.stdout.write(f"🔍 Found {components.count()} unsigned approved components")

        if not components.exists():
            self.stdout.write(self.style.WARNING("No components to sign"))
            return

        # Sign each component
        signed_count = 0
        failed_count = 0
        get_component_signer()

        for component in components:
            success, message = component.sign_package()

            if success:
                component.save()
                signed_count += 1
                if verbose:
                    self.stdout.write(self.style.SUCCESS(f"✅ Signed: {component}"))
            else:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f"❌ Failed to sign {component}: {message}"))

        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n✅ Signed {signed_count} component(s)"))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"❌ Failed to sign {failed_count} component(s)"))

    def _sign_by_id(self, component_id, options):
        """Sign component by ID."""
        component = self._get_component_by_id(component_id)
        self._sign_component(component, options)

    def _sign_by_type(self, component_type, options):
        """Sign component by type."""
        component = self._get_component_by_type(component_type)
        self._sign_component(component, options)

    def _sign_component(self, component, options):
        """Sign a single component."""
        force = options["force"]
        verbose = options["verbose"]

        # Check if already signed
        if component.is_signed() and not force:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Component '{component}' is already signed. Use --force to re-sign."
                )
            )
            return

        # Sign component
        success, message = component.sign_package()

        if success:
            component.save()
            self.stdout.write(self.style.SUCCESS(f"✅ {message}"))
            if verbose:
                self.stdout.write(f"  Component: {component}")
                self.stdout.write(f"  Checksum: {component.checksum_sha256}")
                self.stdout.write(f"  Signed by: {component.signed_by}")
                self.stdout.write(f"  Signed at: {component.signed_at}")
        else:
            self.stdout.write(self.style.ERROR(f"❌ {message}"))

    def _get_component_by_id(self, component_id):
        """Get component by ID."""
        try:
            return ComponentStore.objects.get(pk=component_id)
        except ComponentStore.DoesNotExist:
            raise CommandError(f"Component with ID {component_id} does not exist")

    def _get_component_by_type(self, component_type):
        """Get component by type."""
        try:
            return ComponentStore.objects.get(component_type=component_type)
        except ComponentStore.DoesNotExist:
            raise CommandError(f"Component with type '{component_type}' does not exist")
