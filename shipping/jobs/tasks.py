"""
Celery tasks for asynchronous shipping operations

These tasks handle:
- Rate fetching from shipping providers
- Label generation and purchase
- Tracking updates (polling)
- Webhook processing

NOTE: Phase 11 creates the task skeleton. Actual provider API calls
will be implemented in a future phase when provider implementations are complete.
"""
import logging
from celery import shared_task
from django.utils import timezone
from decimal import Decimal

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name='shipping.fetch_rates',
    max_retries=3,
    default_retry_delay=60,  # 1 minute
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,  # 10 minutes max
    retry_jitter=True,
)
def fetch_rates(self, shipment_data, provider_account_ids=None):
    """
    Fetch shipping rates from one or more providers.

    Args:
        shipment_data (dict): Shipment details (origin, destination, weight, etc.)
        provider_account_ids (list, optional): List of provider account UUIDs to query.
                                               If None, queries all active providers.

    Returns:
        dict: {
            'success': bool,
            'rates': [
                {
                    'provider_account_id': 'uuid',
                    'carrier': 'USPS',
                    'service': 'Priority Mail',
                    'rate': '12.50',
                    'currency': 'USD',
                    'delivery_days': 3,
                    'delivery_date': '2025-10-23',
                },
                ...
            ],
            'errors': [
                {
                    'provider_account_id': 'uuid',
                    'error': 'Authentication failed'
                },
                ...
            ]
        }

    NOTE: This is a skeleton implementation. Actual provider API calls
    will be added when provider implementations are completed.
    """
    logger.info(
        f"Task fetch_rates started - shipment_data keys: {list(shipment_data.keys())}, "
        f"providers: {provider_account_ids or 'all active'}"
    )

    try:
        from shipping.models import ProviderAccount
        from shipping.services.rate_service import RateService

        # Get provider accounts to query
        if provider_account_ids:
            provider_accounts = ProviderAccount.objects.filter(
                id__in=provider_account_ids,
                is_active=True
            )
        else:
            # Query all active providers for the user
            provider_accounts = ProviderAccount.objects.filter(is_active=True)

        rates = []
        errors = []

        # Extract origin, destination, and parcels from shipment_data
        origin = shipment_data.get('origin', {})
        destination = shipment_data.get('destination', {})
        parcels = shipment_data.get('parcels', [])
        options = shipment_data.get('options', {})

        # Fetch rates from each provider
        for provider_account in provider_accounts:
            try:
                provider_rates = RateService.get_rates(
                    provider_account=provider_account,
                    origin=origin,
                    destination=destination,
                    parcels=parcels,
                    options=options
                )

                # Add provider_account_id to each rate
                for rate in provider_rates:
                    rate['provider_account_id'] = str(provider_account.id)
                    rates.append(rate)

            except Exception as exc:
                logger.error(
                    f"Failed to fetch rates from provider {provider_account.id}: {exc}",
                    exc_info=True
                )
                errors.append({
                    'provider_account_id': str(provider_account.id),
                    'error': str(exc)
                })

        result = {
            'success': len(errors) == 0 or len(rates) > 0,
            'rates': rates,
            'errors': errors,
            'fetched_at': timezone.now().isoformat(),
        }

        logger.info(f"Task fetch_rates completed - found {len(result['rates'])} rates")
        return result

    except Exception as exc:
        logger.error(
            f"Task fetch_rates failed - error: {str(exc)}, "
            f"retry attempt: {self.request.retries}",
            exc_info=True
        )
        # Re-raise to trigger retry
        raise


