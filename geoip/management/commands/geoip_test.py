"""
Test GeoIP functionality
"""

import json

from django.core.management.base import BaseCommand
from django.test import RequestFactory

from geoip.middleware import GeoIPMiddleware


class Command(BaseCommand):
    help = "Test GeoIP resolution for a given IP address"

    def add_arguments(self, parser):
        parser.add_argument(
            "ip", nargs="?", default="8.8.8.8", help="IP address to test (default: 8.8.8.8)"
        )
        parser.add_argument("--verbose", action="store_true", help="Show detailed output")

    def handle(self, *args, **options):
        ip = options["ip"]
        verbose = options["verbose"]

        self.stdout.write(f"Testing GeoIP for IP: {ip}")
        self.stdout.write("-" * 50)

        # Create a fake request
        factory = RequestFactory()
        request = factory.get("/")
        request.META["REMOTE_ADDR"] = ip

        # Test middleware
        middleware = GeoIPMiddleware(lambda r: r)
        request = middleware(request)

        # Get location
        if hasattr(request, "geo_location"):
            location = request.geo_location

            if location:
                self.stdout.write(self.style.SUCCESS("✓ Location resolved successfully"))
                self.stdout.write("")

                # Display key information
                self.stdout.write(
                    f"Country: {location.get('country', 'Unknown')} "
                    f"{self._country_flag(location.get('country', ''))}"
                )
                self.stdout.write(f"City: {location.get('city', 'Unknown')}")
                self.stdout.write(f"Region: {location.get('region', 'Unknown')}")
                self.stdout.write(f"Postal Code: {location.get('postal_code', 'Unknown')}")
                self.stdout.write(
                    f"Coordinates: {location.get('lat', 'N/A')}, {location.get('lon', 'N/A')}"
                )
                self.stdout.write(f"Currency: {location.get('currency', 'Unknown')}")
                self.stdout.write(f"Language: {location.get('language', 'Unknown')}")
                self.stdout.write(f"Source: {location.get('source', 'Unknown')}")
                self.stdout.write(f"Confidence: {location.get('confidence', 0) * 100:.0f}%")

                # Check for special flags
                if location.get("is_vpn"):
                    self.stdout.write(self.style.WARNING("⚠ VPN detected"))
                if location.get("is_proxy"):
                    self.stdout.write(self.style.WARNING("⚠ Proxy detected"))
                if location.get("is_tor"):
                    self.stdout.write(self.style.WARNING("⚠ Tor detected"))

                if verbose:
                    self.stdout.write("")
                    self.stdout.write("Full response:")
                    self.stdout.write(json.dumps(location, indent=2, default=str))

            else:
                self.stdout.write(self.style.ERROR("✗ Failed to resolve location"))

        else:
            self.stdout.write(self.style.ERROR("✗ GeoIP middleware not configured properly"))

    def _country_flag(self, country_code):
        """Convert country code to flag emoji"""
        if not country_code or len(country_code) != 2:
            return ""
        return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in country_code.upper())
