"""
License Checkout Provisioning Service

Handles communication with the upgrade server to create licenses and setup
tokens for license purchases and trials on spwig.com.

Uses the same upgrade server endpoints as developer_portal/services/license_provisioning.py:
- POST /api/v1/internal/licenses/  — create license
- POST /api/v1/setup-tokens/      — create setup token
"""

import logging

import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime

from .models import LicenseCheckoutRequest

logger = logging.getLogger(__name__)


def _mask_email(email):
    """Mask email for safe logging."""
    if '@' not in email:
        return '***'
    local, domain = email.split('@', 1)
    masked_local = local[:2] + '***' if len(local) > 2 else '***'
    return f"{masked_local}@{domain}"


def _api_headers():
    return {'X-API-KEY': settings.UPGRADE_SERVER_INTERNAL_API_KEY}


def _log_api_error(operation, response):
    """Log a non-success API response with details."""
    try:
        body = response.json()
        error = body.get('error', '')
        message = body.get('message', '')
        logger.error(
            f"Upgrade server {operation} failed "
            f"(status={response.status_code}): error={error} message={message}"
        )
    except (ValueError, requests.exceptions.JSONDecodeError):
        logger.error(
            f"Upgrade server {operation} returned non-JSON "
            f"(status={response.status_code}): {response.text[:200]}"
        )


def _determine_license_params(checkout_request):
    """
    Determine upgrade server license parameters based on product slug.

    Returns (license_type, product_type, allowed_channels, trial_days)
    """
    slug = checkout_request.license_product.slug
    trial_days = checkout_request.license_product.trial_days

    if slug == 'trial-core-pos':
        return 'trial', 'bundle', ['stable'], trial_days
    elif slug == 'core-license':
        return 'production', 'shop', ['stable'], 0
    elif slug == 'bundle-core-pos':
        return 'production', 'bundle', ['stable'], 0
    elif slug == 'dev-license':
        return 'dev', 'bundle', ['stable', 'beta', 'dev'], 0
    else:
        # Fallback for any custom products added later
        includes_pos = checkout_request.license_product.includes_pos
        product_type = 'bundle' if includes_pos else 'shop'
        return 'production', product_type, ['stable'], 0


def _create_license(checkout_request, license_type, product_type, allowed_channels, trial_days):
    """
    Create a license on the upgrade server.

    Returns the license_key string.
    Raises ValueError or requests.RequestException on failure.
    """
    payload = {
        'owner_name': checkout_request.name or checkout_request.email.split('@')[0],
        'owner_email': checkout_request.email,
        'company': getattr(checkout_request, 'company', '') or '',
        'country': str(checkout_request.billing_country) if checkout_request.billing_country else '',
        'license_type': license_type,
        'product_type': product_type,
        'max_installations': 1,
        'allowed_channels': allowed_channels,
        'metadata': {
            'checkout_request_id': str(checkout_request.id),
            'product_slug': checkout_request.license_product.slug,
        },
    }

    if trial_days > 0:
        payload['trial_days'] = trial_days

    url = f"{settings.UPGRADE_SERVER_URL}/api/v1/internal/licenses/"

    try:
        resp = requests.post(url, json=payload, headers=_api_headers(), timeout=15)
    except requests.RequestException as e:
        logger.error(f"Upgrade server unreachable for license creation: {e}")
        raise

    if resp.status_code == 409:
        raise ValueError('A license with this key already exists')

    if resp.status_code != 201:
        _log_api_error('license creation', resp)
        raise ValueError('Unable to create license')

    data = resp.json()
    license_key = data['license_key']

    # Save immediately in case setup token creation fails
    checkout_request.license_key = license_key
    checkout_request.save(update_fields=['license_key'])

    return license_key


def _create_setup_token(checkout_request, license_key):
    """
    Create a setup token on the upgrade server for the given license.

    Returns the token data dict.
    Raises ValueError or requests.RequestException on failure.
    """
    payload = {
        'license_key': license_key,
        'email': checkout_request.email,
        'owner_name': checkout_request.name or checkout_request.email.split('@')[0],
        'company_name': getattr(checkout_request, 'company', '') or '',
    }

    url = f"{settings.UPGRADE_SERVER_URL}/api/v1/setup-tokens/"

    try:
        resp = requests.post(url, json=payload, headers=_api_headers(), timeout=15)
    except requests.RequestException as e:
        logger.error(
            f"License {license_key} created but setup token failed: {e}"
        )
        raise

    if resp.status_code != 201:
        _log_api_error('setup token creation', resp)
        raise ValueError(
            'License was created but setup token generation failed. '
            'Please contact support.'
        )

    return resp.json()


def _save_provisioning_result(checkout_request, token_data):
    """Save the setup token data to the checkout request."""
    checkout_request.setup_token = token_data.get('token', '')
    checkout_request.setup_token_id = token_data.get('token_id')
    checkout_request.status = LicenseCheckoutRequest.Status.COMPLETED

    token_expires = token_data.get('expires_at')
    if token_expires:
        checkout_request.setup_token_expires_at = parse_datetime(token_expires)

    checkout_request.save(update_fields=[
        'license_key', 'setup_token', 'setup_token_id',
        'setup_token_expires_at', 'status',
    ])


def provision_trial_license(checkout_request):
    """
    Provision a free trial license — no payment required.

    Creates a license and setup token on the upgrade server,
    then sends a welcome email.

    Args:
        checkout_request: LicenseCheckoutRequest instance

    Raises:
        ValueError: Business logic error from upgrade server
        requests.RequestException: Network error
    """
    license_type, product_type, allowed_channels, trial_days = _determine_license_params(checkout_request)

    # Step 1: Create license
    license_key = _create_license(
        checkout_request, license_type, product_type, allowed_channels, trial_days,
    )

    # Step 2: Create setup token
    token_data = _create_setup_token(checkout_request, license_key)

    # Step 3: Save results
    _save_provisioning_result(checkout_request, token_data)

    logger.info(
        f"Provisioned trial license: email={_mask_email(checkout_request.email)} "
        f"license_key={license_key} trial_days={trial_days}"
    )

    # Step 4: Send welcome email
    _send_trial_email(checkout_request)

    return {
        'license_key': license_key,
        'setup_token': token_data.get('token', ''),
        'setup_token_expires_at': token_data.get('expires_at'),
    }


