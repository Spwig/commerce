"""
HQ-only REST API views for the Spwig merchant account portal.

These views power the spwig.com/account Next.js frontend, providing
hosted subscription management, self-hosted license info, and dashboard
data. Only loaded when SPWIG_IS_HQ=True.

Business logic is ported from accounts/views_hosting.py (template views)
and reuses existing service helpers — not duplicated.
"""
import logging
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from license_checkout.models import (
    HostedBillingLog,
    HostedSubscription,
    LicenseCheckoutRequest,
)
from .serializers_hq import (
    CancelSubscriptionSerializer,
    DashboardSerializer,
    HostedBillingLogSerializer,
    HostedSubscriptionSerializer,
    HostedSubscriptionListSerializer,
    IntervalChangeDetailSerializer,
    GhostActivationSerializer,
    LicenseDetailSerializer,
    LicenseListItemSerializer,
    MaintenanceStatusSerializer,
    PaymentConfigSerializer,
    UpdatePaymentSerializer,
)

logger = logging.getLogger(__name__)

HQ_AUTH = [TokenAuthentication, SessionAuthentication]


# ── Helpers ────────────────────────────────────────────────────────────

_VISIBLE_STATUSES = [
    HostedSubscription.Status.ACTIVE,
    HostedSubscription.Status.PAST_DUE,
    HostedSubscription.Status.SUSPENDED,
    HostedSubscription.Status.CANCELLED,
    HostedSubscription.Status.PENDING,
]


def _get_all_subscriptions(user):
    """Get all visible hosted subscriptions for the user."""
    return HostedSubscription.objects.select_related('hosted_plan').filter(
        user=user,
        status__in=_VISIBLE_STATUSES,
    ).order_by('-created_at')


