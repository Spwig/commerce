"""
Webhook endpoint for receiving updates from shipping providers

This module handles inbound webhooks from shipping providers like EasyPost,
ShipStation, etc. Webhooks are used for real-time tracking updates, label
generation callbacks, and error notifications.

Workflow:
1. Receive webhook POST request
2. Log the webhook (WebhookLog model)
3. Verify signature (security)
4. Enqueue processing task (async)
5. Return 200 OK immediately

NOTE: Phase 12 creates the webhook receiver. Actual webhook parsing will be
implemented when provider implementations are complete.
"""
import json
import logging
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.translation import gettext as _

from shipping.models import WebhookLog
from shipping.jobs.tasks import process_webhook
from shipping.providers.registry import ProviderRegistry
from shipping.utils.encryption import decrypt_credentials

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def provider_webhook(request, provider_key):
    """
    Receive webhook from shipping provider.

    URL: POST /admin/shipping/webhooks/<provider_key>/

    Args:
        request: Django HTTP request
        provider_key: Provider slug (e.g., 'easypost', 'shipstation')

    Returns:
        JsonResponse: 200 OK with receipt confirmation

    This endpoint:
    1. Logs all incoming webhooks to WebhookLog
    2. Verifies webhook signature (when provider is implemented)
    3. Enqueues process_webhook Celery task for async processing
    4. Returns 200 OK immediately (doesn't block the provider)

    Security:
    - CSRF exempt (webhooks come from external services)
    - Signature verification required (when provider supports it)
    - All payloads logged for audit trail

    Error Handling:
    - Always returns 200 OK (even on errors)
    - Errors logged but not exposed to provider
    - Failed webhooks can be retried from admin
    """
    start_time = timezone.now()

    # Get request details
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        payload = {'raw_body': request.body.decode('utf-8', errors='replace')}

    headers = {
        key: value
        for key, value in request.META.items()
        if key.startswith('HTTP_') or key in ['CONTENT_TYPE', 'CONTENT_LENGTH']
    }

    # Extract common webhook identifiers
    webhook_id = (
        headers.get('HTTP_X_WEBHOOK_ID') or
        headers.get('HTTP_X_HOOK_ID') or
        payload.get('id') or
        payload.get('webhook_id')
    )

    logger.info(
        f"Webhook received - provider: {provider_key}, "
        f"webhook_id: {webhook_id}, "
        f"endpoint: {request.path}"
    )

    try:
        # Create webhook log entry
        webhook_log = WebhookLog.objects.create(
            provider_key=provider_key,
            endpoint=request.path,
            payload=payload,
            headers=headers,
            processing_status='pending'
        )

        logger.debug(
            f"Webhook logged - log_id: {webhook_log.id}, "
            f"provider: {provider_key}"
        )

        # Verify webhook signature (security)
        provider_class = ProviderRegistry.get_provider(provider_key)
        if provider_class:
            # Try to get the provider account/credentials to access webhook secret
            try:
                from shipping.models import ProviderAccount
                provider_account = ProviderAccount.objects.filter(
                    component__slug=provider_key,
                    is_active=True
                ).first()

                if provider_account:
                    # Extract signature from common header locations
                    signature = (
                        headers.get('HTTP_X_WEBHOOK_SIGNATURE') or
                        headers.get('HTTP_X_SIGNATURE') or
                        headers.get('HTTP_X_HMAC') or
                        headers.get('HTTP_SIGNATURE') or
                        headers.get('X-Webhook-Signature') or
                        headers.get('X-Signature') or
                        headers.get('X-HMAC')
                    )

                    # Try to verify signature
                    try:
                        # Decrypt credentials for provider instance
                        credentials = decrypt_credentials(provider_account.credentials_encrypted)

                        # Create provider instance with decrypted credentials
                        provider_instance = provider_class(
                            credentials=credentials
                        )

                        # Check if provider supports webhook verification
                        if hasattr(provider_instance, 'verify_webhook_signature'):
                            # Verify signature
                            is_valid = provider_instance.verify_webhook_signature(
                                payload=request.body,
                                signature=signature,
                                webhook_secret=credentials.get('webhook_secret')
                            )

                            if not is_valid:
                                logger.warning(
                                    f"Invalid webhook signature from {provider_key} - "
                                    f"log_id: {webhook_log.id}"
                                )
                                webhook_log.processing_status = 'failed'
                                webhook_log.error_message = 'Invalid webhook signature'
                                webhook_log.save()
                                return JsonResponse({
                                    'status': 'error',
                                    'message': 'Invalid signature'
                                }, status=401)

                            logger.debug(f"Webhook signature verified for {provider_key}")
                        else:
                            # Provider doesn't implement signature verification - REJECT
                            logger.error(
                                f"Provider {provider_key} does not implement webhook signature verification"
                            )
                            webhook_log.processing_status = 'failed'
                            webhook_log.error_message = 'Provider does not support webhook verification'
                            webhook_log.save()
                            return JsonResponse({
                                'status': 'error',
                                'message': 'Webhook verification not supported by provider'
                            }, status=401)

                    except NotImplementedError:
                        # Provider explicitly doesn't support webhooks - REJECT
                        logger.error(
                            f"Provider {provider_key} does not support webhooks (NotImplementedError)"
                        )
                        webhook_log.processing_status = 'failed'
                        webhook_log.error_message = 'Provider does not support webhooks'
                        webhook_log.save()
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Webhooks not supported by this provider'
                        }, status=501)  # 501 Not Implemented
                    except Exception as e:
                        # Signature verification failed with error
                        logger.error(
                            f"Webhook signature verification error for {provider_key}: {e}",
                            exc_info=True
                        )
                        webhook_log.processing_status = 'failed'
                        webhook_log.error_message = f'Signature verification error: {str(e)}'
                        webhook_log.save()
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Signature verification failed'
                        }, status=401)

                else:
                    # No provider account configured - REJECT webhook
                    logger.error(
                        f"No active provider account found for {provider_key} - cannot verify webhook"
                    )
                    webhook_log.processing_status = 'failed'
                    webhook_log.error_message = 'No provider account configured for webhook verification'
                    webhook_log.save()
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Provider account not configured'
                    }, status=401)

            except Exception as e:
                logger.error(
                    f"Error loading provider account for signature verification: {e}",
                    exc_info=True
                )
                webhook_log.processing_status = 'failed'
                webhook_log.error_message = f'Unable to verify webhook authenticity: {str(e)}'
                webhook_log.save()
                return JsonResponse({
                    'status': 'error',
                    'message': 'Unable to verify webhook authenticity'
                }, status=401)
        else:
            # Provider not found in registry - REJECT
            logger.error(
                f"Provider {provider_key} not found in registry - cannot verify webhook"
            )
            webhook_log.processing_status = 'failed'
            webhook_log.error_message = 'Provider not registered'
            webhook_log.save()
            return JsonResponse({
                'status': 'error',
                'message': 'Unknown provider'
            }, status=400)

        # Enqueue processing task (async)
        process_webhook.delay(str(webhook_log.id))

        logger.info(
            f"Webhook queued for processing - log_id: {webhook_log.id}, "
            f"provider: {provider_key}, "
            f"processing_time: {(timezone.now() - start_time).total_seconds():.3f}s"
        )

        # Return 200 OK immediately
        # Don't block the provider with long processing
        return JsonResponse({
            'status': 'received',
            'webhook_id': str(webhook_log.id),
            'message': 'Webhook received and queued for processing',
            'received_at': start_time.isoformat()
        }, status=200)

    except Exception as exc:
        # Log error but still return 200 OK
        # We don't want providers to keep retrying on our bugs
        logger.error(
            f"Webhook processing error - provider: {provider_key}, "
            f"error: {str(exc)}",
            exc_info=True
        )

        # Try to log the error
        try:
            webhook_log = WebhookLog.objects.create(
                provider_key=provider_key,
                endpoint=request.path,
                payload=payload,
                headers=headers,
                processing_status='failed',
                error_message=f"Webhook receiver error: {str(exc)}"
            )
        except Exception:
            # Even logging failed, just log to app logs
            logger.error(
                f"Failed to create webhook log for {provider_key}",
                exc_info=True
            )

        # Still return 200 OK to prevent provider retries
        return JsonResponse({
            'status': 'error',
            'message': 'Internal error processing webhook',
            'received_at': start_time.isoformat()
        }, status=200)