def provision_paid_license(order):
    """
    Provision a paid license after successful payment.

    Called from PaymentOrchestrationService._trigger_post_payment_flows()
    when order.metadata.get('license_checkout') is truthy.

    Args:
        order: Order instance with license_checkout metadata
    """
    request_id = order.metadata.get('license_checkout_request_id')
    if not request_id:
        logger.error(f"No license_checkout_request_id in order {order.order_number} metadata")
        return

    try:
        checkout_request = LicenseCheckoutRequest.objects.get(id=request_id)
    except LicenseCheckoutRequest.DoesNotExist:
        logger.error(
            f"LicenseCheckoutRequest {request_id} not found "
            f"for order {order.order_number}"
        )
        return

    checkout_request.status = LicenseCheckoutRequest.Status.PROVISIONING
    checkout_request.order = order
    checkout_request.save(update_fields=['status', 'order'])

    # Route maintenance renewals to the dedicated handler
    if checkout_request.license_product.slug == 'maintenance-renewal':
        provision_maintenance_renewal(order)
        return

    license_type, product_type, allowed_channels, trial_days = _determine_license_params(checkout_request)

    try:
        # Step 1: Create license
        license_key = _create_license(
            checkout_request, license_type, product_type, allowed_channels, trial_days,
        )

        # Step 2: Create setup token
        token_data = _create_setup_token(checkout_request, license_key)

        # Step 3: Save results
        _save_provisioning_result(checkout_request, token_data)

        logger.info(
            f"Provisioned paid license: email={_mask_email(checkout_request.email)} "
            f"license_key={license_key} product={checkout_request.license_product.slug} "
            f"order={order.order_number}"
        )

    except Exception as e:
        logger.error(
            f"Failed to provision license for order {order.order_number}: {e}"
        )
        checkout_request.status = LicenseCheckoutRequest.Status.FAILED
        checkout_request.error_message = str(e)[:500]
        checkout_request.save(update_fields=['status', 'error_message'])
        return

    # Step 4: Send confirmation email
    _send_purchase_email(checkout_request)

    # Step 5: Set up maintenance subscription (non-blocking)
    try:
        create_maintenance_subscription(checkout_request, order)
    except Exception as e:
        logger.error(
            f"Maintenance subscription setup failed for order "
            f"{order.order_number}: {e}"
        )


def create_maintenance_subscription(checkout_request, order):
    """
    Set up annual maintenance subscription after a paid license purchase.

    Creates an Airwallex payment consent from the initial payment's method,
    then creates a CustomerSubscription that will be billed annually by the
    existing Celery fallback billing engine (process_due_subscriptions).

    Maintenance fee = 25% of license price, starting 12 months after purchase.

    Skips silently for trial and dev-license products (no maintenance required).
    """
    # Only core-license and bundle-core-pos need maintenance
    slug = checkout_request.license_product.slug
    if slug in ('trial-core-pos', 'dev-license'):
        return

    # Need customer_id from checkout initiation
    customer_id = (checkout_request.metadata or {}).get('airwallex_customer_id')
    if not customer_id:
        logger.warning(
            f"No airwallex_customer_id for checkout {checkout_request.id} — "
            f"skipping maintenance subscription"
        )
        return

    # Get the payment intent to retrieve payment method details
    intent = checkout_request.payment_intent
    if not intent:
        logger.warning(
            f"No payment intent linked to checkout {checkout_request.id} — "
            f"skipping maintenance subscription"
        )
        return

    provider_account = intent.provider_account

    # Retrieve the completed payment intent from Airwallex to get payment_method
    provider = provider_account.get_provider_instance()
    intent_data = provider.retrieve_payment_intent(intent.provider_intent_id)

    if not intent_data.get('success'):
        logger.error(
            f"Failed to retrieve payment intent {intent.provider_intent_id}: "
            f"{intent_data.get('error')}"
        )
        return

    raw_response = intent_data.get('raw_response', {})
    latest_attempt = raw_response.get('latest_payment_attempt', {})
    payment_method = latest_attempt.get('payment_method', {})
    payment_method_id = payment_method.get('id', '')

    if not payment_method_id:
        logger.warning(
            f"No payment_method_id found in payment intent "
            f"{intent.provider_intent_id} — skipping maintenance subscription"
        )
        return

    # Create payment consent for recurring billing
    from subscriptions.provider_base import get_provider as get_subscription_provider

    sub_provider = get_subscription_provider(provider_account)
    token_result = sub_provider.create_payment_token(
        customer_id=customer_id,
        payment_method_data={'payment_method_id': payment_method_id},
    )

    consent_id = token_result.get('token_id', '')
    if not consent_id:
        logger.error(
            f"Payment consent creation returned no token_id for "
            f"checkout {checkout_request.id}"
        )
        return

    # Find the user (created during checkout initiation)
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(email__iexact=checkout_request.email)
    except User.DoesNotExist:
        logger.error(
            f"User not found for email {_mask_email(checkout_request.email)} — "
            f"skipping maintenance subscription"
        )
        return

    # Save PaymentToken
    from subscriptions.models import PaymentToken

    payment_token = PaymentToken.objects.create(
        user=user,
        provider_account=provider_account,
        gateway_customer_id=customer_id,
        gateway_token_id=consent_id,
        payment_method_type=token_result.get('payment_method_type', 'card'),
        card_brand=token_result.get('card_brand', ''),
        card_last4=token_result.get('card_last4', ''),
        card_exp_month=token_result.get('card_exp_month'),
        card_exp_year=token_result.get('card_exp_year'),
        is_default=True,
        is_active=True,
        is_verified=True,
    )

    # Get the subscription plan and pricing tier
    from subscriptions.models import SubscriptionPlan

    try:
        plan = SubscriptionPlan.objects.get(slug='license-maintenance')
    except SubscriptionPlan.DoesNotExist:
        logger.error(
            "SubscriptionPlan 'license-maintenance' not found — "
            "run seed_license_products first"
        )
        return

    pricing_tier = plan.get_default_tier()
    if not pricing_tier:
        logger.error(
            "No pricing tier found for license-maintenance plan"
        )
        return

    # Find the catalog product (created during checkout initiation)
    from catalog.models import Product

    product_sku = f'lic-{checkout_request.license_product.slug}'
    try:
        catalog_product = Product.objects.get(sku=product_sku)
    except Product.DoesNotExist:
        logger.error(
            f"Catalog product {product_sku} not found — "
            f"skipping maintenance subscription"
        )
        return

    # Create subscription via SubscriptionManager
    from subscriptions.manager import SubscriptionManager

    manager = SubscriptionManager(provider_account)
    subscription = manager.create_subscription(
        user=user,
        plan=plan,
        pricing_tier=pricing_tier,
        payment_token=payment_token,
        product=catalog_product,
        originating_order=order,
    )

    logger.info(
        f"Created maintenance subscription {subscription.subscription_id} "
        f"for {_mask_email(checkout_request.email)}: "
        f"next_billing={subscription.next_billing_date.date()}"
    )


