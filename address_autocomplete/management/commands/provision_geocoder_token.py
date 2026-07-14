"""
Django management command to provision geocoder JWT token based on license
Usage: python manage.py provision_geocoder_token
"""

import asyncio
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from address_autocomplete.license_integration import LicenseBasedGeocoderAuth


class Command(BaseCommand):
    help = "Provision geocoder JWT token based on platform license"

    def add_arguments(self, parser):
        parser.add_argument("--license-key", type=str, help="Override license key from settings")
        parser.add_argument("--installation-uuid", type=str, help="Override installation UUID")
        parser.add_argument(
            "--save-to-settings", action="store_true", help="Save token to settings file"
        )
        parser.add_argument(
            "--output-format",
            type=str,
            default="json",
            choices=["json", "text", "env"],
            help="Output format",
        )

    def handle(self, *args, **options):
        # Get license key
        license_key = options.get("license_key") or getattr(settings, "PLATFORM_LICENSE_KEY", None)

        if not license_key:
            self.stdout.write(
                self.style.ERROR(
                    "No license key provided. Use --license-key or set PLATFORM_LICENSE_KEY in settings"
                )
            )
            return

        # Get or generate installation UUID
        installation_uuid = options.get("installation_uuid") or getattr(
            settings, "INSTALLATION_UUID", None
        )
        if not installation_uuid:
            import platform
            import uuid

            hostname = platform.node()
            installation_uuid = str(
                uuid.uuid5(uuid.NAMESPACE_DNS, f"{hostname}-{timezone.now().isoformat()}")
            )
            self.stdout.write(f"Generated installation UUID: {installation_uuid}")

        # Initialize auth manager
        auth_manager = LicenseBasedGeocoderAuth()

        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.stdout.write("Validating license with update server...")

        try:
            result = loop.run_until_complete(
                auth_manager.validate_license_and_get_token(license_key, installation_uuid)
            )
        finally:
            loop.close()

        if not result["success"]:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to provision token: {result.get('error', 'Unknown error')}"
                )
            )
            return

        # Output results
        if options["output_format"] == "json":
            self.stdout.write(
                json.dumps(
                    {
                        "token": result["token"],
                        "expires_at": result["expires_at"],
                        "tier": result["tier"],
                        "rate_limit": result["rate_limit"],
                        "merchant_id": result["merchant_id"],
                        "license_type": result["license_type"],
                    },
                    indent=2,
                )
            )

        elif options["output_format"] == "text":
            self.stdout.write(self.style.SUCCESS("\n=== Geocoder Token Provisioned ===\n"))
            self.stdout.write(f"License Type: {result['license_type']}")
            self.stdout.write(f"Geocoder Tier: {result['tier']}")
            self.stdout.write(f"Rate Limit: {result['rate_limit']} req/min")
            self.stdout.write(f"Merchant ID: {result['merchant_id']}")
            self.stdout.write(f"Expires: {result['expires_at']}")
            self.stdout.write(self.style.WARNING(f"\nToken:\n{result['token']}\n"))

        elif options["output_format"] == "env":
            self.stdout.write("# Add to your .env or settings:")
            self.stdout.write(f'GEOCODER_JWT_TOKEN="{result["token"]}"')
            self.stdout.write(f'GEOCODER_MERCHANT_ID="{result["merchant_id"]}"')
            self.stdout.write(f'GEOCODER_TIER="{result["tier"]}"')

        # Save to settings file if requested
        if options["save_to_settings"]:
            self._save_to_settings(result)

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Token provisioned successfully for {result['license_type']} license (tier: {result['tier']})"
            )
        )

    def _save_to_settings(self, result):
        """Save token to local settings file."""
        settings_file = "settings_local.py"

        settings_content = f"""
# Geocoder JWT Token Configuration
# Generated: {timezone.now().isoformat()}
# License Type: {result["license_type"]}
# Tier: {result["tier"]}

GEOCODER_JWT_TOKEN = '{result["token"]}'
GEOCODER_MERCHANT_ID = '{result["merchant_id"]}'
GEOCODER_TIER = '{result["tier"]}'
GEOCODER_TOKEN_EXPIRES = '{result["expires_at"]}'
"""

        try:
            with open(settings_file, "a") as f:
                f.write(settings_content)
            self.stdout.write(f"Token saved to {settings_file}")
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not save to {settings_file}: {e}"))
