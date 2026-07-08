"""
Django management command to generate JWT tokens for geocoder service
Usage: python manage.py generate_geocoder_token --merchant-id MERCHANT123 --tier premium
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from address_autocomplete.jwt_auth import GeocoderJWTAuth
import json
import uuid


class Command(BaseCommand):
    help = 'Generate JWT token for geocoder service access'

    def add_arguments(self, parser):
        parser.add_argument(
            '--merchant-id',
            type=str,
            required=True,
            help='Merchant ID'
        )
        parser.add_argument(
            '--installation-uuid',
            type=str,
            help='Installation UUID (auto-generated if not provided)'
        )
        parser.add_argument(
            '--tier',
            type=str,
            default='standard',
            choices=['standard', 'premium', 'enterprise'],
            help='Service tier'
        )
        parser.add_argument(
            '--expiry-hours',
            type=int,
            help='Token expiry in hours (overrides default)'
        )
        parser.add_argument(
            '--output-format',
            type=str,
            default='json',
            choices=['json', 'text', 'curl'],
            help='Output format'
        )

    def handle(self, *args, **options):
        # Initialize JWT auth
        auth = GeocoderJWTAuth()

        # Override expiry if provided
        if options['expiry_hours']:
            auth.expiry_hours = options['expiry_hours']

        # Generate installation UUID if not provided
        installation_uuid = options['installation_uuid'] or str(uuid.uuid4())

        # Generate token
        token_info = auth.generate_merchant_token(
            merchant_id=options['merchant_id'],
            installation_uuid=installation_uuid,
            tier=options['tier']
        )

        # Output in requested format
        if options['output_format'] == 'json':
            self.stdout.write(json.dumps(token_info, indent=2))

        elif options['output_format'] == 'text':
            self.stdout.write(self.style.SUCCESS('\n=== Geocoder JWT Token Generated ===\n'))
            self.stdout.write(f"Merchant ID: {options['merchant_id']}")
            self.stdout.write(f"Installation: {installation_uuid}")
            self.stdout.write(f"Tier: {options['tier']}")
            self.stdout.write(f"Rate Limit: {token_info['rate_limit']} req/min")
            self.stdout.write(f"Expires: {token_info['expires_at']}")
            self.stdout.write(self.style.WARNING(f"\nToken:\n{token_info['token']}\n"))

        elif options['output_format'] == 'curl':
            self.stdout.write('# Test the token with curl:')
            self.stdout.write(f'export GEOCODER_TOKEN="{token_info["token"]}"')
            self.stdout.write('curl -H "Authorization: Bearer $GEOCODER_TOKEN" \\')
            self.stdout.write('     -H "Content-Type: application/json" \\')
            self.stdout.write('     -X POST http://geocoder.spwig.com/api/v1/autocomplete \\')
            self.stdout.write('     -d \'{"query":"Singapore","limit":3}\'')

        # Log token generation
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Token generated for {options['merchant_id']} (tier: {options['tier']})"
            )
        )