def get_renewal_info(license_key):
    """
    Fetch license details from the update server and calculate renewal price.

    Calls the update server's internal maintenance endpoint to get current
    status, then looks up the corresponding LicenseProduct to calculate the
    renewal price as 25% of the current list price (regular_price).

    Args:
        license_key: The license key to look up (e.g. 'CORE-XXXX-XXXX-XXXX')

    Returns:
        dict with renewal details, or raises ValueError on failure.
    """
    # Step 1: Get maintenance status from update server
    url = f"{settings.UPGRADE_SERVER_URL}/api/v1/internal/licenses/{license_key}/maintenance/"

    try:
        resp = requests.get(url, headers=_api_headers(), timeout=10)
    except requests.RequestException as e:
        logger.error(f"Update server unreachable for renewal info: {e}")
        raise ValueError('Unable to verify license. Please try again later.')

    if resp.status_code == 404:
        raise ValueError('License not found')

    if resp.status_code != 200:
        _log_api_error('renewal info', resp)
        raise ValueError('Unable to verify license')

    maintenance_data = resp.json()

    # Step 2: Get license metadata to determine product type
    license_url = f"{settings.UPGRADE_SERVER_URL}/api/v1/internal/licenses/{license_key}/"

    try:
        license_resp = requests.get(license_url, headers=_api_headers(), timeout=10)
    except requests.RequestException as e:
        logger.error(f"Update server unreachable for license details: {e}")
        raise ValueError('Unable to verify license. Please try again later.')

    if license_resp.status_code != 200:
        _log_api_error('license details', license_resp)
        raise ValueError('Unable to verify license')

    license_data = license_resp.json()
    product_type = license_data.get('product_type', 'shop')
    owner_email = license_data.get('owner_email', '')
    owner_name = license_data.get('owner_name', '')
    license_type = license_data.get('license_type', '')

    # Don't allow renewal for trial/dev licenses
    if license_type in ('trial', 'dev'):
        raise ValueError(
            'Maintenance renewal is not available for trial or developer licenses'
        )

    # Step 3: Calculate price from current list price
    if product_type == 'bundle':
        base_slug = 'bundle-core-pos'
    else:
        base_slug = 'core-license'

    try:
        base_product = LicenseProduct.objects.get(slug=base_slug, is_active=True)
    except LicenseProduct.DoesNotExist:
        logger.error(f"Base product {base_slug} not found for renewal pricing")
        raise ValueError('Unable to calculate renewal price')

    from decimal import Decimal, ROUND_HALF_UP

    # 25% of the regular (list) price
    list_price = base_product.regular_price.amount
    renewal_price = (list_price * Decimal('0.25')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    # Step 4: Major version enforcement
    # If maintenance lapsed past grace period and a new major version was
    # released, the merchant must purchase a new license instead of renewing.
    major_entitled = maintenance_data.get('major_version_entitled', 1)
    latest_major = maintenance_data.get('latest_major_version', 1)
    maintenance_active = maintenance_data.get('maintenance_active', False)
    reinstatement_tier = maintenance_data.get('reinstatement_tier', 'standard')

    upgrade_required = (
        latest_major > major_entitled
        and not maintenance_active
        and reinstatement_tier != 'grace'
    )

    return {
        'license_key': license_key,
        'product_type': product_type,
        'base_product_name': base_product.name,
        'list_price': str(list_price),
        'renewal_price': str(renewal_price),
        'currency': str(base_product.regular_price.currency),
        'owner_email': owner_email,
        'owner_name': owner_name,
        'maintenance_active': maintenance_active,
        'in_grace_period': maintenance_data.get('in_grace_period', False),
        'days_remaining': maintenance_data.get('days_remaining'),
        'grace_days_remaining': maintenance_data.get('grace_days_remaining', 0),
        'reinstatement_tier': reinstatement_tier,
        'upgrade_required': upgrade_required,
        'major_version_entitled': major_entitled,
        'latest_major_version': latest_major,
    }


def provision_maintenance_renewal(order):
    """
    Extend maintenance on an existing license after successful renewal payment.

    Called from PaymentOrchestrationService._trigger_post_payment_flows()
    when the checkout request is for a maintenance-renewal product.

    Args:
        order: Order instance with license_checkout metadata
    """
    request_id = order.metadata.get('license_checkout_request_id')
    if not request_id:
        logger.error(
            f"No license_checkout_request_id in order {order.order_number} metadata"
        )
        return

    try:
        checkout_request = LicenseCheckoutRequest.objects.get(id=request_id)
    except LicenseCheckoutRequest.DoesNotExist:
        logger.error(
            f"LicenseCheckoutRequest {request_id} not found "
            f"for order {order.order_number}"
        )
        return

    checkout_request.status = LicenseCheckoutRequest.Status.PROVISIONING
    checkout_request.order = order
    checkout_request.save(update_fields=['status', 'order'])

    renewal_key = (checkout_request.metadata or {}).get('renewal_license_key', '')
    if not renewal_key:
        logger.error(
            f"No renewal_license_key in checkout {checkout_request.id} metadata"
        )
        checkout_request.status = LicenseCheckoutRequest.Status.FAILED
        checkout_request.error_message = 'Missing license key for renewal'
        checkout_request.save(update_fields=['status', 'error_message'])
        return

    try:
        # Safety check: re-validate upgrade requirement to prevent race conditions
        # (e.g. major version released between checkout start and payment completion)
        try:
            renewal_info = get_renewal_info(renewal_key)
            if renewal_info.get('upgrade_required'):
                raise ValueError(
                    'A new major version was released. '
                    'Renewal blocked — new license purchase required.'
                )
        except ValueError as ve:
            if 'major version' in str(ve).lower():
                raise
            # Other ValueError (e.g. network timeout) — don't block provisioning
            # for transient errors; the original checkout already validated
            logger.warning(
                f"Could not re-validate renewal for {renewal_key}: {ve}"
            )

        # Calculate new expiry: 1 year from now
        from django.utils import timezone as tz
        from datetime import timedelta as td
        new_expiry = (tz.now() + td(days=365)).isoformat()

        # Call update server to extend maintenance
        url = (
            f"{settings.UPGRADE_SERVER_URL}"
            f"/api/v1/internal/licenses/{renewal_key}/maintenance/"
        )
        payload = {
            'expires_at': new_expiry,
            'order_reference': order.order_number,
        }

        resp = requests.post(url, json=payload, headers=_api_headers(), timeout=15)

        if resp.status_code not in (200, 201):
            _log_api_error('maintenance renewal', resp)
            raise ValueError('Update server failed to extend maintenance')

        result = resp.json()

        checkout_request.license_key = renewal_key
        checkout_request.status = LicenseCheckoutRequest.Status.COMPLETED
        checkout_request.metadata['renewal_result'] = {
            'action': result.get('action', 'renewed'),
            'expires_at': result.get('expires_at'),
            'pre_renewal_lapse_days': result.get('pre_renewal_lapse_days', 0),
        }
        checkout_request.save(
            update_fields=['license_key', 'status', 'metadata']
        )

        logger.info(
            f"Maintenance renewed: license={renewal_key} "
            f"order={order.order_number} "
            f"action={result.get('action')} "
            f"expires_at={result.get('expires_at')}"
        )

    except Exception as e:
        logger.error(
            f"Failed to renew maintenance for license {renewal_key}, "
            f"order {order.order_number}: {e}"
        )
        checkout_request.status = LicenseCheckoutRequest.Status.FAILED
        checkout_request.error_message = str(e)[:500]
        checkout_request.save(update_fields=['status', 'error_message'])
        return

    # Send renewal confirmation email
    _send_renewal_email(checkout_request)


def _send_renewal_email(checkout_request):
    """Send maintenance renewal confirmation email."""
    try:
        from email_system.services.email_sender import EmailSendingService

        language = (checkout_request.metadata or {}).get('language', 'en')
        renewal_result = (checkout_request.metadata or {}).get('renewal_result', {})

        outbox = EmailSendingService.send_template_email(
            to_email=checkout_request.email,
            template_type='license_maintenance_renewal',
            context={
                'customer_name': checkout_request.name or 'there',
                'license_key': checkout_request.license_key,
                'renewal_expires_at': renewal_result.get('expires_at', ''),
                'order_number': (
                    checkout_request.order.order_number
                    if checkout_request.order else ''
                ),
            },
            language=language,
        )
        if outbox and outbox.status == 'queued':
            EmailSendingService.send_email(str(outbox.id))
            logger.info(
                f"Sent renewal confirmation to "
                f"{_mask_email(checkout_request.email)}"
            )
        elif outbox and outbox.status == 'skipped':
            logger.info(
                f"Renewal email skipped for "
                f"{_mask_email(checkout_request.email)}: {outbox.skip_reason}"
            )
    except Exception as e:
        logger.error(
            f"Failed to send renewal email to "
            f"{_mask_email(checkout_request.email)}: {e}"
        )


def _send_trial_email(checkout_request):
    """Send trial welcome email with setup token."""
    try:
        from email_system.services.email_sender import EmailSendingService

        language = (checkout_request.metadata or {}).get('language', 'en')

        outbox = EmailSendingService.send_template_email(
            to_email=checkout_request.email,
            template_type='license_trial_welcome',
            context={
                'customer_name': checkout_request.name or 'there',
                'product_name': checkout_request.license_product.name,
                'trial_days': checkout_request.license_product.trial_days,
                'setup_token': checkout_request.setup_token,
                'setup_url': f"https://docs.spwig.com/getting-started/",
                'includes_pos': checkout_request.license_product.includes_pos,
            },
            language=language,
        )
        if outbox and outbox.status == 'queued':
            EmailSendingService.send_email(str(outbox.id))
            logger.info(f"Sent trial welcome email to {_mask_email(checkout_request.email)}")
        elif outbox and outbox.status == 'skipped':
            logger.info(f"Trial welcome email skipped for {_mask_email(checkout_request.email)}: {outbox.skip_reason}")
    except Exception as e:
        logger.error(f"Failed to send trial welcome email to {_mask_email(checkout_request.email)}: {e}")


def _send_purchase_email(checkout_request):
    """Send purchase confirmation email with setup token and activation link."""
    try:
        from django.contrib.auth import get_user_model
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        from email_system.services.email_sender import EmailSendingService

        User = get_user_model()

        # Determine language from order (set at checkout) or checkout request metadata
        if checkout_request.order:
            from email_system.utils.language import get_order_email_language
            language = get_order_email_language(checkout_request.order)
        else:
            language = (checkout_request.metadata or {}).get('language', 'en')

        # Generate activation URL for guest users
        activation_url = ''
        user = User.objects.filter(email__iexact=checkout_request.email).first()
        if user and user.username.startswith('guest_'):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            locale_prefix = f"/{language}" if language != 'en' else ''
            activation_url = f"https://spwig.com{locale_prefix}/account/activate-guest/{uid}/{token}/"

        outbox = EmailSendingService.send_template_email(
            to_email=checkout_request.email,
            template_type='license_purchase_confirmation',
            context={
                'customer_name': checkout_request.name or 'there',
                'product_name': checkout_request.license_product.name,
                'price': str(checkout_request.license_product.price),
                'license_key': checkout_request.license_key,
                'setup_token': checkout_request.setup_token,
                'setup_url': f"https://docs.spwig.com/getting-started/",
                'includes_pos': checkout_request.license_product.includes_pos,
                'order_number': checkout_request.order.order_number if checkout_request.order else '',
                'activation_url': activation_url,
            },
            language=language,
        )
        if outbox and outbox.status == 'queued':
            EmailSendingService.send_email(str(outbox.id))
            logger.info(f"Sent purchase confirmation email to {_mask_email(checkout_request.email)}")
        elif outbox and outbox.status == 'skipped':
            logger.info(f"Purchase confirmation email skipped for {_mask_email(checkout_request.email)}: {outbox.skip_reason}")
    except Exception as e:
        logger.error(f"Failed to send purchase confirmation email to {_mask_email(checkout_request.email)}: {e}")


# ── Hosted Subscription Provisioning ─────────────────────────────────────


def _build_confirmation_context(checkout, plan, subscription, next_billing):
    """Build email context for subscription confirmation, including intro pricing."""
    from decimal import Decimal

    ctx = {
        'name': checkout.name,
        'store_name': checkout.store_name,
        'plan_name': plan.name,
        'billing_interval': checkout.billing_interval,
        'amount': str(subscription.billing_amount),
        'currency': 'EUR',
        'next_billing_date': next_billing.strftime('%d %B %Y'),
        'intro_period': '',
        'full_amount': '',
    }

    # Add intro pricing details if applicable
    addon = Decimal('29.00') if checkout.pos_addon and not plan.includes_pos else Decimal('0')
    if checkout.billing_interval == 'monthly' and plan.has_monthly_intro:
        ctx['intro_period'] = f"{plan.intro_monthly_discount_cycles} months"
        ctx['full_amount'] = str(plan.monthly_price.amount + addon)
    elif checkout.billing_interval == 'annual' and plan.has_annual_intro:
        cycles = plan.intro_annual_discount_cycles
        ctx['intro_period'] = f"{cycles} year{'s' if cycles != 1 else ''}"
        ctx['full_amount'] = str(plan.annual_price.amount * 12 + addon * 12)

    return ctx


def provision_hosted_subscription(order):
    """
    Called after payment succeeds for a hosted plan checkout.

    Creates the HostedSubscription, posts subscription.created to the
    update server, triggers instance provisioning, and sends the
    subscription confirmation email.
    """
    from datetime import timedelta as td
    from django.utils import timezone as tz
    from dateutil.relativedelta import relativedelta
    from license_checkout.models import (
        HostedCheckoutRequest, HostedSubscription, HostedPlan,
    )

    checkout_id = order.metadata.get('hosted_checkout_request_id')
    if not checkout_id:
        logger.error('provision_hosted_subscription: missing hosted_checkout_request_id in order metadata')
        return

    # Idempotency: skip if subscription already exists for this checkout
    if HostedCheckoutRequest.objects.filter(
        id=checkout_id,
        subscription__isnull=False,
    ).exists():
        logger.info('provision_hosted_subscription: already provisioned for checkout %s', checkout_id)
        return

    try:
        checkout = HostedCheckoutRequest.objects.select_related('hosted_plan').get(id=checkout_id)
    except HostedCheckoutRequest.DoesNotExist:
        logger.error('provision_hosted_subscription: HostedCheckoutRequest %s not found', checkout_id)
        return

    plan = checkout.hosted_plan
    now = tz.now()

    # Calculate billing period
    if checkout.billing_interval == 'annual':
        period_end = now + relativedelta(years=1)
        next_billing = period_end
    else:
        period_end = now + relativedelta(months=1)
        next_billing = period_end

    # Resolve the payment provider account and user from the order
    from payment_providers.models import PaymentProviderAccount
    payment_provider = None
    if order.payment_provider_id:
        payment_provider = order.payment_provider
    else:
        payment_provider = PaymentProviderAccount.objects.filter(
            is_active=True, connection_status='connected',
        ).first()

    user = order.user if hasattr(order, 'user') and order.user_id else None

    # Create the subscription record
    subscription = HostedSubscription.objects.create(
        hosted_plan=plan,
        billing_interval=checkout.billing_interval,
        email=checkout.email,
        name=checkout.name,
        company=checkout.company,
        user=user,
        store_name=checkout.store_name,
        store_slug=checkout.store_slug,
        region=checkout.region,
        pos_addon=checkout.pos_addon,
        payment_provider_account=payment_provider,
        status=HostedSubscription.Status.PENDING,
        current_period_start=now,
        current_period_end=period_end,
        next_billing_date=next_billing,
        billing_cycle_count=1,
        last_billing_date=now,
        last_billing_status='successful',
        airwallex_customer_id=checkout.metadata.get('airwallex_customer_id', ''),
    )

    # Link subscription to checkout request
    checkout.subscription = subscription
    checkout.status = HostedCheckoutRequest.Status.PROVISIONING
    checkout.order = order
    checkout.save(update_fields=['subscription', 'status', 'order', 'updated_at'])

    logger.info(
        'Created HostedSubscription %s for %s (%s %s)',
        subscription.id, checkout.store_slug, plan.slug, checkout.billing_interval,
    )

    # Save Airwallex payment consent for recurring billing
    # The consent ID comes from the payment intent metadata after card tokenisation
    try:
        if checkout.payment_intent:
            intent_meta = checkout.payment_intent.metadata or {}
            consent_id = intent_meta.get('consent_id', '')
            if consent_id:
                subscription.airwallex_consent_id = consent_id
                subscription.save(update_fields=['airwallex_consent_id'])
    except Exception as e:
        logger.warning('Could not save payment consent for %s: %s', checkout.store_slug, e)

    # Trigger provisioning on the update server.
    # The update server's POST /api/v1/hosting/provision/ endpoint:
    # 1. Validates the license exists
    # 2. Creates a HostedInstance record
    # 3. Dispatches the async provisioning task
    # 4. On completion, posts provision_complete back to our /api/hosting-events/
    #
    # The license must already exist. We use the existing license provisioning
    # system (via _provision_license_on_server) to create it first.
    import secrets
    import httpx
    import time

    upgrade_server_url = getattr(settings, 'UPGRADE_SERVER_URL', '')
    internal_api_key = getattr(settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')

    if not upgrade_server_url:
        logger.error('UPGRADE_SERVER_URL not configured — cannot provision hosted instance')
        _mark_checkout_failed(checkout, 'Internal configuration error during provisioning')
        return

    api_headers = {
        'X-API-KEY': internal_api_key,
        'Content-Type': 'application/json',
    }

    # Step 1: Create a hosted license on the update server
    license_key = None
    license_response = _http_post_with_retry(
        f"{upgrade_server_url.rstrip('/')}/api/v1/internal/licenses/",
        json_data={
            'owner_name': checkout.name or checkout.email.split('@')[0],
            'owner_email': checkout.email,
            'company': checkout.company or '',
            'country': str(checkout.billing_country) if checkout.billing_country else '',
            'license_type': 'production',
            'hosting_type': 'spwig_hosted',
            'product_type': 'shop',
            'plan_slug': plan.slug,
            'max_installations': 1,
            'allowed_channels': ['stable'],
        },
        headers=api_headers,
    )

    if license_response is None:
        logger.error('Failed to create hosted license for %s after retries', checkout.store_slug)
        _mark_checkout_failed(checkout, 'Could not connect to provisioning server')
        return

    if license_response.status_code in (200, 201):
        license_data = license_response.json()
        license_key = license_data.get('license_key', '')
        subscription.license_key = license_key
        subscription.save(update_fields=['license_key'])
        logger.info('Created hosted license %s for %s', license_key, checkout.store_slug)
    else:
        logger.error(
            'Failed to create hosted license: %s %s',
            license_response.status_code, license_response.text[:200],
        )
        _mark_checkout_failed(checkout, 'License creation failed during provisioning')
        return

    # Step 1b: Create a setup token for auto-activation during first boot.
    # The docker entrypoint reads SETUP_TOKEN and calls activate_with_token
    # to register the installation, write license.json, and create the admin user.
    setup_token_jwt = ''
    try:
        token_payload = {
            'license_key': license_key,
            'email': checkout.email,
            'owner_name': checkout.name or checkout.email.split('@')[0],
            'company_name': checkout.company or '',
            'site_name': checkout.store_name or '',
            'domain': f'{checkout.store_slug}.myspwig.com',
        }
        token_resp = _http_post_with_retry(
            f"{upgrade_server_url.rstrip('/')}/api/v1/setup-tokens/",
            json_data=token_payload,
            headers=api_headers,
        )
        if token_resp and token_resp.status_code == 201:
            token_data = token_resp.json()
            setup_token_jwt = token_data.get('token', '')
            logger.info('Created setup token for %s (id=%s)', checkout.store_slug, token_data.get('token_id'))
        else:
            status_code = token_resp.status_code if token_resp else 'no response'
            logger.warning(
                'Setup token creation failed for %s: %s — merchant will need manual activation',
                checkout.store_slug, status_code,
            )
    except Exception as e:
        logger.warning('Setup token creation failed for %s: %s — continuing without token', checkout.store_slug, e)

    # Step 2: Trigger instance provisioning
    # Use the merchant's chosen password hash from checkout, or generate one as fallback
    admin_password_hash = checkout.metadata.get('admin_password_hash', '')
    if not admin_password_hash:
        from django.contrib.auth.hashers import make_password
        admin_password_hash = make_password(secrets.token_urlsafe(16))
        logger.warning('No admin_password_hash in checkout metadata — using auto-generated password')

    provision_response = _http_post_with_retry(
        f"{upgrade_server_url.rstrip('/')}/api/v1/hosting/provision/",
        json_data={
            'store_slug': checkout.store_slug,
            'store_name': checkout.store_name,
            'license_key': license_key,
            'plan_slug': plan.slug,
            'region': checkout.region,
            'admin_email': checkout.email,
            'admin_password_hash': admin_password_hash,
            'spwig_version': getattr(settings, 'SPWIG_VERSION', 'latest'),
            'setup_token_jwt': setup_token_jwt,
        },
        headers=api_headers,
    )

    if provision_response is None:
        logger.error('Failed to trigger provisioning for %s after retries', checkout.store_slug)
        _mark_checkout_failed(checkout, 'Could not connect to provisioning server')
        return

    if provision_response.status_code in (200, 201, 202):
        logger.info(
            'Provisioning triggered for %s (license=%s)',
            checkout.store_slug, license_key,
        )
    else:
        logger.error(
            'Failed to trigger provisioning for %s: %s %s',
            checkout.store_slug, provision_response.status_code,
            provision_response.text[:200],
        )
        _mark_checkout_failed(checkout, 'Store provisioning could not be started')
        return

    # Send subscription confirmation email
    _send_hosting_email(
        to_email=checkout.email,
        template_type='hosted_subscription_confirmation',
        context=_build_confirmation_context(checkout, plan, subscription, next_billing),
        label='subscription confirmation',
    )

    logger.info(
        'Hosted subscription provisioning initiated for %s (plan=%s)',
        checkout.store_slug, plan.slug,
    )


def _http_post_with_retry(url, json_data, headers, timeout=30, max_retries=2):
    """POST with simple retry for transient failures.

    Returns the response on success, or None if all retries failed.
    Non-transient errors (4xx) are returned immediately without retry.
    """
    import time
    import httpx

    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            response = httpx.post(url, json=json_data, headers=headers, timeout=timeout)
            # Don't retry client errors (4xx) — they won't succeed on retry
            if response.status_code < 500:
                return response
            # Server error — retry
            logger.warning(
                'HTTP %d from %s (attempt %d/%d)',
                response.status_code, url, attempt + 1, max_retries + 1,
            )
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # 1s, 2s
                continue
            return response
        except (httpx.RequestError, httpx.TimeoutException) as e:
            last_exc = e
            logger.warning(
                'HTTP request to %s failed (attempt %d/%d): %s',
                url, attempt + 1, max_retries + 1, e,
            )
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    logger.error('HTTP POST to %s failed after %d attempts: %s', url, max_retries + 1, last_exc)
    return None


def _mark_checkout_failed(checkout, error_message):
    """Mark a hosted checkout as failed and notify the merchant."""
    from .models import HostedCheckoutRequest

    checkout.status = HostedCheckoutRequest.Status.FAILED
    checkout.error_message = error_message
    checkout.save(update_fields=['status', 'error_message', 'updated_at'])

    _send_hosting_email(
        to_email=checkout.email,
        template_type='hosted_provision_failed',
        context={
            'name': checkout.name or checkout.email.split('@')[0],
            'store_name': checkout.store_name,
            'store_slug': checkout.store_slug,
            'provision_error': (
                'We encountered an issue while setting up your store. '
                'Our team has been notified and will resolve this shortly. '
                'If you need immediate assistance, please contact support@spwig.com.'
            ),
        },
        label='provision failed (HQ-side)',
    )
    logger.error(
        'Hosted checkout %s marked as FAILED: %s',
        checkout.store_slug, error_message,
    )


def notify_update_server_subscription(event_type, data):
    """
    Post a subscription lifecycle event to the update server's webhook.

    Events: subscription.created, subscription.updated,
            subscription.cancelled, subscription.plan_changed
    """
    import hashlib
    import hmac as hmac_module
    import httpx

    webhook_url = getattr(settings, 'UPGRADE_SERVER_URL', '')
    if not webhook_url:
        logger.warning('UPGRADE_SERVER_URL not configured — skipping subscription webhook')
        return

    webhook_secret = getattr(settings, 'SUBSCRIPTION_WEBHOOK_SECRET', '')
    if not webhook_secret:
        logger.warning('SUBSCRIPTION_WEBHOOK_SECRET not configured — skipping subscription webhook')
        return

    url = f"{webhook_url.rstrip('/')}/api/v1/subscriptions/webhook/"
    payload = {
        'event': event_type,
        **data,
    }

    import json
    body = json.dumps(payload, sort_keys=True)
    signature = hmac_module.new(
        webhook_secret.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()

    try:
        response = httpx.post(
            url,
            content=body,
            headers={
                'Content-Type': 'application/json',
                'X-Webhook-Signature': signature,
            },
            timeout=30,
        )
        if response.status_code not in (200, 201):
            logger.error(
                'Update server subscription webhook returned %s: %s',
                response.status_code, response.text[:200],
            )
        else:
            logger.info(
                'Posted %s to update server for %s',
                event_type, data.get('store_slug', data.get('license_key', '?')),
            )
    except Exception as e:
        logger.error('Failed to post %s to update server: %s', event_type, e)


# ── Hosted Provisioning Event Handlers ───────────────────────────────────

HOSTING_SUPPORT_EMAIL = 'support@spwig.com'


def handle_hosting_event(event_type, payload):
    """Route hosting provisioning events to the appropriate handler.

    Called by HostingEventWebhookView when the update server posts a
    provisioning lifecycle event.
    """
    handlers = {
        'provision_complete': _handle_provision_complete,
        'provision_failed': _handle_provision_failed,
    }
    handler = handlers.get(event_type)
    if not handler:
        logger.warning('Unknown hosting event type: %s', event_type)
        return False

    return handler(payload)


def _validate_hosting_email(admin_email):
    """Validate admin_email from hosting event payload."""
    from django.core.exceptions import ValidationError as DjangoValidationError
    from django.core.validators import validate_email as django_validate_email

    if not admin_email:
        return False
    try:
        django_validate_email(admin_email)
        return True
    except DjangoValidationError:
        logger.error('Invalid admin_email in hosting event: %s', _mask_email(admin_email))
        return False


def _handle_provision_complete(payload):
    """Send provisioning-complete email and schedule onboarding tips for 24h later."""
    admin_email = payload.get('admin_email', '')
    store_name = payload.get('store_name', '')

    if not _validate_hosting_email(admin_email):
        logger.error('provision_complete event: missing or invalid admin_email')
        return False

    # Look up merchant name from the checkout request (payload doesn't include it)
    merchant_name = payload.get('name', '')
    checkout = None
    try:
        from license_checkout.models import HostedCheckoutRequest, HostedSubscription
        checkout = HostedCheckoutRequest.objects.filter(
            store_slug=payload.get('store_slug', ''),
            status=HostedCheckoutRequest.Status.PROVISIONING,
        ).select_related('subscription').first()
        if checkout and not merchant_name:
            merchant_name = checkout.name
    except Exception as e:
        logger.warning('Could not look up HostedCheckoutRequest for name: %s', e)

    # 1. Send immediate "your store is ready" email
    _send_hosting_email(
        to_email=admin_email,
        template_type='hosted_provision_complete',
        context={
            'name': merchant_name,
            'store_name': store_name,
            'store_url': payload.get('store_url', ''),
            'admin_url': payload.get('admin_url', ''),
            'subdomain': payload.get('subdomain', ''),
            'region': payload.get('region', ''),
        },
        label='provision complete',
    )

    # 2. Schedule onboarding email sequence (with duplicate guard)
    from datetime import timedelta as td
    from django.utils import timezone as tz
    from email_system.models import ScheduledEmail

    # Skip if onboarding was already scheduled (duplicate provision_complete event)
    already_scheduled = ScheduledEmail.objects.filter(
        template_type__startswith='hosted_onboarding',
        recipient_email=admin_email,
    ).exists()
    if already_scheduled:
        logger.info('Onboarding emails already scheduled for %s — skipping', _mask_email(admin_email))
    else:
        onboarding_context = {
            'name': merchant_name,
            'store_name': store_name,
            'store_url': payload.get('store_url', ''),
            'admin_url': payload.get('admin_url', ''),
        }

        onboarding_schedule = [
            ('hosted_onboarding_tips', td(hours=24), 'Day 1 tips'),
            ('hosted_onboarding_day3', td(days=3), 'Day 3 products'),
            ('hosted_onboarding_day7', td(days=7), 'Day 7 marketing'),
            ('hosted_onboarding_day14', td(days=14), 'Day 14 advanced'),
        ]

        now = tz.now()
        for template_type, delay, label in onboarding_schedule:
            ScheduledEmail.objects.create(
                template_type=template_type,
                recipient_email=admin_email,
                context_json=onboarding_context,
                scheduled_for=now + delay,
            )
        logger.info(
            'Scheduled 4 onboarding emails for %s (Day 1/3/7/14)',
            _mask_email(admin_email),
        )

    # 3. Update HostedCheckoutRequest if one exists for this store
    if checkout:
        try:
            from license_checkout.models import HostedCheckoutRequest, HostedSubscription
            checkout.status = HostedCheckoutRequest.Status.COMPLETED
            checkout.metadata['store_url'] = payload.get('store_url', '')
            checkout.metadata['admin_url'] = payload.get('admin_url', '')
            checkout.save(update_fields=['status', 'metadata', 'updated_at'])
            logger.info('Updated HostedCheckoutRequest %s → completed', checkout.id)

            # Transition subscription from PENDING to ACTIVE now that store is live
            if checkout.subscription and checkout.subscription.status == HostedSubscription.Status.PENDING:
                checkout.subscription.status = HostedSubscription.Status.ACTIVE
                checkout.subscription.save(update_fields=['status', 'updated_at'])
                logger.info('HostedSubscription %s → ACTIVE (provision complete)', checkout.subscription.id)
        except Exception as e:
            logger.warning('Could not update HostedCheckoutRequest: %s', e)

    return True


def _handle_provision_failed(payload):
    """Send failure notification to merchant AND separate email to support."""
    admin_email = payload.get('admin_email', '')
    store_name = payload.get('store_name', '')
    provision_error = payload.get('provision_error', 'An unexpected error occurred')

    if not _validate_hosting_email(admin_email):
        logger.error('provision_failed event: missing or invalid admin_email')
        return False

    # Look up merchant name from the checkout request (payload doesn't include it)
    merchant_name = payload.get('name', '')
    if not merchant_name:
        try:
            from license_checkout.models import HostedCheckoutRequest
            failed_checkout = HostedCheckoutRequest.objects.filter(
                store_slug=payload.get('store_slug', ''),
                status=HostedCheckoutRequest.Status.PROVISIONING,
            ).first()
            if failed_checkout:
                merchant_name = failed_checkout.name
        except Exception as e:
            logger.warning('Could not look up HostedCheckoutRequest for name: %s', e)

    # Merchant sees a generic message; support sees the raw error
    merchant_error = (
        'We encountered a technical issue while setting up your store. '
        'Our team has been notified and will resolve this as soon as possible.'
    )

    merchant_context = {
        'name': merchant_name,
        'store_name': store_name,
        'store_slug': payload.get('store_slug', ''),
        'provision_error': merchant_error,
        'infra_tier': payload.get('infra_tier', ''),
        'region': payload.get('region', ''),
    }

    support_context = {
        'store_name': store_name,
        'store_slug': payload.get('store_slug', ''),
        'provision_error': provision_error,
        'infra_tier': payload.get('infra_tier', ''),
        'region': payload.get('region', ''),
        'admin_email': admin_email,
    }

    # 1. Email the merchant (generic error)
    _send_hosting_email(
        to_email=admin_email,
        template_type='hosted_provision_failed',
        context=merchant_context,
        label='provision failed (merchant)',
    )

    # 2. Separate email to support@spwig.com (full error details)
    _send_hosting_email(
        to_email=HOSTING_SUPPORT_EMAIL,
        template_type='hosted_provision_failed',
        context=support_context,
        label='provision failed (support)',
    )

    # 3. Update HostedCheckoutRequest and HostedSubscription
    try:
        from license_checkout.models import HostedCheckoutRequest, HostedSubscription
        checkout = HostedCheckoutRequest.objects.filter(
            store_slug=payload.get('store_slug', ''),
            status=HostedCheckoutRequest.Status.PROVISIONING,
        ).select_related('subscription').first()
        if checkout:
            checkout.status = HostedCheckoutRequest.Status.FAILED
            checkout.error_message = merchant_error
            checkout.save(update_fields=['status', 'error_message', 'updated_at'])
            logger.info('Updated HostedCheckoutRequest %s → failed', checkout.id)

            # Record the error on the subscription (it's in PENDING state at this point)
            if checkout.subscription:
                checkout.subscription.error_message = merchant_error
                checkout.subscription.save(update_fields=['error_message', 'updated_at'])
                logger.info('Updated HostedSubscription %s → pending (provision failed)', checkout.subscription.id)
    except Exception as e:
        logger.warning('Could not update HostedCheckoutRequest/Subscription: %s', e)

    return True


def _send_hosting_email(to_email, template_type, context, label=''):
    """Send a single hosting-related email via EmailSendingService."""
    try:
        from email_system.services.email_sender import EmailSendingService

        outbox = EmailSendingService.send_template_email(
            to_email=to_email,
            template_type=template_type,
            context=context,
        )
        if outbox and outbox.status == 'queued':
            EmailSendingService.send_email(str(outbox.id))
            logger.info('Sent %s email to %s', label, _mask_email(to_email))
        elif outbox and outbox.status == 'skipped':
            logger.info('%s email skipped for %s: %s', label, _mask_email(to_email), outbox.skip_reason)
        elif not outbox:
            logger.critical(
                'CRITICAL: %s email returned no outbox for %s — template may be missing',
                label, _mask_email(to_email),
            )
    except Exception as e:
        logger.critical(
            'CRITICAL: Failed to send %s email to %s: %s',
            label, _mask_email(to_email), e, exc_info=True,
        )
