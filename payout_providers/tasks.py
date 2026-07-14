"""
Payout Provider Celery Tasks

Background tasks for processing affiliate payouts through external providers
(PayPal Payouts, Airwallex Transfers, etc.)
"""

import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from core.utils import get_default_currency

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="payout_providers.process_payout",
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=1800,  # 30 minutes
    retry_jitter=True,
)
def process_payout(self, payout_id: int, provider_account_id: int = None):
    """
    Process a single payout through the appropriate provider.

    This task:
    1. Loads the payout and determines the appropriate provider
    2. Creates a PayoutRequest from the payout data
    3. Calls the provider's create_payout method
    4. Updates the payout with the result

    Args:
        payout_id: ID of the Payout to process
        provider_account_id: Optional specific provider account to use

    Returns:
        dict: Processing result with status and details
    """
    from affiliate.models import Payout

    from .loader import get_provider_class
    from .models import PayoutProviderAccount
    from .providers.base import PayoutMethod, PayoutRecipient, PayoutRequest

    logger.info(f"Processing payout {payout_id}")

    try:
        payout = Payout.objects.select_related("affiliate").get(id=payout_id)
    except Payout.DoesNotExist:
        logger.error(f"Payout {payout_id} not found")
        return {"success": False, "error": "Payout not found", "payout_id": payout_id}

    # Check if already processed
    if payout.status in ("completed", "processing"):
        logger.warning(f"Payout {payout_id} already {payout.status}, skipping")
        return {
            "success": False,
            "error": f"Payout already {payout.status}",
            "payout_id": payout_id,
        }

    affiliate = payout.affiliate

    # Determine provider account
    if provider_account_id:
        try:
            provider_account = PayoutProviderAccount.objects.get(
                id=provider_account_id, is_active=True
            )
        except PayoutProviderAccount.DoesNotExist:
            logger.error(f"Provider account {provider_account_id} not found or inactive")
            return {"success": False, "error": "Provider account not found", "payout_id": payout_id}
    else:
        # Auto-select based on affiliate's payment method
        provider_account = _get_provider_for_affiliate(affiliate)

    if not provider_account:
        error_msg = f"No active provider found for payment method: {affiliate.payment_method}"
        logger.error(error_msg)
        payout.mark_as_failed(notes=error_msg)
        return {"success": False, "error": error_msg, "payout_id": payout_id}

    # Get provider class and instantiate
    provider_class = get_provider_class(provider_account.provider_type, provider_account.component)

    if not provider_class:
        error_msg = f"Provider class not found for type: {provider_account.provider_type}"
        logger.error(error_msg)
        payout.mark_as_failed(notes=error_msg)
        return {"success": False, "error": error_msg, "payout_id": payout_id}

    # Instantiate provider with credentials
    config = provider_account.credentials
    config.update(provider_account.settings)
    provider = provider_class(config)

    # Build recipient info
    recipient = PayoutRecipient(
        name=affiliate.company_name or str(affiliate.user),
        email=affiliate.paypal_email or affiliate.user.email,
        account_number=affiliate.bank_account_number,
        routing_number=affiliate.bank_routing_code,
        swift_code=affiliate.bank_swift_code,
        country=affiliate.bank_country or affiliate.country,
        bank_name=None,  # Not stored in current model
        account_holder_name=affiliate.bank_account_holder,
    )

    # Determine payout method
    if affiliate.payment_method == "paypal":
        payout_method = PayoutMethod.PAYPAL
    else:
        payout_method = PayoutMethod.BANK_TRANSFER

    # Create payout request
    payout_request = PayoutRequest(
        payout_id=payout.id,
        recipient=recipient,
        amount=payout.amount,
        currency=payout.currency or get_default_currency(),
        reference=f"SPWIG-PAYOUT-{payout.id}",
        method=payout_method,
        note=f"Commission payout for {affiliate.company_name or affiliate.user.email}",
        metadata={
            "affiliate_id": affiliate.id,
            "payout_id": payout.id,
        },
    )

    try:
        # Mark as processing before API call
        payout.mark_as_processing(provider_account=provider_account)

        # Call provider
        result = provider.create_payout(payout_request)

        if result.success:
            # Update payout with provider response
            payout.provider_reference = result.provider_reference or ""
            payout.provider_response = result.raw_response or {}

            # If immediately completed (rare), mark complete
            if result.status.value == "completed":
                payout.mark_as_completed(
                    provider_reference=result.provider_reference,
                    provider_response=result.raw_response,
                )
                logger.info(f"Payout {payout_id} completed immediately")
            else:
                # Still processing - save the reference for webhook updates
                payout.save()
                logger.info(
                    f"Payout {payout_id} submitted, awaiting confirmation. Ref: {result.provider_reference}"
                )

            return {
                "success": True,
                "payout_id": payout_id,
                "provider_reference": result.provider_reference,
                "status": result.status.value,
                "message": result.message,
            }
        else:
            # Provider returned failure
            payout.mark_as_failed(
                notes=result.message or "Provider returned failure",
                provider_response=result.raw_response,
            )
            logger.error(f"Payout {payout_id} failed: {result.message}")

            return {
                "success": False,
                "payout_id": payout_id,
                "error": result.message,
                "raw_response": result.raw_response,
            }

    except Exception as e:
        logger.error(f"Error processing payout {payout_id}: {e}", exc_info=True)

        # Mark as failed
        payout.mark_as_failed(notes=str(e))

        # Retry if not max retries
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        return {"success": False, "payout_id": payout_id, "error": str(e)}