@shared_task(
    bind=True,
    name='shipping.buy_label',
    max_retries=3,
    default_retry_delay=30,  # 30 seconds
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,  # 5 minutes max
    retry_jitter=True,
)
def buy_label(self, shipment_id, rate_id=None, provider_account_id=None):
    """
    Purchase shipping label from provider.

    Args:
        shipment_id (str): UUID of Shipment model instance
        rate_id (str, optional): Provider's rate ID (from fetch_rates)
        provider_account_id (str, optional): Specific provider to use

    Returns:
        dict: {
            'success': bool,
            'shipment_id': 'uuid',
            'tracking_id': '1Z999AA10123456784',
            'label_url': 'https://provider.com/labels/xyz.pdf',
            'carrier': 'UPS',
            'service': 'Ground',
            'cost': '12.50',
            'currency': 'USD',
            'created_at': '2025-10-20T10:00:00Z',
            'error': 'Error message if failed'
        }

    This task will:
    1. Validate shipment exists and is in correct state
    2. Call provider API to purchase label
    3. Update Shipment model with tracking ID and label URL
    4. Update status to 'label_created'
    5. Create initial tracking event

    NOTE: This is a skeleton implementation. Actual provider API calls
    will be added when provider implementations are completed.
    """
    logger.info(
        f"Task buy_label started - shipment: {shipment_id}, "
        f"rate: {rate_id}, provider: {provider_account_id}"
    )

    try:
        from shipping.models import Shipment

        # Validate shipment exists
        try:
            shipment = Shipment.objects.select_related(
                'provider_account',
                'carrier_preset',
                'order'
            ).get(id=shipment_id)
        except Shipment.DoesNotExist:
            error_msg = f"Shipment {shipment_id} not found"
            logger.error(f"Task buy_label failed - {error_msg}")
            return {
                'success': False,
                'shipment_id': shipment_id,
                'error': error_msg
            }

        from shipping.services.label_service import LabelService

        # Validate shipment has provider account
        if not shipment.provider_account:
            error_msg = "Shipment must have a provider_account to purchase label"
            logger.error(f"Task buy_label failed - {error_msg}")
            return {
                'success': False,
                'shipment_id': str(shipment_id),
                'error': error_msg
            }

        # Build rate dictionary (simplified version)
        # In real usage, rate_id would be used to fetch the selected rate from cache/session
        # For now, we'll use a basic rate structure
        from core.utils import get_default_currency
        rate = {
            'service_code': 'fedex_ground',
            'service_name': 'FedEx Ground',
            'carrier': 'FedEx',
            'rate': Decimal('12.50'),
            'currency': get_default_currency(),
        }

        # Call LabelService to purchase label
        label_info = LabelService.buy_label(
            shipment=shipment,
            rate=rate,
            label_format='PDF',
            label_size='4x6'
        )

        result = {
            'success': True,
            'shipment_id': str(shipment_id),
            'tracking_id': label_info['tracking_number'],
            'label_url': label_info['label_url'],
            'carrier': label_info['carrier'],
            'service': label_info['service'],
            'cost': str(label_info['cost']),
            'currency': label_info['currency'],
            'created_at': timezone.now().isoformat()
        }

        logger.info(f"Task buy_label completed - shipment: {shipment_id}, tracking: {label_info['tracking_number']}")
        return result

    except Exception as exc:
        logger.error(
            f"Task buy_label failed - shipment: {shipment_id}, "
            f"error: {str(exc)}, retry attempt: {self.request.retries}",
            exc_info=True
        )
        raise


