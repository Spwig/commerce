"""
Management command to update exchange rates from configured providers.

Usage:
    python manage.py update_rates
    python manage.py update_rates --base USD
    python manage.py update_rates --currencies EUR,GBP,JPY
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from exchange_rates.services.exchange_service import ExchangeRateService
from exchange_rates.models import ExchangeRateProviderAccount
from core.models import SiteSettings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update exchange rates from configured providers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--base',
            type=str,
            help='Base currency to use (defaults to site default_currency)',
        )

        parser.add_argument(
            '--currencies',
            type=str,
            help='Comma-separated list of target currencies (e.g., EUR,GBP,JPY)',
        )

        parser.add_argument(
            '--site',
            type=int,
            help='Site ID (defaults to current site)',
        )

        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if cached rates are fresh',
        )

    def handle(self, *args, **options):
        # Get site
        if options['site']:
            try:
                site = Site.objects.get(pk=options['site'])
            except Site.DoesNotExist:
                raise CommandError(f"Site with ID {options['site']} does not exist")
        else:
            site = Site.objects.get_current()

        self.stdout.write(f"Updating rates for site: {site.name}")

        # Check if multi-currency is enabled
        settings = SiteSettings.get_settings()
        if not settings.enable_multi_currency:
            self.stdout.write(self.style.WARNING("Multi-currency is not enabled in Site Settings"))
            self.stdout.write("Updating rates anyway for testing purposes...")

        # Check for active providers
        active_providers = ExchangeRateProviderAccount.objects.filter(
            site=site,
            is_active=True
        ).count()

        if active_providers == 0:
            raise CommandError(
                "No active exchange rate providers configured. "
                "Please add and configure a provider in Admin → Exchange Rates → Provider Accounts"
            )

        self.stdout.write(f"Found {active_providers} active provider(s)")

        # Initialize service
        service = ExchangeRateService(site=site)

        # Determine base currency
        base_currency = options.get('base') or settings.default_currency
        self.stdout.write(f"Base currency: {base_currency}")

        # Determine target currencies
        if options.get('currencies'):
            target_currencies = [c.strip().upper() for c in options['currencies'].split(',')]
            self.stdout.write(f"Target currencies: {', '.join(target_currencies)}")
        else:
            if settings.supported_currencies:
                target_currencies = [c for c in settings.supported_currencies if c != base_currency]
                self.stdout.write(f"Using configured supported currencies: {', '.join(target_currencies)}")
            else:
                from core.utils.currency_helpers import get_common_currencies
                target_currencies = [code for code, _ in get_common_currencies() if code != base_currency]
                self.stdout.write(f"Using common currencies (no specific currencies configured)")

        if not target_currencies:
            raise CommandError("No target currencies to update")

        # Update rates
        self.stdout.write(self.style.SUCCESS(f"\nUpdating {len(target_currencies)} exchange rates...\n"))

        success_count = 0
        failure_count = 0

        for target_currency in target_currencies:
            try:
                # Clear cache if force flag is set
                if options['force']:
                    from django.core.cache import cache
                    cache_key = f'exchange_rate:{base_currency}:{target_currency}'
                    cache.delete(cache_key)

                rate = service.get_rate(base_currency, target_currency)

                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ {base_currency}/{target_currency}: {rate}")
                )
                success_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  ✗ {base_currency}/{target_currency}: {str(e)}")
                )
                failure_count += 1

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated: {success_count} rates")
        )

        if failure_count > 0:
            self.stdout.write(
                self.style.WARNING(f"Failed to update: {failure_count} rates")
            )

        self.stdout.write("=" * 60)

        # Exit code
        if failure_count > 0:
            self.stdout.write(
                self.style.WARNING("\nSome rates failed to update. Check logs for details.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("\n✓ All rates updated successfully!")
            )