@shared_task(
    bind=True,
    name="payout_providers.process_batch_payouts",
    max_retries=2,
    default_retry_delay=600,  # 10 minutes
)
def process_batch_payouts(self, payout_ids: list, provider_account_id: int):
    """
    Process multiple payouts as a batch (optimized for PayPal).

    PayPal supports up to 15,000 payments per batch, making this much more
    efficient than individual API calls.

    Args:
        payout_ids: List of Payout IDs to process
        provider_account_id: Provider account to use for the batch

    Returns:
        dict: Batch processing result
    """
    from affiliate.models import Payout

    from .loader import get_provider_class
    from .models import PayoutProviderAccount
    from .providers.base import PayoutMethod, PayoutRecipient, PayoutRequest

    logger.info(
        f"Processing batch of {len(payout_ids)} payouts with provider {provider_account_id}"
    )

    if not payout_ids:
        return {"success": False, "error": "No payout IDs provided"}

    try:
        provider_account = PayoutProviderAccount.objects.get(id=provider_account_id, is_active=True)
    except PayoutProviderAccount.DoesNotExist:
        logger.error(f"Provider account {provider_account_id} not found or inactive")
        return {"success": False, "error": "Provider account not found"}

    # Get provider class
    provider_class = get_provider_class(provider_account.provider_type, provider_account.component)

    if not provider_class:
        return {
            "success": False,
            "error": f"Provider class not found: {provider_account.provider_type}",
        }

    # Instantiate provider
    config = provider_account.credentials
    config.update(provider_account.settings)
    provider = provider_class(config)

    # Check if provider supports batch
    if not hasattr(provider, "create_batch_payout"):
        # Fall back to individual processing
        logger.info(
            f"Provider {provider_account.provider_type} doesn't support batch, processing individually"
        )
        results = []
        for payout_id in payout_ids:
            result = process_payout.delay(payout_id, provider_account_id)
            results.append({"payout_id": payout_id, "task_id": str(result.id)})
        return {"success": True, "message": "Queued for individual processing", "tasks": results}

    # Load payouts
    payouts = Payout.objects.filter(id__in=payout_ids, status="pending").select_related("affiliate")

    if not payouts.exists():
        return {"success": False, "error": "No pending payouts found"}

    # Build payout requests
    payout_requests = []
    payout_map = {}  # Map reference to payout for later update

    for payout in payouts:
        affiliate = payout.affiliate

        recipient = PayoutRecipient(
            name=affiliate.company_name or str(affiliate.user),
            email=affiliate.paypal_email or affiliate.user.email,
            account_number=affiliate.bank_account_number,
            routing_number=affiliate.bank_routing_code,
            swift_code=affiliate.bank_swift_code,
            country=affiliate.bank_country or affiliate.country,
            account_holder_name=affiliate.bank_account_holder,
        )

        reference = f"SPWIG-PAYOUT-{payout.id}"

        payout_request = PayoutRequest(
            payout_id=payout.id,
            recipient=recipient,
            amount=payout.amount,
            currency=payout.currency or get_default_currency(),
            reference=reference,
            method=PayoutMethod.PAYPAL
            if affiliate.payment_method == "paypal"
            else PayoutMethod.BANK_TRANSFER,
            note=f"Commission payout for {affiliate.company_name or affiliate.user.email}",
            metadata={"affiliate_id": affiliate.id, "payout_id": payout.id},
        )

        payout_requests.append(payout_request)
        payout_map[reference] = payout

    try:
        # Mark all as processing
        with transaction.atomic():
            Payout.objects.filter(id__in=payout_ids).update(
                status="processing", processed_at=timezone.now(), provider_account=provider_account
            )

        # Call batch payout
        batch_result = provider.create_batch_payout(payout_requests)

        if batch_result.success:
            # Update payouts with batch reference
            Payout.objects.filter(id__in=payout_ids).update(
                provider_reference=batch_result.batch_reference or "",
                provider_response=batch_result.raw_response or {},
            )

            logger.info(f"Batch payout submitted. Ref: {batch_result.batch_reference}")

            return {
                "success": True,
                "batch_reference": batch_result.batch_reference,
                "message": batch_result.message,
                "count": len(payout_ids),
            }
        else:
            # Batch failed - mark all as failed
            Payout.objects.filter(id__in=payout_ids).update(
                status="failed",
                notes=batch_result.message or "Batch submission failed",
                provider_response=batch_result.raw_response or {},
            )

            logger.error(f"Batch payout failed: {batch_result.message}")

            return {"success": False, "error": batch_result.message, "count": len(payout_ids)}

    except Exception as e:
        logger.error(f"Error processing batch payout: {e}", exc_info=True)

        # Mark all as failed
        Payout.objects.filter(id__in=payout_ids).update(status="failed", notes=str(e))

        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        return {"success": False, "error": str(e)}


