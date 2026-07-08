"""
Celery tasks for product feed generation and synchronization.

Scheduled tasks:
- sync_all_feeds: Sync all active feed provider accounts
- sync_feed: Sync a specific feed provider account
- cleanup_expired_feeds: Remove old cached feeds
"""

from celery import shared_task
from django.contrib.sites.models import Site
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_all_feeds(self, site_id=None, force=False):
    """
    Sync all active feed provider accounts.

    This task runs on a schedule to regenerate feeds and push to providers.

    Args:
        site_id: Site ID to sync feeds for (None = site 1)
        force: Force sync even if not due yet

    Returns:
        Dict with sync statistics
    """
    from product_feeds.models import FeedProviderAccount, FeedSyncLog

    try:
        # Platform is single-tenant, always use Site ID=1
        if site_id:
            site = Site.objects.get(pk=site_id)
        else:
            site = Site.objects.get(pk=1)

        # Get accounts that need syncing
        now = timezone.now()

        accounts = FeedProviderAccount.objects.filter(
            site=site,
            is_active=True
        )

        if not force:
            # Only sync accounts that are due
            accounts = accounts.filter(
                next_sync_at__lte=now
            ) | accounts.filter(next_sync_at__isnull=True)

        total_success = 0
        total_failed = 0
        accounts_processed = 0

        for account in accounts:
            try:
                # Trigger individual sync task
                result = sync_feed.delay(account.id)
                accounts_processed += 1

                logger.info(f"Triggered sync for feed account: {account.name}")

            except Exception as e:
                total_failed += 1
                logger.error(f"Failed to trigger sync for {account.name}: {e}")

        result = {
            'success': True,
            'accounts_processed': accounts_processed,
            'message': f'Triggered sync for {accounts_processed} feed account(s)',
        }

        logger.info(f"Feed sync batch complete: {result}")
        return result

    except Exception as exc:
        logger.error(f"Feed sync batch task failed: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_feed(self, account_id, full_sync=False):
    """
    Sync a specific feed provider account.

    Generates the feed and optionally pushes to the provider API.

    Args:
        account_id: FeedProviderAccount ID
        full_sync: Force full catalog sync (vs incremental)

    Returns:
        Dict with sync result
    """
    from product_feeds.models import FeedProviderAccount, FeedSyncLog
    from product_feeds.services import FeedService

    sync_log = None

    try:
        account = FeedProviderAccount.objects.select_related('component').get(pk=account_id)

        # Create sync log
        sync_log = FeedSyncLog.objects.create(
            account=account,
            status='running',
            sync_type='full' if full_sync else 'scheduled',
        )

        # Update account status
        account.sync_status = 'syncing'
        account.save(update_fields=['sync_status', 'updated_at'])

        logger.info(f"Starting feed sync for: {account.name}")

        # Initialize feed service
        service = FeedService(account)

        # Determine feed format from config
        feed_format = account.config.get('feed_format', 'xml')

        # Generate feed
        feed_content = service.generate_feed(
            format=feed_format,
            save_to_db=True
        )

        # Get the saved feed
        feed = service.get_latest_feed(format=feed_format)

        # Try to push to provider if supported
        push_result = {'success': True}
        try:
            provider = account.get_provider_instance()
            if provider and provider.capabilities.get('push_feed', False):
                push_result = provider.push_feed(feed_content, feed_format)
        except Exception as push_error:
            logger.warning(f"Feed push failed for {account.name}: {push_error}")
            push_result = {'success': False, 'error': str(push_error)}

        # Update sync log
        completed_at = timezone.now()
        duration = int((completed_at - sync_log.started_at).total_seconds())

        sync_log.status = 'success' if push_result.get('success', True) else 'partial'
        sync_log.completed_at = completed_at
        sync_log.duration_seconds = duration
        sync_log.products_synced = feed.product_count if feed else 0
        sync_log.feed = feed
        sync_log.save()

        # Update account
        account.sync_status = 'success'
        account.last_sync_at = completed_at
        account.next_sync_at = _calculate_next_sync(account)
        account.sync_error_message = ''
        account.products_in_feed = feed.product_count if feed else 0
        account.save(update_fields=[
            'sync_status', 'last_sync_at', 'next_sync_at',
            'sync_error_message', 'products_in_feed', 'updated_at'
        ])

        result = {
            'success': True,
            'account_id': account_id,
            'account_name': account.name,
            'products_synced': feed.product_count if feed else 0,
            'duration_seconds': duration,
            'push_result': push_result,
        }

        logger.info(f"Feed sync complete for {account.name}: {result}")
        return result

    except FeedProviderAccount.DoesNotExist:
        logger.error(f"Feed account not found: {account_id}")
        return {
            'success': False,
            'error': f'Account {account_id} not found',
        }

    except Exception as exc:
        error_msg = str(exc)
        logger.error(f"Feed sync failed for account {account_id}: {error_msg}")

        # Update sync log if exists
        if sync_log:
            sync_log.status = 'failed'
            sync_log.completed_at = timezone.now()
            sync_log.error_message = error_msg
            sync_log.save()

        # Update account status
        try:
            account = FeedProviderAccount.objects.get(pk=account_id)
            account.sync_status = 'error'
            account.sync_error_message = error_msg
            account.last_error_at = timezone.now()
            account.save(update_fields=[
                'sync_status', 'sync_error_message', 'last_error_at', 'updated_at'
            ])
        except Exception:
            pass

        # Retry task with exponential backoff
        raise self.retry(exc=exc)


@shared_task
def cleanup_expired_feeds(days_old=7):
    """
    Clean up expired feed cache entries.

    Removes ProductFeed records that have expired.

    Args:
        days_old: Also remove unexpired feeds older than this many days

    Returns:
        Number of deleted records
    """
    from product_feeds.models import ProductFeed
    import os

    now = timezone.now()
    cutoff_date = now - timedelta(days=days_old)

    # Find feeds to delete
    feeds_to_delete = ProductFeed.objects.filter(
        expires_at__lt=now
    ) | ProductFeed.objects.filter(
        generated_at__lt=cutoff_date
    )

    # Delete associated files
    for feed in feeds_to_delete:
        if feed.file_path and os.path.exists(feed.file_path):
            try:
                os.remove(feed.file_path)
                logger.debug(f"Deleted feed file: {feed.file_path}")
            except Exception as e:
                logger.warning(f"Could not delete feed file {feed.file_path}: {e}")

    # Delete database records
    deleted_count, _ = feeds_to_delete.delete()

    logger.info(f"Cleaned up {deleted_count} expired feed records")

    return deleted_count


@shared_task
def validate_provider_credentials(account_id):
    """
    Validate feed provider credentials.

    Used when setting up a new provider account.

    Args:
        account_id: FeedProviderAccount ID

    Returns:
        Dict with validation result
    """
    from product_feeds.models import FeedProviderAccount

    try:
        account = FeedProviderAccount.objects.get(pk=account_id)
        provider = account.get_provider_instance()

        if not provider:
            return {
                'success': False,
                'message': 'Could not load provider implementation',
                'account_name': account.name,
            }

        result = provider.test_connection()

        if result.get('success'):
            logger.info(f"Provider credentials validated: {account.name}")
        else:
            logger.warning(f"Provider credential validation failed: {account.name} - {result.get('message')}")

        return {
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'details': result.get('details', {}),
            'account_name': account.name,
        }

    except FeedProviderAccount.DoesNotExist:
        logger.error(f"Account not found: {account_id}")
        return {
            'success': False,
            'message': f'Account {account_id} not found',
            'account_name': None,
        }

    except Exception as e:
        logger.error(f"Credential validation task failed: {e}")
        return {
            'success': False,
            'message': str(e),
            'account_name': None,
        }


@shared_task
def generate_feed_preview(account_id, format='xml', limit=10):
    """
    Generate a small preview of the feed for testing.

    Args:
        account_id: FeedProviderAccount ID
        format: Feed format
        limit: Max products to include

    Returns:
        Dict with preview content
    """
    from product_feeds.models import FeedProviderAccount
    from product_feeds.services import FeedService
    from catalog.models import Product

    try:
        account = FeedProviderAccount.objects.get(pk=account_id)
        service = FeedService(account)

        # Get first N product IDs
        product_ids = list(
            Product.objects.filter(is_active=True, status='published')
            .values_list('id', flat=True)[:limit]
        )

        # Generate preview (don't save to DB)
        feed_content = service.generate_feed(
            format=format,
            product_ids=product_ids,
            save_to_db=False
        )

        return {
            'success': True,
            'content': feed_content[:10000],  # Limit preview size
            'product_count': len(product_ids),
            'format': format,
            'truncated': len(feed_content) > 10000,
        }

    except FeedProviderAccount.DoesNotExist:
        return {
            'success': False,
            'error': f'Account {account_id} not found',
        }

    except Exception as e:
        logger.error(f"Feed preview generation failed: {e}")
        return {
            'success': False,
            'error': str(e),
        }


def _calculate_next_sync(account):
    """
    Calculate next sync time based on account config.

    Args:
        account: FeedProviderAccount instance

    Returns:
        datetime for next sync
    """
    sync_interval = account.config.get('sync_interval', 'daily')
    now = timezone.now()

    intervals = {
        'hourly': timedelta(hours=1),
        'daily': timedelta(days=1),
        'weekly': timedelta(weeks=1),
        'manual': None,
    }

    delta = intervals.get(sync_interval)

    if delta:
        return now + delta
    return None  # Manual sync, no auto-schedule