@shared_task(
    bind=True,
    name='shipping.poll_tracking',
    max_retries=3,
    default_retry_delay=120,  # 2 minutes
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,  # 10 minutes max
    retry_jitter=True,
)
def poll_tracking(self, shipment_id=None, batch_size=100):
    """
    Poll tracking updates from provider for one or more shipments.

    This task can be run:
    1. For a specific shipment (provide shipment_id)
    2. As a batch job for all active shipments (periodic celery beat task)

    Args:
        shipment_id (str, optional): Specific shipment UUID to poll
        batch_size (int): Number of shipments to poll if running batch

    Returns:
        dict: {
            'success': bool,
            'shipments_polled': int,
            'shipments_updated': int,
            'new_events': int,
            'errors': [...]
        }

    For each shipment:
    1. Check if tracking should be polled (not delivered, not canceled)
    2. Call provider API to get latest tracking
    3. Compare with existing tracking events
    4. Create new TrackingEvent records for new checkpoints
    5. Update shipment status if changed

    NOTE: This is a skeleton implementation. Actual provider API calls
    will be added when provider implementations are completed.
    """
    logger.info(
        f"Task poll_tracking started - "
        f"shipment: {shipment_id or 'batch'}, batch_size: {batch_size}"
    )

    try:
        from shipping.models import Shipment, TrackingEvent

        # Get shipments to poll
        if shipment_id:
            shipments = Shipment.objects.filter(
                id=shipment_id
            ).select_related('provider_account', 'carrier_preset')
        else:
            # Batch mode: poll active shipments
            shipments = Shipment.objects.filter(
                status__in=['label_created', 'in_transit', 'out_for_delivery'],
                provider_account__isnull=False  # Only poll API shipments
            ).select_related('provider_account', 'carrier_preset')[:batch_size]

        shipments_polled = 0
        shipments_updated = 0
        new_events = 0
        errors = []

        for shipment in shipments:
            shipments_polled += 1

            try:
                # TODO (Future Phase): Implement actual provider API calls
                # from shipping.services.tracking_service import TrackingService
                # tracking_service = TrackingService()
                # tracking_data = tracking_service.get_tracking(shipment)
                #
                # # Get existing event hashes to avoid duplicates
                # existing_events = set(
                #     TrackingEvent.objects.filter(shipment=shipment)
                #     .values_list('raw__event_hash', flat=True)
                # )
                #
                # # Create new events
                # for event_data in tracking_data['events']:
                #     event_hash = hash_event(event_data)
                #     if event_hash not in existing_events:
                #         TrackingEvent.objects.create(
                #             shipment=shipment,
                #             status=event_data['status'],
                #             description=event_data['description'],
                #             location=event_data['location'],
                #             occurred_at=event_data['timestamp'],
                #             raw={'event_hash': event_hash, **event_data}
                #         )
                #         new_events += 1
                #
                # # Update shipment status if changed
                # if tracking_data['status'] != shipment.status:
                #     shipment.status = tracking_data['status']
                #     shipment.save(update_fields=['status', 'updated_at'])
                #     shipments_updated += 1

                # Skeleton: just log
                logger.debug(f"Would poll tracking for shipment {shipment.id}")

            except Exception as exc:
                error_msg = f"Failed to poll shipment {shipment.id}: {str(exc)}"
                logger.error(error_msg, exc_info=True)
                errors.append({
                    'shipment_id': str(shipment.id),
                    'error': str(exc)
                })

        result = {
            'success': len(errors) == 0,
            'shipments_polled': shipments_polled,
            'shipments_updated': shipments_updated,
            'new_events': new_events,
            'errors': errors,
            'polled_at': timezone.now().isoformat()
        }

        logger.info(
            f"Task poll_tracking completed - "
            f"polled: {shipments_polled}, updated: {shipments_updated}, "
            f"new_events: {new_events}, errors: {len(errors)}"
        )

        return result

    except Exception as exc:
        logger.error(
            f"Task poll_tracking failed - error: {str(exc)}, "
            f"retry attempt: {self.request.retries}",
            exc_info=True
        )
        raise