def webhook_health_check(request):
    """
    Health check endpoint for webhook system.

    URL: GET /webhooks/shipping/health/

    Returns:
        JsonResponse: System health status

    This endpoint can be used by monitoring systems to verify
    the webhook endpoint is operational.
    """
    if request.method not in ['GET', 'HEAD']:
        return HttpResponse(status=405)

    return JsonResponse({
        'status': 'healthy',
        'service': 'shipping-webhooks',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0'
    })


@staff_member_required
def webhook_documentation(request):
    """
    Webhook endpoint documentation page.

    URL: GET /admin/shipping/webhooks/

    Returns:
        HTML page with webhook documentation

    This provides human-readable documentation for developers
    integrating with the webhook system.
    """
    from django.shortcuts import render

    webhook_examples = [
        {
            'provider': 'easypost',
            'url': request.build_absolute_uri('/admin/shipping/webhooks/easypost/'),
            'description': _('EasyPost tracking updates and label events')
        },
        {
            'provider': 'shipstation',
            'url': request.build_absolute_uri('/admin/shipping/webhooks/shipstation/'),
            'description': _('ShipStation shipment notifications')
        },
        {
            'provider': 'custom',
            'url': request.build_absolute_uri('/admin/shipping/webhooks/custom/'),
            'description': _('Custom provider webhooks')
        },
    ]

    context = {
        'title': _('Shipping Webhooks'),
        'webhook_examples': webhook_examples,
        'health_check_url': request.build_absolute_uri('/admin/shipping/webhooks/health/'),
    }

    return render(request, 'admin/shipping/webhooks/documentation.html', context)