@shared_task(
    bind=True,
    name="payout_providers.sync_payout_status",
    max_retries=3,
    default_retry_delay=60,
)
def sync_payout_status(self, payout_id: int):
    """
    Sync payout status from the provider API.

    Use this as a fallback when webhooks fail or to verify final status.

    Args:
        payout_id: ID of the Payout to sync

    Returns:
        dict: Sync result with updated status
    """
    from affiliate.models import Payout

    from .loader import get_provider_class

    logger.info(f"Syncing status for payout {payout_id}")

    try:
        payout = Payout.objects.select_related("provider_account").get(id=payout_id)
    except Payout.DoesNotExist:
        return {"success": False, "error": "Payout not found"}

    if not payout.provider_account:
        return {"success": False, "error": "No provider account associated"}

    if not payout.provider_reference:
        return {"success": False, "error": "No provider reference to sync"}

    provider_account = payout.provider_account

    # Get provider
    provider_class = get_provider_class(provider_account.provider_type, provider_account.component)

    if not provider_class:
        return {"success": False, "error": "Provider class not found"}

    config = provider_account.credentials
    config.update(provider_account.settings)
    provider = provider_class(config)

    try:
        result = provider.get_payout_status(payout.provider_reference)

        if result.success:
            old_status = payout.status
            new_status = _map_provider_status(result.status)

            # Update payout status
            if new_status == "completed" and payout.status != "completed":
                payout.mark_as_completed(
                    provider_reference=payout.provider_reference,
                    provider_response=result.raw_response,
                )
                logger.info(f"Payout {payout_id} marked as completed")

            elif new_status == "failed" and payout.status not in ("completed", "failed"):
                payout.mark_as_failed(
                    notes=result.message or "Provider reported failure",
                    provider_response=result.raw_response,
                )
                logger.warning(f"Payout {payout_id} marked as failed: {result.message}")

            elif new_status in ("returned", "cancelled") and payout.status not in (
                "completed",
                "failed",
                "cancelled",
            ):
                payout.status = "cancelled"
                payout.notes = result.message or f"Provider status: {result.status.value}"
                payout.provider_response = result.raw_response or {}
                payout.save()
                logger.warning(f"Payout {payout_id} marked as cancelled")

            else:
                # Just update the response data
                payout.provider_response = result.raw_response or {}
                payout.save()

            return {
                "success": True,
                "payout_id": payout_id,
                "old_status": old_status,
                "new_status": payout.status,
                "provider_status": result.status.value,
            }
        else:
            logger.error(f"Failed to get status for payout {payout_id}: {result.message}")
            return {"success": False, "payout_id": payout_id, "error": result.message}

    except Exception as e:
        logger.error(f"Error syncing payout {payout_id}: {e}", exc_info=True)

        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        return {"success": False, "payout_id": payout_id, "error": str(e)}