def _get_subscription_by_id_or_404(user, subscription_id):
    """Get a specific subscription by UUID, ensuring it belongs to the user."""
    try:
        sub = HostedSubscription.objects.select_related('hosted_plan').get(
            id=subscription_id,
            user=user,
            status__in=_VISIBLE_STATUSES,
        )
        return sub, None
    except HostedSubscription.DoesNotExist:
        return None, Response(
            {'success': False, 'error': 'Subscription not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )


def _resolve_subscription(user, subscription_id=None):
    """Resolve to a specific subscription, or fall back to first."""
    if subscription_id:
        return _get_subscription_by_id_or_404(user, subscription_id)
    sub = _get_all_subscriptions(user).first()
    if not sub:
        return None, Response(
            {'success': False, 'error': 'No active subscription found.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return sub, None


def _get_all_license_keys(user):
    """Get all license keys for the user from both self-hosted and hosted sources."""
    licenses = []

    # Self-hosted licenses from LicenseCheckoutRequest
    checkout_requests = LicenseCheckoutRequest.objects.filter(
        email__iexact=user.email, status='completed',
    ).select_related('license_product')
    for lcr in checkout_requests:
        if lcr.license_key:
            data = _fetch_license_from_update_server(lcr.license_key)
            if data:
                data['source'] = 'self_hosted'
                data['subscription_id'] = None
                data['store_name'] = ''
                licenses.append(data)

    # Hosted subscription licenses
    hosted_subs = HostedSubscription.objects.filter(
        user=user,
        status__in=_VISIBLE_STATUSES,
    ).exclude(license_key='').select_related('hosted_plan')
    for sub in hosted_subs:
        data = _fetch_license_from_update_server(sub.license_key)
        if data:
            data['source'] = 'hosted'
            data['subscription_id'] = str(sub.id)
            data['store_name'] = sub.store_name
            licenses.append(data)

    return licenses


def _resolve_first_license_key(user):
    """Get the first available license key from self-hosted or hosted sources."""
    lcr = LicenseCheckoutRequest.objects.filter(
        email__iexact=user.email, status='completed',
    ).first()
    if lcr and lcr.license_key:
        return lcr.license_key

    sub = HostedSubscription.objects.filter(
        user=user, status__in=_VISIBLE_STATUSES,
    ).exclude(license_key='').first()
    if sub:
        return sub.license_key

    return None


def _get_provider():
    """Get active payment provider account and provider instance."""
    from payment_providers.models import PaymentProviderAccount
    from subscriptions.provider_base import get_provider

    provider_account = PaymentProviderAccount.objects.filter(
        is_active=True, connection_status='connected',
    ).first()

    if not provider_account:
        return None, None

    return provider_account, get_provider(provider_account)


# ── Dashboard ──────────────────────────────────────────────────────────

@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def account_dashboard(request):
    """Account overview — subscription summary, license summary, account type."""
    user = request.user

    # All subscriptions
    subscriptions = _get_all_subscriptions(user)
    first_subscription = subscriptions.first()

    # All licenses (self-hosted + hosted)
    all_licenses = _get_all_license_keys(user)
    first_license = all_licenses[0] if all_licenses else None

    # Determine account type
    has_hosted = subscriptions.exists()
    has_license = len(all_licenses) > 0
    if has_hosted and has_license:
        account_type = 'both'
    elif has_hosted:
        account_type = 'hosted'
    elif has_license:
        account_type = 'self_hosted'
    else:
        account_type = 'none'

    data = {
        'account_type': account_type,
        # Backward compat — singular (first item)
        'hosted_subscription': first_subscription,
        'license_summary': first_license,
        # New plural fields
        'hosted_subscriptions': subscriptions,
        'licenses': all_licenses,
        'subscription_count': subscriptions.count(),
        'license_count': len(all_licenses),
        '_user': user,
    }
    serializer = DashboardSerializer(data)
    return Response({'success': True, 'data': serializer.data})


# ── Hosting Subscription Detail ────────────────────────────────────────

@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_subscription_detail(request, subscription_id=None):
    """Subscription detail with actions."""
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    serializer = HostedSubscriptionSerializer(subscription)
    return Response({'success': True, 'data': serializer.data})


# ── Billing History ────────────────────────────────────────────────────

@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_billing_history(request, subscription_id=None):
    """Paginated billing history for the user's subscription."""
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    page = int(request.query_params.get('page', 1))
    page_size = min(int(request.query_params.get('page_size', 20)), 100)
    offset = (page - 1) * page_size

    logs = HostedBillingLog.objects.filter(
        subscription=subscription,
    ).order_by('-billing_date')

    total = logs.count()
    page_logs = logs[offset:offset + page_size]

    serializer = HostedBillingLogSerializer(page_logs, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size if page_size else 1,
        },
    })


# ── Cancel ─────────────────────────────────────────────────────────────

@api_view(['POST'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_cancel(request, subscription_id=None):
    """Cancel hosted subscription (end of billing period)."""
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    if subscription.status not in (
        HostedSubscription.Status.ACTIVE,
        HostedSubscription.Status.PAST_DUE,
        HostedSubscription.Status.SUSPENDED,
    ):
        return Response(
            {'success': False, 'error': 'This subscription cannot be cancelled.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = CancelSubscriptionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    reason = serializer.validated_data.get('reason', '')

    access_until = subscription.current_period_end
    termination_date = (
        access_until + timedelta(days=30)
        if access_until
        else timezone.now() + timedelta(days=30)
    )

    now = timezone.now()
    subscription.cancellation_type = HostedSubscription.CancellationType.END_OF_PERIOD
    subscription.cancelled_at = now
    subscription.cancellation_reason = reason
    subscription.termination_scheduled_at = termination_date
    subscription.status = HostedSubscription.Status.CANCELLED
    subscription.save(update_fields=[
        'cancellation_type', 'cancelled_at', 'cancellation_reason',
        'termination_scheduled_at', 'status', 'updated_at',
    ])

    # Email + update server notification
    from license_checkout.services import _send_hosting_email, notify_update_server_subscription
    _send_hosting_email(
        to_email=subscription.email,
        template_type='hosted_cancellation_confirmation',
        context={
            'store_name': subscription.store_name,
            'plan_name': subscription.hosted_plan.name,
            'access_until_date': access_until.strftime('%d %B %Y') if access_until else '',
            'termination_date': termination_date.strftime('%d %B %Y'),
        },
        label='cancellation (API)',
    )

    try:
        notify_update_server_subscription(
            event_type='subscription.cancelled',
            data={
                'license_key': subscription.license_key,
                'access_until': access_until.isoformat() if access_until else '',
            },
        )
    except Exception as e:
        logger.error('Failed to notify update server of cancellation: %s', e)

    # Cancel pending onboarding emails
    try:
        from email_system.models import ScheduledEmail
        ScheduledEmail.objects.filter(
            recipient_email=subscription.email,
            status='pending',
            template_type__startswith='hosted_onboarding',
        ).update(status='cancelled')
    except Exception:
        pass

    return Response({
        'success': True,
        'message': 'Subscription cancelled.',
        'data': {
            'access_until': access_until.isoformat() if access_until else None,
            'termination_date': termination_date.isoformat(),
        },
    })


# ── Undo Cancel ────────────────────────────────────────────────────────

@api_view(['POST'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_undo_cancel(request, subscription_id=None):
    """Reverse a cancellation before the paid period ends."""
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    now = timezone.now()

    if subscription.status != HostedSubscription.Status.CANCELLED:
        return Response(
            {'success': False, 'error': 'This subscription is not cancelled.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not subscription.current_period_end or subscription.current_period_end <= now:
        return Response(
            {'success': False, 'error': 'Your paid period has ended. Please reactivate instead.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    subscription.cancellation_type = HostedSubscription.CancellationType.NONE
    subscription.cancelled_at = None
    subscription.cancellation_reason = ''
    subscription.termination_scheduled_at = None
    subscription.status = HostedSubscription.Status.ACTIVE
    subscription.save(update_fields=[
        'cancellation_type', 'cancelled_at', 'cancellation_reason',
        'termination_scheduled_at', 'status', 'updated_at',
    ])

    from license_checkout.services import notify_update_server_subscription, _send_hosting_email
    try:
        notify_update_server_subscription(
            event_type='subscription.updated',
            data={
                'license_key': subscription.license_key,
                'account_status': 'active',
            },
        )
    except Exception as e:
        logger.error('Failed to notify update server of reversal: %s', e)

    _send_hosting_email(
        to_email=subscription.email,
        template_type='hosted_cancellation_reversed',
        context={
            'store_name': subscription.store_name,
            'plan_name': subscription.hosted_plan.name,
            'next_billing_date': (
                subscription.next_billing_date.strftime('%d %B %Y')
                if subscription.next_billing_date else ''
            ),
        },
        label='cancellation reversed (API)',
    )

    return Response({
        'success': True,
        'message': 'Cancellation reversed. Your subscription will continue as normal.',
    })


# ── Reactivate ─────────────────────────────────────────────────────────

@api_view(['POST'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_reactivate(request, subscription_id=None):
    """Reactivate a suspended or cancelled subscription (charges immediately)."""
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    if subscription.status not in (
        HostedSubscription.Status.SUSPENDED,
        HostedSubscription.Status.CANCELLED,
    ):
        return Response(
            {'success': False, 'error': 'This subscription does not need reactivation.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    amount = subscription.billing_amount
    now = timezone.now()

    billing_log = HostedBillingLog.objects.create(
        subscription=subscription,
        cycle_number=subscription.billing_cycle_count + 1,
        billing_date=now,
        amount=amount,
        status=HostedBillingLog.Status.PROCESSING,
    )

    from license_checkout.tasks import _charge_subscription
    success = _charge_subscription(subscription, amount, billing_log)

    if not success:
        return Response(
            {'success': False, 'error': 'Payment failed. Please update your payment method first.'},
            status=status.HTTP_402_PAYMENT_REQUIRED,
        )

    # Payment succeeded — reactivate
    from dateutil.relativedelta import relativedelta

    if subscription.billing_interval == 'annual':
        period_end = now + relativedelta(years=1)
    else:
        period_end = now + relativedelta(months=1)

    subscription.status = HostedSubscription.Status.ACTIVE
    subscription.cancellation_type = HostedSubscription.CancellationType.NONE
    subscription.cancelled_at = None
    subscription.cancellation_reason = ''
    subscription.termination_scheduled_at = None
    subscription.grace_period_end_date = None
    subscription.retry_count = 0
    subscription.current_period_start = now
    subscription.current_period_end = period_end
    subscription.next_billing_date = period_end
    subscription.billing_cycle_count += 1
    subscription.last_billing_date = now
    subscription.last_billing_status = 'successful'
    subscription.save()

    billing_log.status = HostedBillingLog.Status.SUCCESSFUL
    billing_log.save(update_fields=['status'])

    from license_checkout.services import notify_update_server_subscription, _send_hosting_email
    try:
        notify_update_server_subscription(
            event_type='subscription.updated',
            data={
                'license_key': subscription.license_key,
                'account_status': 'active',
            },
        )
    except Exception as e:
        logger.error('Failed to notify update server of reactivation: %s', e)

    _send_hosting_email(
        to_email=subscription.email,
        template_type='hosted_reactivation_confirmed',
        context={
            'store_name': subscription.store_name,
            'plan_name': subscription.hosted_plan.name,
            'amount': str(amount),
            'currency': 'EUR',
            'next_billing_date': period_end.strftime('%d %B %Y'),
            'store_url': f'https://{subscription.store_slug}.myspwig.com',
            'admin_url': f'https://{subscription.store_slug}.myspwig.com/en/admin/',
        },
        label='reactivation confirmed (API)',
    )

    return Response({
        'success': True,
        'message': 'Subscription reactivated successfully.',
        'data': {
            'next_billing_date': period_end.isoformat(),
            'amount_charged': str(amount),
        },
    })


# ── Update Payment Method ──────────────────────────────────────────────

@api_view(['GET', 'POST'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_update_payment(request, subscription_id=None):
    """
    GET: Return Airwallex payment config for the card capture form.
    POST: Process payment method update after Airwallex card capture.
    """
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    if subscription.status == HostedSubscription.Status.CANCELLED:
        return Response(
            {'success': False, 'error': 'Please reactivate your subscription first.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == 'GET':
        return _update_payment_get(subscription)

    return _update_payment_post(request, subscription)


def _update_payment_get(subscription):
    """Create verification intent and return payment config."""
    provider_account, sub_provider = _get_provider()
    if not provider_account:
        return Response(
            {'success': False, 'error': 'Payment system is currently unavailable.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    try:
        intent = sub_provider.create_payment_intent_for_verification(
            amount=Decimal('0.50'),
            currency='EUR',
            customer_id=subscription.airwallex_customer_id or None,
            metadata={
                'purpose': 'payment_method_update',
                'store_slug': subscription.store_slug,
            },
        )
        payment_config = {
            'client_secret': intent.get('client_secret', ''),
            'intent_id': intent.get('id', ''),
            'provider_slug': (
                provider_account.component.slug
                if provider_account.component else ''
            ),
            'env': 'demo' if provider_account.test_mode else 'prod',
        }
        serializer = PaymentConfigSerializer(payment_config)
        return Response({'success': True, 'data': serializer.data})
    except Exception as e:
        logger.error('Failed to create verification intent for %s: %s', subscription.store_slug, e)
        return Response(
            {'success': False, 'error': 'Could not initialize payment form. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _update_payment_post(request, subscription):
    """Process payment method update after Airwallex card capture."""
    serializer = UpdatePaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    payment_intent_id = serializer.validated_data['payment_intent_id']

    provider_account, sub_provider = _get_provider()
    if not provider_account:
        return Response(
            {'success': False, 'error': 'Payment system is currently unavailable.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    try:
        # Get payment intent to extract payment method
        intent_details = sub_provider.get_payment_intent(payment_intent_id)
        payment_method_id = (
            intent_details.get('latest_payment_attempt', {})
            .get('payment_method', {})
            .get('id', '')
        )

        if not payment_method_id:
            return Response(
                {'success': False, 'error': 'Could not retrieve payment method.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create or get Airwallex customer
        customer_id = subscription.airwallex_customer_id
        if not customer_id:
            customer_result = sub_provider.create_customer(
                request.user, subscription.email,
            )
            customer_id = customer_result.get('customer_id', '')

        # Create payment consent for recurring charges
        consent_result = sub_provider.create_payment_token(
            customer_id=customer_id,
            payment_method_data={'payment_method_id': payment_method_id},
        )
        new_consent_id = consent_result.get('token_id', '')

        if not new_consent_id:
            return Response(
                {'success': False, 'error': 'Could not set up recurring payment.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update subscription
        subscription.airwallex_consent_id = new_consent_id
        subscription.airwallex_customer_id = customer_id
        subscription.payment_provider_account = provider_account
        subscription.save(update_fields=[
            'airwallex_consent_id', 'airwallex_customer_id',
            'payment_provider_account', 'updated_at',
        ])

        # Confirmation email
        from license_checkout.services import _send_hosting_email
        _send_hosting_email(
            to_email=subscription.email,
            template_type='hosted_payment_method_updated',
            context={
                'store_name': subscription.store_name,
                'plan_name': subscription.hosted_plan.name,
            },
            label='payment method updated (API)',
        )

        # If past_due, attempt immediate charge
        recovery_result = None
        if subscription.status == HostedSubscription.Status.PAST_DUE:
            recovery_result = _attempt_recovery_charge(subscription)

        message = 'Payment method updated successfully.'
        if recovery_result is True:
            message = 'Payment method updated and outstanding balance paid successfully.'
        elif recovery_result is False:
            message = 'Payment method updated, but the outstanding charge could not be processed. We will retry automatically.'

        return Response({'success': True, 'message': message})

    except Exception as e:
        logger.error('Payment method update failed for %s: %s', subscription.store_slug, e)
        return Response(
            {'success': False, 'error': 'An error occurred. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _attempt_recovery_charge(subscription):
    """Attempt to charge an overdue subscription. Returns True/False/None."""
    from license_checkout.tasks import _charge_subscription

    amount = subscription.billing_amount
    billing_log = HostedBillingLog.objects.create(
        subscription=subscription,
        cycle_number=subscription.billing_cycle_count,
        billing_date=timezone.now(),
        amount=amount,
        status=HostedBillingLog.Status.PROCESSING,
    )

    if _charge_subscription(subscription, amount, billing_log):
        from dateutil.relativedelta import relativedelta
        now = timezone.now()
        if subscription.billing_interval == 'annual':
            period_end = now + relativedelta(years=1)
        else:
            period_end = now + relativedelta(months=1)

        subscription.status = HostedSubscription.Status.ACTIVE
        subscription.retry_count = 0
        subscription.grace_period_end_date = None
        subscription.current_period_start = now
        subscription.current_period_end = period_end
        subscription.next_billing_date = period_end
        subscription.last_billing_date = now
        subscription.last_billing_status = 'successful'
        subscription.save()

        billing_log.status = HostedBillingLog.Status.SUCCESSFUL
        billing_log.save(update_fields=['status'])
        return True

    return False


# ── Change Billing Interval ────────────────────────────────────────────

@api_view(['GET', 'POST'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_change_interval(request, subscription_id=None):
    """
    GET: Return pricing details for interval switch.
    POST: Execute the interval change.
    """
    subscription, error = _resolve_subscription(request.user, subscription_id)
    if error:
        return error

    if subscription.status != HostedSubscription.Status.ACTIVE:
        return Response(
            {'success': False, 'error': 'Interval can only be changed on an active subscription.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    plan = subscription.hosted_plan
    current_interval = subscription.billing_interval
    new_interval = 'annual' if current_interval == 'monthly' else 'monthly'

    pricing = _calculate_interval_change(subscription, plan, new_interval)

    if request.method == 'GET':
        serializer = IntervalChangeDetailSerializer(pricing)
        return Response({'success': True, 'data': serializer.data})

    return _execute_interval_change(subscription, plan, new_interval, pricing)


def _calculate_interval_change(subscription, plan, new_interval):
    """Calculate pricing for an interval change."""
    monthly_price = plan.monthly_price.amount if plan.monthly_price else Decimal('0')
    annual_price = plan.annual_price.amount if plan.annual_price else Decimal('0')
    annual_total = annual_price * 12

    pos_monthly = (
        Decimal('29.00')
        if subscription.pos_addon and not plan.includes_pos
        else Decimal('0')
    )
    pos_annual = pos_monthly * 12

    current_price = (
        (monthly_price + pos_monthly)
        if subscription.billing_interval == 'monthly'
        else (annual_total + pos_annual)
    )

    if new_interval == 'annual':
        now = timezone.now()
        if subscription.current_period_end and subscription.current_period_start:
            total_days = (subscription.current_period_end - subscription.current_period_start).days
            remaining_days = max((subscription.current_period_end - now).days, 0)
            daily_rate = (monthly_price + pos_monthly) / max(total_days, 1)
            credit = daily_rate * remaining_days
        else:
            credit = Decimal('0')

        new_price = annual_total + pos_annual
        charge_amount = max(new_price - credit, Decimal('0'))
        savings = (monthly_price + pos_monthly) * 12 - new_price
    else:
        new_price = monthly_price + pos_monthly
        charge_amount = Decimal('0')
        credit = Decimal('0')
        savings = Decimal('0')

    return {
        'current_interval': subscription.billing_interval,
        'new_interval': new_interval,
        'current_price': current_price,
        'new_price': new_price,
        'charge_amount': charge_amount,
        'credit': credit,
        'savings': savings,
        'next_billing_date': subscription.next_billing_date,
    }


def _execute_interval_change(subscription, plan, new_interval, pricing):
    """Execute the billing interval change."""
    current_interval = subscription.billing_interval
    charge_amount = pricing['charge_amount']

    if new_interval == 'annual' and charge_amount > 0:
        from dateutil.relativedelta import relativedelta
        from license_checkout.tasks import _charge_subscription
        now = timezone.now()

        billing_log = HostedBillingLog.objects.create(
            subscription=subscription,
            cycle_number=subscription.billing_cycle_count + 1,
            billing_date=now,
            amount=charge_amount,
            status=HostedBillingLog.Status.PROCESSING,
        )

        success = _charge_subscription(subscription, charge_amount, billing_log)
        if not success:
            return Response(
                {'success': False, 'error': 'Payment failed. Please update your payment method.'},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        subscription.billing_interval = 'annual'
        subscription.current_period_start = now
        subscription.current_period_end = now + relativedelta(years=1)
        subscription.next_billing_date = subscription.current_period_end
        subscription.billing_cycle_count += 1
        subscription.last_billing_date = now
        subscription.last_billing_status = 'successful'
        subscription.save()

        billing_log.status = HostedBillingLog.Status.SUCCESSFUL
        billing_log.save(update_fields=['status'])
    else:
        subscription.billing_interval = 'monthly'
        subscription.save(update_fields=['billing_interval', 'updated_at'])

    from license_checkout.services import _send_hosting_email
    _send_hosting_email(
        to_email=subscription.email,
        template_type='hosted_interval_changed',
        context={
            'store_name': subscription.store_name,
            'plan_name': plan.name,
            'old_interval': current_interval,
            'new_interval': new_interval,
            'next_billing_date': (
                subscription.next_billing_date.strftime('%d %B %Y')
                if subscription.next_billing_date else ''
            ),
        },
        label='interval changed (API)',
    )

    return Response({
        'success': True,
        'message': f'Billing interval changed to {new_interval}.',
        'data': {
            'new_interval': new_interval,
            'next_billing_date': (
                subscription.next_billing_date.isoformat()
                if subscription.next_billing_date else None
            ),
        },
    })


# ── Subscription List ─────────────────────────────────────────────────

@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def hosting_subscription_list(request):
    """List all hosted subscriptions for the user."""
    subs = _get_all_subscriptions(request.user)
    serializer = HostedSubscriptionListSerializer(subs, many=True)
    return Response({'success': True, 'data': serializer.data})


# ── License List ─────────────────────────────────────────────────────

@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def license_list(request):
    """All licenses for this account (self-hosted + hosted)."""
    licenses = _get_all_license_keys(request.user)
    serializer = LicenseListItemSerializer(licenses, many=True)
    return Response({'success': True, 'data': serializer.data})


# ── Self-Hosted License (singular — backward compat) ─────────────────

@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def license_detail(request):
    """License details — proxied from the update server."""
    license_key = _resolve_first_license_key(request.user)

    if not license_key:
        return Response(
            {'success': False, 'error': 'No license found for this account.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = _fetch_license_from_update_server(license_key)
    if not data:
        return Response(
            {'success': False, 'error': 'Could not retrieve license details.'},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    serializer = LicenseDetailSerializer(data)
    return Response({'success': True, 'data': serializer.data})


@api_view(['GET'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def license_maintenance(request):
    """Maintenance status — proxied from the update server."""
    license_key = _resolve_first_license_key(request.user)

    if not license_key:
        return Response(
            {'success': False, 'error': 'No license found for this account.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = _fetch_maintenance_from_update_server(license_key)
    if data is None:
        return Response(
            {'success': False, 'error': 'Could not retrieve maintenance status.'},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    serializer = MaintenanceStatusSerializer(data)
    return Response({'success': True, 'data': serializer.data})


def _fetch_license_from_update_server(license_key):
    """Fetch license data from the update server internal API."""
    import httpx

    url = f"{settings.UPGRADE_SERVER_URL.rstrip('/')}/api/v1/internal/licenses/{license_key}/"
    try:
        resp = httpx.get(
            url,
            headers={'X-API-Key': settings.UPGRADE_SERVER_INTERNAL_API_KEY},
            timeout=10,
        )
        if resp.status_code != 200:
            logger.warning('Update server returned %s for license %s', resp.status_code, license_key[:8])
            return None

        data = resp.json()
        # Mask the license key for frontend display
        masked_key = f"{license_key[:8]}...{license_key[-4:]}" if len(license_key) > 12 else license_key

        return {
            'license_key': masked_key,
            'license_type': data.get('license_type', ''),
            'product_type': data.get('product_type', ''),
            'owner_name': data.get('owner_name', ''),
            'company': data.get('company', ''),
            'is_active': data.get('is_active', False),
            'expires_at': data.get('expires_at'),
            'installations_count': data.get('installations_count', 0),
            'max_installations': data.get('max_installations', 1),
        }
    except Exception as e:
        logger.error('Failed to fetch license from update server: %s', e)
        return None


def _fetch_maintenance_from_update_server(license_key):
    """Fetch maintenance status from the update server internal API."""
    import httpx

    url = f"{settings.UPGRADE_SERVER_URL.rstrip('/')}/api/v1/internal/licenses/{license_key}/maintenance/"
    try:
        resp = httpx.get(
            url,
            headers={'X-API-Key': settings.UPGRADE_SERVER_INTERNAL_API_KEY},
            timeout=10,
        )
        if resp.status_code != 200:
            logger.warning('Update server returned %s for maintenance %s', resp.status_code, license_key[:8])
            return None

        data = resp.json()
        return {
            'active': data.get('maintenance_active', False),
            'expires_at': data.get('maintenance_expires_at'),
            'days_remaining': data.get('days_remaining', 0),
            'grace_period': data.get('grace_period', False),
            'reinstatement_tier': data.get('reinstatement_tier', ''),
        }
    except Exception as e:
        logger.error('Failed to fetch maintenance from update server: %s', e)
        return None


# ── Change Password ───────────────────────────────────────────────────

@api_view(['POST'])
@authentication_classes(HQ_AUTH)
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change password for the currently authenticated user."""
    from .serializers_hq import ChangePasswordSerializer

    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    if not user.check_password(serializer.validated_data['current_password']):
        return Response(
            {'success': False, 'error': 'Current password is incorrect.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(serializer.validated_data['new_password'])
    user.save(update_fields=['password'])

    # Rotate the auth token so the user stays logged in with a new token
    from rest_framework.authtoken.models import Token
    Token.objects.filter(user=user).delete()
    new_token = Token.objects.create(user=user)

    return Response({
        'success': True,
        'message': 'Password changed successfully.',
        'data': {'token': new_token.key},
    })


# ── Ghost Account Activation ───────────────────────────────────────────

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def activate_ghost_account(request):
    """Activate a ghost account by setting a password. Returns auth token."""
    from django.contrib.auth import get_user_model
    from rest_framework.authtoken.models import Token

    serializer = GhostActivationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    User = get_user_model()

    try:
        uid = urlsafe_base64_decode(serializer.validated_data['uidb64']).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {'success': False, 'error': 'Invalid activation link.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not default_token_generator.check_token(user, serializer.validated_data['token']):
        return Response(
            {'success': False, 'error': 'Activation link has expired.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not user.username.startswith('guest_'):
        return Response(
            {'success': False, 'error': 'This account is already activated.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Convert guest to full account
    from accounts.services.account_creation_service import AccountCreationService
    success, message = AccountCreationService.convert_guest_to_full_account(
        user=user,
        password=serializer.validated_data['password'],
        send_confirmation_email=True,
    )

    if not success:
        return Response(
            {'success': False, 'error': message},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Return auth token for auto-login
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'success': True,
        'message': 'Account activated successfully.',
        'data': {
            'token': token.key,
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
        },
    })
