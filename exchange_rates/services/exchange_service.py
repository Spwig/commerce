"""
Exchange Rate Service

Centralized service for fetching, caching, and converting currencies.
Handles provider fallback chain and exchange rate markup application.
"""

from decimal import Decimal
from typing import Optional
from django.core.cache import cache
from django.utils import timezone
from django.db import transaction
from django.contrib.sites.models import Site
from exchange_rates.models import ExchangeRate, ExchangeRateHistory, ExchangeRateProviderAccount, ManualExchangeRate
from exchange_rates.providers.base import RateFetchError
from core.models import SiteSettings
import logging

logger = logging.getLogger(__name__)


class ExchangeRateService:
    """
    Service for fetching, caching, and converting currencies.
    Handles provider fallback chain and markup application.
    """

    def __init__(self, site=None):
        """
        Initialize exchange rate service.

        Args:
            site: Django Site instance (defaults to current site)
        """
        self.site = site or Site.objects.get_current()
        self.settings = SiteSettings.get_settings()

    def _get_cache_ttl(self):
        """Get Redis cache TTL in seconds based on sync interval setting."""
        TTL_MAP = {
            'realtime': 300,      # 5 min
            'hourly': 1800,       # 30 min
            'daily': 3600,        # 1 hour
            'weekly': 21600,      # 6 hours
            'monthly': 43200,     # 12 hours
            'quarterly': 86400,   # 24 hours
            'manual_only': 3600,  # 1 hour (manual rates still cached)
        }
        interval = getattr(self.settings, 'exchange_rate_sync_interval', 'daily')
        return TTL_MAP.get(interval, 300)

    def convert(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """
        Convert amount from one currency to another.

        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., 'USD')
            to_currency: Target currency code (e.g., 'EUR')

        Returns:
            Converted amount in target currency with proper rounding

        Example:
            >>> service = ExchangeRateService()
            >>> service.convert(Decimal('100.00'), 'USD', 'EUR')
            Decimal('85.00')
        """
        if from_currency == to_currency:
            return amount

        rate = self.get_rate(from_currency, to_currency)

        # Apply exchange rate markup if enabled
        if self.settings.exchange_rate_markup_enabled:
            markup_decimal = Decimal(str(self.settings.exchange_rate_markup_percentage)) / Decimal('100')
            rate = rate * (Decimal('1') + markup_decimal)

        converted = amount * rate

        # Round according to target currency decimal places
        from core.utils.currency_helpers import round_money
        return round_money(converted, to_currency)

    def get_rate(self, from_currency: str, to_currency: str) -> Decimal:
        """
        Get exchange rate between two currencies.
        Uses caching and provider fallback chain.

        Priority:
        1. Redis cache (5 min TTL)
        2. Manual exchange rates (merchant-defined, always fresh)
        3. Database cache (24 hr TTL if not stale)
        4. Provider API (with fallback chain by priority)

        Args:
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            Exchange rate as Decimal (e.g., 0.85 means 1 USD = 0.85 EUR)

        Raises:
            RateFetchError: If no rate available from any source
        """
        if from_currency == to_currency:
            return Decimal('1.0')

        # Try Redis cache first (fastest)
        cache_key = f'exchange_rate:{from_currency}:{to_currency}'
        cached_rate = cache.get(cache_key)
        if cached_rate:
            logger.debug(f"Rate {from_currency}/{to_currency} from Redis cache")
            return Decimal(str(cached_rate))

        # Try manual exchange rates (merchant-defined, take precedence)
        manual_rate = self._get_manual_rate(from_currency, to_currency)
        if manual_rate is not None:
            cache.set(cache_key, str(manual_rate), self._get_cache_ttl())
            return manual_rate

        # Try database cache (if not stale)
        # Use rate selection strategy to determine which provider's rate to use
        try:
            # Build query based on selection strategy
            rate_query = ExchangeRate.objects.filter(
                base_currency=from_currency,
                target_currency=to_currency,
                provider_account__is_active=True
            )

            # Apply strategy
            if self.settings.exchange_rate_selection_strategy == 'primary':
                # Try primary provider first
                db_rate = rate_query.filter(
                    provider_account__is_primary=True
                ).order_by('-fetched_at').first()

                # Fallback to latest from any provider if primary has no rate
                if not db_rate or db_rate.is_stale:
                    logger.debug(f"Primary provider has no fresh rate for {from_currency}/{to_currency}, falling back to latest")
                    db_rate = rate_query.order_by('-fetched_at').first()
            else:
                # 'latest' strategy - use most recently synced rate from any provider
                db_rate = rate_query.order_by('-fetched_at').first()

            if db_rate and not db_rate.is_stale:
                logger.debug(f"Rate {from_currency}/{to_currency} from database cache (provider: {db_rate.provider_account.name}, strategy: {self.settings.exchange_rate_selection_strategy})")
                cache.set(cache_key, str(db_rate.rate), self._get_cache_ttl())
                return db_rate.rate

        except Exception as e:
            logger.warning(f"Database cache lookup failed: {e}")

        # Fetch from provider with fallback chain
        logger.info(f"Fetching rate {from_currency}/{to_currency} from providers")
        rate = self._fetch_from_providers(from_currency, to_currency)

        if not rate:
            raise RateFetchError(f"Could not fetch rate for {from_currency}/{to_currency} from any provider")

        # Cache the fetched rate
        cache.set(cache_key, str(rate), self._get_cache_ttl())
        self._cache_rate_in_db(from_currency, to_currency, rate)

        return rate

    def _get_manual_rate(self, from_currency: str, to_currency: str) -> Optional[Decimal]:
        """
        Check for an active manual exchange rate for this currency pair.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            Exchange rate as Decimal or None if no manual rate exists
        """
        try:
            manual_rate = ManualExchangeRate.objects.filter(
                site=self.site,
                base_currency=from_currency,
                target_currency=to_currency,
                is_active=True
            ).first()

            if manual_rate:
                logger.debug(f"Rate {from_currency}/{to_currency} from manual rate")
                return manual_rate.rate

        except Exception as e:
            logger.warning(f"Manual rate lookup failed: {e}")

        return None

    def _fetch_from_providers(self, from_currency: str, to_currency: str) -> Optional[Decimal]:
        """
        Fetch rate from providers in priority order.
        Implements fallback chain.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            Exchange rate or None if all providers fail
        """
        providers = ExchangeRateProviderAccount.objects.filter(
            site=self.site,
            is_active=True
        ).order_by('priority')

        if not providers.exists():
            logger.error("No active exchange rate providers configured")
            return None

        for provider_account in providers:
            try:
                provider = provider_account.get_provider_instance()
                rate = provider.get_rate(from_currency, to_currency)

                if rate:
                    logger.info(f"Fetched rate {from_currency}/{to_currency}={rate} from {provider_account.name}")
                    return rate

            except Exception as e:
                logger.warning(f"Provider {provider_account.name} failed for {from_currency}/{to_currency}: {e}")
                continue

        logger.error(f"All providers failed for {from_currency}/{to_currency}")
        return None

    def _cache_rate_in_db(self, from_currency: str, to_currency: str, rate: Decimal):
        """
        Cache rate in database for future use.
        Respects the exchange rate selection strategy.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            rate: Exchange rate to cache
        """
        try:
            # Select provider account based on strategy
            if self.settings.exchange_rate_selection_strategy == 'primary':
                # Prefer primary provider for caching
                provider_account = ExchangeRateProviderAccount.objects.filter(
                    site=self.site,
                    is_active=True,
                    is_primary=True
                ).first()

                # Fallback to highest priority if no primary
                if not provider_account:
                    provider_account = ExchangeRateProviderAccount.objects.filter(
                        site=self.site,
                        is_active=True
                    ).order_by('priority').first()
            else:
                # 'latest' strategy - use highest priority provider
                provider_account = ExchangeRateProviderAccount.objects.filter(
                    site=self.site,
                    is_active=True
                ).order_by('priority').first()

            if not provider_account:
                logger.warning("No provider account available for caching rate")
                return

            ExchangeRate.objects.update_or_create(
                provider_account=provider_account,
                base_currency=from_currency,
                target_currency=to_currency,
                defaults={'rate': rate}
            )

            logger.debug(f"Cached rate {from_currency}/{to_currency}={rate} in database (provider: {provider_account.name})")

        except Exception as e:
            logger.error(f"Failed to cache rate in database: {e}")

    def update_all_rates(self, base_currency: str = None):
        """
        Update all exchange rates for supported currencies.
        Called by management command and Celery scheduled task.

        Args:
            base_currency: Base currency to use (defaults to site default_currency)

        Returns:
            Tuple of (success_count, failure_count)
        """
        if not base_currency:
            base_currency = self.settings.default_currency

        # Get supported currencies
        if self.settings.supported_currencies:
            target_currencies = self.settings.supported_currencies
        else:
            # If no specific currencies configured, use common currencies
            from core.utils.currency_helpers import get_common_currencies
            target_currencies = [code for code, _ in get_common_currencies()]

        # Remove base currency from targets
        target_currencies = [c for c in target_currencies if c != base_currency]

        success_count = 0
        failure_count = 0

        logger.info(f"Updating exchange rates for {len(target_currencies)} currencies from base {base_currency}")

        for target_currency in target_currencies:
            try:
                rate = self._fetch_from_providers(base_currency, target_currency)
                if rate:
                    self._cache_rate_in_db(base_currency, target_currency, rate)
                    success_count += 1
                else:
                    logger.warning(f"Failed to fetch rate for {base_currency}/{target_currency}")
                    failure_count += 1

            except Exception as e:
                logger.error(f"Error updating rate {base_currency}/{target_currency}: {e}")
                failure_count += 1

        logger.info(f"Rate update complete: {success_count} success, {failure_count} failed")
        return (success_count, failure_count)

    def snapshot_rate_for_order(self, from_currency: str, to_currency: str, order=None) -> ExchangeRateHistory:
        """
        Create historical snapshot of exchange rate for order auditing.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            order: Order instance (optional)

        Returns:
            ExchangeRateHistory instance
        """
        try:
            rate = self.get_rate(from_currency, to_currency)

            # Determine the rate source for audit trail
            manual_rate = self._get_manual_rate(from_currency, to_currency)
            if manual_rate is not None:
                provider_name = "Manual"
            else:
                provider_account = ExchangeRateProviderAccount.objects.filter(
                    site=self.site,
                    is_active=True
                ).order_by('priority').first()
                provider_name = provider_account.name if provider_account else "Unknown"

            snapshot = ExchangeRateHistory.objects.create(
                base_currency=from_currency,
                target_currency=to_currency,
                rate=rate,
                provider_name=provider_name,
                order=order
            )

            logger.info(f"Created rate snapshot for order: {from_currency}/{to_currency}={rate}")
            return snapshot

        except Exception as e:
            logger.error(f"Failed to create rate snapshot: {e}")
            raise

    def get_rate_info(self, from_currency: str, to_currency: str) -> dict:
        """
        Get detailed rate information including metadata.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            Dictionary with rate, source, timestamp, etc.
        """
        rate = self.get_rate(from_currency, to_currency)

        # Check if this is a manual rate
        manual_rate_obj = ManualExchangeRate.objects.filter(
            site=self.site,
            base_currency=from_currency,
            target_currency=to_currency,
            is_active=True
        ).first()

        if manual_rate_obj:
            return {
                'rate': rate,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'provider': 'Manual',
                'fetched_at': manual_rate_obj.updated_at,
                'is_stale': False,
                'source': 'manual',
                'markup_applied': self.settings.exchange_rate_markup_enabled,
                'markup_percentage': str(self.settings.exchange_rate_markup_percentage) if self.settings.exchange_rate_markup_enabled else None,
                'selection_strategy': self.settings.exchange_rate_selection_strategy,
            }

        # Get rate source using same strategy as get_rate()
        rate_query = ExchangeRate.objects.filter(
            base_currency=from_currency,
            target_currency=to_currency,
            provider_account__is_active=True
        )

        # Apply selection strategy
        if self.settings.exchange_rate_selection_strategy == 'primary':
            db_rate = rate_query.filter(
                provider_account__is_primary=True
            ).order_by('-fetched_at').first()

            # Fallback to latest if primary not available
            if not db_rate:
                db_rate = rate_query.order_by('-fetched_at').first()
        else:
            # 'latest' strategy
            db_rate = rate_query.order_by('-fetched_at').first()

        return {
            'rate': rate,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'provider': db_rate.provider_account.name if db_rate else None,
            'fetched_at': db_rate.fetched_at if db_rate else None,
            'is_stale': db_rate.is_stale if db_rate else True,
            'source': 'provider',
            'markup_applied': self.settings.exchange_rate_markup_enabled,
            'markup_percentage': str(self.settings.exchange_rate_markup_percentage) if self.settings.exchange_rate_markup_enabled else None,
            'selection_strategy': self.settings.exchange_rate_selection_strategy,
        }
