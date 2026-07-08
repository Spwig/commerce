"""
Celery tasks for exchange rate updates.

Scheduled tasks:
- update_exchange_rates: Periodic rate updates (interval-configurable)
"""

from celery import shared_task
from datetime import timedelta
from django.contrib.sites.models import Site
from django.utils import timezone
from exchange_rates.services.exchange_service import ExchangeRateService
from exchange_rates.models import ExchangeRateProviderAccount
from core.models import SiteSettings
import logging

logger = logging.getLogger(__name__)


def _get_interval_delta(interval):
    """Return timedelta for a sync interval setting, or None for manual_only."""
    INTERVAL_DELTAS = {
        'realtime': timedelta(minutes=15),
        'hourly': timedelta(hours=1),
        'daily': timedelta(hours=24),
        'weekly': timedelta(weeks=1),
        'monthly': timedelta(days=30),
        'quarterly': timedelta(days=90),
        'manual_only': None,
    }
    return INTERVAL_DELTAS.get(interval)


@shared_task(bind=True, max_retries=3, ignore_result=True)
def update_exchange_rates(self, site_id=None, base_currency=None, force=False):
    """
    Update all exchange rates for configured currencies.

    Called by Celery Beat every 15 minutes. The task checks whether the
    configured sync interval has elapsed before actually fetching rates.

    Args:
        site_id: Site ID to update rates for (None = site 1)
        base_currency: Base currency (None = use site default)
        force: If True, bypass interval check (for manual "sync now")

    Returns:
        Dict with update statistics
    """
    try:
        sites = [Site.objects.get(pk=site_id or 1)]

        total_success = 0
        total_failure = 0

        for site in sites:
            # Check for active providers first (cheapest short-circuit for fresh installs)
            active_providers = ExchangeRateProviderAccount.objects.filter(
                site=site,
                is_active=True
            ).count()

            if active_providers == 0:
                logger.debug(f"No active exchange rate providers for site {site.name}, skipping")
                continue

            settings = SiteSettings.get_settings()

            # Skip if multi-currency not enabled
            if not settings.enable_multi_currency:
                logger.debug(f"Multi-currency not enabled for site {site.name}, skipping")
                continue

            # Check sync interval unless forced
            sync_interval = getattr(settings, 'exchange_rate_sync_interval', 'daily')

            if sync_interval == 'manual_only' and not force:
                logger.debug("Sync interval is manual_only, skipping auto-sync")
                continue

            if not force:
                # Check if enough time has passed since last provider sync
                last_sync = ExchangeRateProviderAccount.objects.filter(
                    site=site, is_active=True, last_sync_at__isnull=False
                ).order_by('-last_sync_at').values_list('last_sync_at', flat=True).first()

                if last_sync:
                    elapsed = timezone.now() - last_sync
                    required_delta = _get_interval_delta(sync_interval)
                    if required_delta and elapsed < required_delta:
                        logger.debug(
                            f"Skipping sync: {elapsed} elapsed < {required_delta} required ({sync_interval})"
                        )
                        continue

            # Update rates
            service = ExchangeRateService(site=site)
            success_count, failure_count = service.update_all_rates(base_currency=base_currency)

            total_success += success_count
            total_failure += failure_count

            # Update last_sync_at on active providers
            ExchangeRateProviderAccount.objects.filter(
                site=site, is_active=True
            ).update(last_sync_at=timezone.now(), sync_status='success')

            logger.info(f"Updated rates for {site.name}: {success_count} success, {failure_count} failed")

        result = {
            'success': total_success,
            'failed': total_failure,
            'sites_processed': len(sites),
        }

        if total_success > 0 or total_failure > 0:
            logger.info(f"Exchange rate update complete: {result}")
        else:
            logger.debug(f"Exchange rate update complete: {result}")
        return result

    except Exception as exc:
        logger.error(f"Exchange rate update task failed: {exc}")
        # Retry task with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def cleanup_stale_rates(days_old=7):
    """
    Clean up stale exchange rate cache entries.

    Removes ExchangeRate records older than specified days.

    Args:
        days_old: Remove rates older than this many days

    Returns:
        Number of deleted records
    """
    from exchange_rates.models import ExchangeRate

    cutoff_date = timezone.now() - timedelta(days=days_old)

    deleted_count, _ = ExchangeRate.objects.filter(
        fetched_at__lt=cutoff_date
    ).delete()

    logger.info(f"Cleaned up {deleted_count} stale exchange rate records older than {days_old} days")

    return deleted_count


@shared_task
def validate_provider_credentials(provider_account_id):
    """
    Validate exchange rate provider credentials.

    Used when setting up a new provider account.

    Args:
        provider_account_id: ExchangeRateProviderAccount ID

    Returns:
        Dict with validation result
    """
    try:
        provider_account = ExchangeRateProviderAccount.objects.get(pk=provider_account_id)
        provider = provider_account.get_provider_instance()

        test_result = provider.test_connection()
        success = test_result.get('success', False)
        message = test_result.get('message', '')

        result = {
            'success': success,
            'message': message,
            'provider_name': provider_account.name,
        }

        if success:
            logger.info("Provider credentials validated: %s", provider_account.name)
        else:
            logger.warning("Provider credential validation failed: %s - %s", provider_account.name, message)

        return result

    except Exception as e:
        logger.error("Credential validation task failed: %s", e)
        return {
            'success': False,
            'message': str(e),
            'provider_name': None,
        }