@shared_task(name="payout_providers.sync_pending_payout_statuses")
def sync_pending_payout_statuses():
    """
    Periodic task to sync statuses for all processing payouts.

    This acts as a fallback for webhook delivery failures.
    Runs every hour via Celery Beat.

    Returns:
        dict: Summary of synced payouts
    """
    from datetime import timedelta

    from affiliate.models import Payout

    logger.info("Starting periodic payout status sync")

    # Find payouts that have been processing for more than 5 minutes
    # (gives webhooks time to arrive first)
    cutoff_time = timezone.now() - timedelta(minutes=5)

    processing_payouts = (
        Payout.objects.filter(
            status="processing", provider_reference__isnull=False, processed_at__lt=cutoff_time
        )
        .exclude(provider_reference="")
        .values_list("id", flat=True)[:100]
    )  # Process 100 at a time

    synced = 0
    failed = 0

    for payout_id in processing_payouts:
        try:
            sync_payout_status.delay(payout_id)
            synced += 1
        except Exception as e:
            logger.error(f"Failed to queue sync for payout {payout_id}: {e}")
            failed += 1

    logger.info(f"Queued {synced} payouts for status sync, {failed} failed to queue")

    return {"queued": synced, "failed": failed, "total_processing": len(processing_payouts)}


@shared_task(name="payout_providers.handle_webhook_event")
def handle_webhook_event(webhook_log_id: int):
    """
    Process a webhook event from a payout provider.

    This task is called after a webhook is received and logged.
    It handles updating payout statuses based on provider events.

    Args:
        webhook_log_id: ID of the PayoutWebhookLog entry

    Returns:
        dict: Processing result
    """
    from affiliate.models import Payout

    from .loader import get_provider_class
    from .models import PayoutWebhookLog

    logger.info(f"Processing webhook event {webhook_log_id}")

    try:
        webhook_log = PayoutWebhookLog.objects.select_related("provider_account").get(
            id=webhook_log_id
        )
    except PayoutWebhookLog.DoesNotExist:
        return {"success": False, "error": "Webhook log not found"}

    if webhook_log.processed:
        return {"success": True, "message": "Already processed"}

    provider_account = webhook_log.provider_account

    # Get provider to parse webhook
    provider_class = get_provider_class(
        webhook_log.provider_type, provider_account.component if provider_account else None
    )

    if not provider_class:
        webhook_log.processing_error = "Provider class not found"
        webhook_log.save()
        return {"success": False, "error": "Provider class not found"}

    # Instantiate provider
    config = provider_account.credentials if provider_account else {}
    if provider_account:
        config.update(provider_account.settings)
    provider = provider_class(config)

    try:
        # Parse webhook event
        event_data = provider.handle_webhook(webhook_log.payload)

        payout_reference = event_data.get("payout_reference")
        provider_status = event_data.get("status")

        if not payout_reference:
            webhook_log.processed = True
            webhook_log.processed_at = timezone.now()
            webhook_log.save()
            return {"success": True, "message": "No payout reference in event"}

        # Find matching payout
        payout = Payout.objects.filter(provider_reference=payout_reference).first()

        if not payout:
            webhook_log.processed = True
            webhook_log.processed_at = timezone.now()
            webhook_log.save()
            logger.warning(f"No payout found for reference: {payout_reference}")
            return {
                "success": True,
                "message": f"No payout found for reference: {payout_reference}",
            }

        # Update payout status
        new_status = _map_provider_status(provider_status)

        if new_status == "completed" and payout.status != "completed":
            payout.mark_as_completed(
                provider_reference=payout_reference,
                provider_response=event_data.get("raw_data", {}),
            )
            logger.info(f"Payout {payout.id} marked completed via webhook")

        elif new_status == "failed" and payout.status not in ("completed", "failed"):
            payout.mark_as_failed(
                notes=event_data.get("message", "Failed via webhook"),
                provider_response=event_data.get("raw_data", {}),
            )
            logger.warning(f"Payout {payout.id} marked failed via webhook")

        elif new_status in ("returned", "cancelled"):
            payout.status = "cancelled"
            payout.notes = event_data.get("message", f"Status: {provider_status}")
            payout.provider_response = event_data.get("raw_data", {})
            payout.save()
            logger.warning(f"Payout {payout.id} marked cancelled via webhook")

        # Mark webhook as processed
        webhook_log.payout_reference = payout_reference
        webhook_log.processed = True
        webhook_log.processed_at = timezone.now()
        webhook_log.save()

        return {
            "success": True,
            "payout_id": payout.id,
            "new_status": payout.status,
            "event_type": event_data.get("event_type"),
        }

    except Exception as e:
        logger.error(f"Error processing webhook {webhook_log_id}: {e}", exc_info=True)
        webhook_log.processing_error = str(e)
        webhook_log.save()
        return {"success": False, "error": str(e)}


