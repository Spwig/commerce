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
        with transaction.atomic():
            payout = (
                Payout.objects.select_for_update().select_related("affiliate").get(id=payout_id)
            )

            # Check if already processed. Holding the row lock while we re-check
            # and claim the payout means a concurrent duplicate delivery or a
            # retry racing the original cannot both pass this guard and call
            # create_payout, which would double-pay the affiliate.
            if payout.status in ("completed", "processing"):
                logger.warning(f"Payout {payout_id} already {payout.status}, skipping")
                return {
                    "success": False,
                    "error": f"Payout already {payout.status}",
                    "payout_id": payout_id,
                }

            # Claim the payout before the lock is released so no other worker can
            # pass the guard above for the same payout.
            payout.mark_as_processing()
    except Payout.DoesNotExist:
        logger.error(f"Payout {payout_id} not found")
        return {"success": False, "error": "Payout not found", "payout_id": payout_id}

    affiliate = payout.affiliate

    # Everything below runs after the payout has already been claimed as
    # 'processing'. It must all sit inside this try: an exception during provider
    # lookup, instantiation, or request construction would otherwise escape, and
    # because the task autoretries on any Exception the retry would hit the
    # 'already processing, skipping' guard above and abandon the payout forever
    # (the sync fallback only rescues rows that have a provider_reference, which
    # such a payout never gets). Catching here marks it failed first, so the
    # retry re-enters past the guard and reprocesses.
    try:
        # Determine provider account
        if provider_account_id:
            try:
                provider_account = PayoutProviderAccount.objects.get(
                    id=provider_account_id, is_active=True
                )
            except PayoutProviderAccount.DoesNotExist:
                error_msg = f"Provider account {provider_account_id} not found or inactive"
                logger.error(error_msg)
                # The payout was already claimed as 'processing' above; without
                # this it would be stuck there forever.
                payout.mark_as_failed(notes=error_msg)
                return {
                    "success": False,
                    "error": "Provider account not found",
                    "payout_id": payout_id,
                }
        else:
            # Auto-select based on affiliate's payment method
            provider_account = _get_provider_for_affiliate(affiliate)

        if not provider_account:
            error_msg = f"No active provider found for payment method: {affiliate.payment_method}"
            logger.error(error_msg)
            payout.mark_as_failed(notes=error_msg)
            return {"success": False, "error": error_msg, "payout_id": payout_id}

        # Get provider class and instantiate
        provider_class = get_provider_class(
            provider_account.provider_type, provider_account.component
        )

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
            affiliate_id=affiliate.id,
            email=affiliate.paypal_email or affiliate.user.email,
            bank_account_holder=affiliate.bank_account_holder,
            bank_account_number=affiliate.bank_account_number,
            bank_routing_code=affiliate.bank_routing_code,
            bank_swift_code=affiliate.bank_swift_code,
            bank_country=affiliate.bank_country or affiliate.country,
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

    # Load payouts. Only 'pending' rows are eligible. pending_ids is the
    # candidate set; the actual set this worker claims (claimed_ids, computed
    # under a row lock below) is what every later status update targets, never
    # the raw payout_ids, so we never force-process an id that was already
    # completed/failed and never built into a request.
    payouts = list(
        Payout.objects.filter(id__in=payout_ids, status="pending").select_related("affiliate")
    )

    if not payouts:
        return {"success": False, "error": "No pending payouts found"}

    pending_ids = [payout.id for payout in payouts]

    # Build payout requests
    payout_requests = []
    payout_map = {}  # Map payout id to payout for later update

    for payout in payouts:
        affiliate = payout.affiliate

        recipient = PayoutRecipient(
            affiliate_id=affiliate.id,
            email=affiliate.paypal_email or affiliate.user.email,
            bank_account_holder=affiliate.bank_account_holder,
            bank_account_number=affiliate.bank_account_number,
            bank_routing_code=affiliate.bank_routing_code,
            bank_swift_code=affiliate.bank_swift_code,
            bank_country=affiliate.bank_country or affiliate.country,
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
        payout_map[payout.id] = payout

    # The exact set of ids this worker wins the claim for. Only these are ever
    # submitted to the provider or touched by any later status update.
    claimed_ids = []

    try:
        # Claim only the rows we actually win. select_for_update locks the
        # still-pending rows so a concurrent batch sharing an id cannot also
        # claim it; claimed_ids is the precise rowset this worker owns. A
        # conditional UPDATE ... WHERE status='pending' alone cannot tell us
        # which rows it changed, so a losing concurrent batch would still submit
        # its prebuilt request for that id = double payment. Locking and reading
        # the pending rows first gives us that set. The lock is released when the
        # atomic block commits status='processing'; that claim is durable, so we
        # deliberately do NOT hold the lock across the provider network call.
        with transaction.atomic():
            locked = list(
                Payout.objects.select_for_update().filter(id__in=pending_ids, status="pending")
            )
            claimed_ids = [payout.id for payout in locked]
            if claimed_ids:
                Payout.objects.filter(id__in=claimed_ids).update(
                    status="processing",
                    processed_at=timezone.now(),
                    provider_account=provider_account,
                )

        if not claimed_ids:
            # Every candidate row was won by a concurrent batch; submit nothing.
            return {"success": False, "error": "No pending payouts found"}

        # Restrict the submission set to the rows we actually claimed. Rows won
        # by another worker were left untouched and must never be sent to the
        # provider.
        claimed_set = set(claimed_ids)
        payout_requests = [req for req in payout_requests if req.payout_id in claimed_set]

        # Call batch payout
        batch_result = provider.create_batch_payout(payout_requests)

        if batch_result.success:
            # Inspect per-item results so requests the provider skipped/rejected
            # (e.g. a recipient with no PayPal email) are not recorded as
            # submitted payouts. Fall back to treating the whole batch as
            # submitted only when the provider returns no per-item detail.
            submitted_ids = []
            failed_items = []  # (payout_id, message)
            if batch_result.results and len(batch_result.results) == len(payout_requests):
                for req, item_result in zip(payout_requests, batch_result.results, strict=True):
                    if item_result.success:
                        submitted_ids.append(req.payout_id)
                    else:
                        failed_items.append((req.payout_id, item_result.message))
            else:
                submitted_ids = list(claimed_ids)

            if submitted_ids:
                # Every payout in the batch shares the one batch_reference, so it
                # cannot uniquely identify a payout for item-level webhooks.
                # Persist the unique per-item reference (echoed by the provider as
                # sender_item_id) on each payout so item events resolve to exactly
                # one record, while the batch reference drives batch-level events.
                submitted_payouts = []
                for payout_id in submitted_ids:
                    payout = payout_map[payout_id]
                    payout.reference = f"SPWIG-PAYOUT-{payout.id}"
                    payout.provider_reference = batch_result.batch_reference or ""
                    payout.provider_response = batch_result.raw_response or {}
                    submitted_payouts.append(payout)
                Payout.objects.bulk_update(
                    submitted_payouts, ["reference", "provider_reference", "provider_response"]
                )

            for failed_id, message in failed_items:
                Payout.objects.filter(id=failed_id).update(
                    status="failed",
                    notes=message or "Payout skipped by provider",
                    provider_response=batch_result.raw_response or {},
                )

            logger.info(
                f"Batch payout submitted. Ref: {batch_result.batch_reference}. "
                f"Submitted: {len(submitted_ids)}, skipped: {len(failed_items)}"
            )

            return {
                "success": True,
                "batch_reference": batch_result.batch_reference,
                "message": batch_result.message,
                "count": len(submitted_ids),
                "failed_count": len(failed_items),
            }
        else:
            # Batch was rejected outright by the provider - mark the claimed
            # set failed (never the raw payout_ids or rows won by another worker).
            Payout.objects.filter(id__in=claimed_ids).update(
                status="failed",
                notes=batch_result.message or "Batch submission failed",
                provider_response=batch_result.raw_response or {},
            )

            logger.error(f"Batch payout failed: {batch_result.message}")

            return {"success": False, "error": batch_result.message, "count": len(claimed_ids)}

    except Exception as e:
        logger.error(f"Error processing batch payout: {e}", exc_info=True)

        if self.request.retries < self.max_retries:
            # Restore the claimed payouts to 'pending' so the retried invocation
            # can resubmit them. Marking them 'failed' here would make the retry
            # filter (status="pending") find nothing and submit nothing. Only the
            # rows this worker claimed are restored; rows won by another worker
            # stay untouched.
            Payout.objects.filter(id__in=claimed_ids, status="processing").update(status="pending")
            raise self.retry(exc=e)

        # Retries exhausted - now it is safe to record the failure.
        Payout.objects.filter(id__in=claimed_ids).update(status="failed", notes=str(e))

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

            _apply_provider_status(
                payout,
                new_status,
                message=result.message or "",
                raw_response=result.raw_response,
            )
            logger.info(f"Payout {payout_id} synced: {old_status} -> {payout.status}")

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

        # Resolve the affected payouts. A batch shares one batch reference across
        # every payout, so batch-level events must update all records in the
        # batch; item-level events carry a unique per-item reference and must
        # resolve to exactly one payout (never an arbitrary .first()).
        event_type = event_data.get("event_type", "") or ""
        if "ITEM" in event_type.upper():
            payouts = list(Payout.objects.filter(reference=payout_reference))
        else:
            payouts = list(Payout.objects.filter(provider_reference=payout_reference))

        if not payouts:
            webhook_log.payout_reference = payout_reference
            webhook_log.processed = True
            webhook_log.processed_at = timezone.now()
            webhook_log.save()
            logger.warning(f"No payout found for reference: {payout_reference}")
            return {
                "success": True,
                "message": f"No payout found for reference: {payout_reference}",
            }

        # Apply the provider status with the same terminal-state guards used by
        # sync_payout_status, so a late/duplicate cancellation cannot regress an
        # already completed payout. Cancellations route through Payout.cancel(),
        # which reverts the related commissions.
        new_status = _map_provider_status(provider_status)
        message = event_data.get("message", "")
        raw_data = event_data.get("raw_data", {})

        updated_ids = []
        for payout in payouts:
            if _apply_provider_status(payout, new_status, message=message, raw_response=raw_data):
                updated_ids.append(payout.id)
            logger.info(f"Payout {payout.id} webhook processed; status={payout.status}")

        # Mark webhook as processed
        webhook_log.payout_reference = payout_reference
        webhook_log.processed = True
        webhook_log.processed_at = timezone.now()
        webhook_log.save()

        return {
            "success": True,
            "payout_ids": [payout.id for payout in payouts],
            "updated_ids": updated_ids,
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


def _apply_provider_status(payout, new_status, message="", raw_response=None):
    """Apply a provider-reported status to a payout, guarding terminal states.

    Shared by webhook processing and the status-sync fallback so both apply the
    same guards: a payout already in a terminal state (completed/failed/
    cancelled) is never regressed by a late or duplicate event, and
    cancellations route through ``Payout.cancel`` so the related commissions are
    reverted consistently.

    Returns True if the payout status changed.
    """
    raw_response = raw_response or {}

    if new_status == "completed" and payout.status != "completed":
        payout.mark_as_completed(
            provider_reference=payout.provider_reference,
            provider_response=raw_response,
        )
        return True

    if new_status == "failed" and payout.status not in ("completed", "failed"):
        payout.mark_as_failed(
            notes=message or "Provider reported failure",
            provider_response=raw_response,
        )
        return True

    if new_status in ("returned", "cancelled") and payout.status not in (
        "completed",
        "failed",
        "cancelled",
    ):
        payout.cancel(notes=message or f"Provider status: {new_status}")
        payout.provider_response = raw_response
        payout.save(update_fields=["provider_response"])
        return True

    # No status transition; persist the latest response for the audit trail.
    payout.provider_response = raw_response
    payout.save(update_fields=["provider_response"])
    return False


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