@shared_task(
    bind=True,
    name='shipping.process_webhook',
    max_retries=5,
    default_retry_delay=30,  # 30 seconds
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,  # 10 minutes max
    retry_jitter=True,
)
def process_webhook(self, webhook_log_id):
    """
    Process webhook payload from shipping provider.

    This task is enqueued by the webhook receiver endpoint after
    logging the raw webhook data. Processing webhooks asynchronously
    ensures we return 200 OK quickly to the provider.

    Args:
        webhook_log_id (str): UUID of WebhookLog record

    Returns:
        dict: {
            'success': bool,
            'webhook_log_id': 'uuid',
            'shipment_id': 'uuid',
            'action': 'tracking_update|label_created|error',
            'events_created': int,
            'status_changed': bool,
            'error': 'Error message if failed'
        }

    Processing steps:
    1. Load WebhookLog record
    2. Identify provider from webhook_log.provider_key
    3. Call provider.parse_webhook(payload) to extract structured data
    4. Find related shipment(s)
    5. Process webhook action (tracking update, label created, etc.)
    6. Update WebhookLog with processing status

    NOTE: This is a skeleton implementation. Actual provider webhook parsing
    will be added when provider implementations are completed.
    """
    logger.info(f"Task process_webhook started - webhook_log: {webhook_log_id}")

    try:
        from shipping.models import WebhookLog

        # Load webhook log
        try:
            webhook_log = WebhookLog.objects.get(id=webhook_log_id)
        except WebhookLog.DoesNotExist:
            error_msg = f"WebhookLog {webhook_log_id} not found"
            logger.error(f"Task process_webhook failed - {error_msg}")
            return {
                'success': False,
                'webhook_log_id': webhook_log_id,
                'error': error_msg
            }

        # Mark as processing
        webhook_log.processing_status = 'processing'
        webhook_log.save(update_fields=['processing_status'])

        try:
            # TODO (Future Phase): Implement actual webhook processing
            # from shipping.services.webhook_service import WebhookService
            # webhook_service = WebhookService()
            #
            # # Parse webhook with provider-specific logic
            # parsed_data = webhook_service.parse_webhook(webhook_log)
            #
            # # Process based on webhook type
            # if parsed_data['type'] == 'tracking_update':
            #     result = webhook_service.process_tracking_update(parsed_data)
            # elif parsed_data['type'] == 'label_created':
            #     result = webhook_service.process_label_created(parsed_data)
            # elif parsed_data['type'] == 'error':
            #     result = webhook_service.process_error(parsed_data)
            # else:
            #     raise ValueError(f"Unknown webhook type: {parsed_data['type']}")
            #
            # # Mark as processed
            # webhook_log.status = 'processed'
            # webhook_log.processed_at = timezone.now()
            # webhook_log.save()

            # Skeleton response
            result = {
                'success': False,
                'webhook_log_id': str(webhook_log_id),
                'error': 'Webhook processing not yet implemented (Phase 11 skeleton)',
                'message': 'Webhook processing will be implemented in future phase'
            }

            # Mark as pending (not implemented)
            webhook_log.processing_status = 'pending'
            webhook_log.save(update_fields=['processing_status'])

            logger.info(
                f"Task process_webhook completed - "
                f"webhook_log: {webhook_log_id}"
            )

            return result

        except Exception as exc:
            # Mark as failed
            webhook_log.processing_status = 'failed'
            webhook_log.error_message = str(exc)
            webhook_log.save(update_fields=['processing_status', 'error_message'])
            raise

    except Exception as exc:
        logger.error(
            f"Task process_webhook failed - webhook_log: {webhook_log_id}, "
            f"error: {str(exc)}, retry attempt: {self.request.retries}",
            exc_info=True
        )
        raise


# Utility function for webhook signature verification
def verify_webhook_signature(payload, signature, secret):
    """
    Verify webhook signature (HMAC-SHA256).

    This is used by the webhook receiver endpoint before queuing
    the process_webhook task.

    Args:
        payload (bytes): Raw webhook payload
        signature (str): Signature from webhook header
        secret (str): Provider webhook secret

    Returns:
        bool: True if signature is valid

    NOTE: Actual implementation should use provider-specific logic
    from provider.verify_webhook_signature()
    """
    import hmac
    import hashlib

    # TODO (Future Phase): Use provider-specific verification
    # provider = get_provider_by_key(provider_key)
    # return provider.verify_webhook_signature(payload, signature, secret)

    # Generic HMAC-SHA256 verification
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)