def _get_provider_for_affiliate(affiliate):
    """
    Get the appropriate provider account for an affiliate based on their payment method.

    Args:
        affiliate: Affiliate model instance

    Returns:
        PayoutProviderAccount or None
    """
    from .models import PayoutProviderAccount

    # Check for preferred provider first
    if affiliate.preferred_payout_provider and affiliate.preferred_payout_provider.is_active:
        return affiliate.preferred_payout_provider

    # Map payment method to provider type
    method_to_provider = {
        "paypal": "paypal",
        "bank_transfer": "airwallex",  # Airwallex for bank transfers
    }

    provider_type = method_to_provider.get(affiliate.payment_method)

    if provider_type:
        # Get default provider of this type
        provider = PayoutProviderAccount.objects.filter(
            provider_type=provider_type, is_active=True, is_default=True
        ).first()

        if provider:
            return provider

        # Fall back to any active provider of this type
        return PayoutProviderAccount.objects.filter(
            provider_type=provider_type, is_active=True
        ).first()

    return None


def _map_provider_status(provider_status):
    """
    Map provider status enum to payout model status string.

    Args:
        provider_status: PayoutStatus enum value

    Returns:
        str: Status string for Payout model
    """
    from .providers.base import PayoutStatus

    if isinstance(provider_status, str):
        # Already a string
        return provider_status

    status_map = {
        PayoutStatus.PENDING: "pending",
        PayoutStatus.PROCESSING: "processing",
        PayoutStatus.COMPLETED: "completed",
        PayoutStatus.FAILED: "failed",
        PayoutStatus.CANCELLED: "cancelled",
        PayoutStatus.RETURNED: "cancelled",  # Map returned to cancelled
    }

    return status_map.get(provider_status, "pending")
