"""
Management command to activate Spwig with a setup token.

Usage:
    python manage.py activate_with_token <setup_token>

This is the CLI counterpart of the /activate/ web view.
Both use core.activation for the shared activation logic.

Typical use: docker-entrypoint.sh passes SETUP_TOKEN env var for
headless / automated activations (cloud deploys, CI, etc.).
"""

import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Activate this Spwig installation using a setup token'

    def add_arguments(self, parser):
        parser.add_argument(
            'token',
            type=str,
            help='The JWT setup token from your purchase email or spwig.com dashboard',
        )
        parser.add_argument(
            '--domain',
            type=str,
            default='localhost',
            help='The domain this installation will run on (default: localhost)',
        )

    def handle(self, *args, **options):
        from core.activation import activate_with_token

        token = options['token'].strip()
        domain = options['domain']

        if not token:
            self.stderr.write(self.style.ERROR('Setup token is required.'))
            sys.exit(1)

        self.stdout.write(f'Activating with domain: {domain}')
        self.stdout.write('Validating setup token...')

        result = activate_with_token(token, domain=domain)

        if result.success:
            self.stdout.write(self.style.SUCCESS('Activation successful!'))
            self.stdout.write(f'  License type: {result.license_type}')
            if result.owner_name:
                self.stdout.write(f'  Owner: {result.owner_name}')
            if result.admin_username:
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('Admin credentials (save these!):'))
                self.stdout.write(f'  Username: {result.admin_username}')
                self.stdout.write(f'  Password: {result.admin_password}')
            self.stdout.write('')
            self.stdout.write('You can now log in at /en/admin/')
        else:
            self.stderr.write(self.style.ERROR(f'Activation failed: {result.error}'))
            sys.exit(1)
