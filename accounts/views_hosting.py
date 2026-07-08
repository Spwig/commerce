"""
Hosted subscription management views for spwig.com (HQ only).

These views let merchants manage their Spwig hosting subscription
from their account dashboard — update payment method, cancel, reactivate,
undo cancellation, and change billing interval.

Only loaded when SPWIG_IS_HQ=True (see accounts/urls.py).
"""
import logging
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _

from license_checkout.models import HostedSubscription, HostedBillingLog

logger = logging.getLogger(__name__)


def _get_subscription(request):
    """Get the authenticated user's hosted subscription (non-terminated)."""
    return get_object_or_404(
        HostedSubscription.objects.select_related('hosted_plan'),
        user=request.user,
        status__in=[
            HostedSubscription.Status.ACTIVE,
            HostedSubscription.Status.PAST_DUE,
            HostedSubscription.Status.SUSPENDED,
            HostedSubscription.Status.CANCELLED,
            HostedSubscription.Status.PENDING,
        ],
    )


# ── Detail ─────────────────────────────────────────────────────────────

@login_required
def hosting_detail(request):
    """Hosted subscription detail with billing history and action buttons."""
    subscription = _get_subscription(request)
    now = timezone.now()

    billing_logs = HostedBillingLog.objects.filter(
        subscription=subscription,
    ).order_by('-billing_date')[:12]

    # Determine available actions based on status
    can_cancel = subscription.status in (
        HostedSubscription.Status.ACTIVE,
        HostedSubscription.Status.PAST_DUE,
        HostedSubscription.Status.SUSPENDED,
    )
    can_undo_cancel = (
        subscription.status == HostedSubscription.Status.CANCELLED
        and subscription.current_period_end
        and subscription.current_period_end > now
    )
    can_reactivate = subscription.status in (
        HostedSubscription.Status.SUSPENDED,
        HostedSubscription.Status.CANCELLED,
    ) and not can_undo_cancel
    can_change_interval = subscription.status == HostedSubscription.Status.ACTIVE
    can_update_payment = subscription.status in (
        HostedSubscription.Status.ACTIVE,
        HostedSubscription.Status.PAST_DUE,
        HostedSubscription.Status.SUSPENDED,
    )

    # Build store URL from metadata or checkout
    store_url = ''
    admin_url = ''
    if subscription.store_slug:
        store_url = f'https://{subscription.store_slug}.myspwig.com'
        admin_url = f'{store_url}/en/admin/'

    context = {
        'subscription': subscription,
        'billing_logs': billing_logs,
        'billing_amount': subscription.billing_amount,
        'store_url': store_url,
        'admin_url': admin_url,
        'can_cancel': can_cancel,
        'can_undo_cancel': can_undo_cancel,
        'can_reactivate': can_reactivate,
        'can_change_interval': can_change_interval,
        'can_update_payment': can_update_payment,
    }

    return render(request, 'accounts/hosting/detail.html', context)


# ── Cancel ─────────────────────────────────────────────────────────────

@login_required
def hosting_cancel(request):
    """Cancel hosted subscription (end of billing period)."""
    subscription = _get_subscription(request)

    if subscription.status not in (
        HostedSubscription.Status.ACTIVE,
        HostedSubscription.Status.PAST_DUE,
        HostedSubscription.Status.SUSPENDED,
    ):
        messages.error(request, _('This subscription cannot be cancelled.'))
        return redirect('accounts:hosting_detail')

    access_until = subscription.current_period_end
    termination_date = access_until + timedelta(days=30) if access_until else timezone.now() + timedelta(days=30)

    if request.method == 'POST':
        reason = request.POST.get('reason', '')[:500]
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

        # Send cancellation email
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
            label='cancellation (self-service)',
        )

        # Notify update server with access_until
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

        messages.success(request, _('Your subscription has been cancelled. You will have access until %(date)s.') % {
            'date': access_until.strftime('%d %B %Y') if access_until else '',
        })
        return redirect('accounts:hosting_detail')

    context = {
        'subscription': subscription,
        'access_until': access_until,
        'termination_date': termination_date,
    }
    return render(request, 'accounts/hosting/cancel_confirm.html', context)


# ── Undo Cancel ────────────────────────────────────────────────────────

@login_required
def hosting_undo_cancel(request):
    """Reverse a cancellation before the paid period ends."""
    subscription = _get_subscription(request)
    now = timezone.now()

    if subscription.status != HostedSubscription.Status.CANCELLED:
        messages.error(request, _('This subscription is not cancelled.'))
        return redirect('accounts:hosting_detail')

    if not subscription.current_period_end or subscription.current_period_end <= now:
        messages.error(request, _('Your paid period has ended. Please reactivate your subscription instead.'))
        return redirect('accounts:hosting_detail')

    if request.method == 'POST':
        subscription.cancellation_type = HostedSubscription.CancellationType.NONE
        subscription.cancelled_at = None
        subscription.cancellation_reason = ''
        subscription.termination_scheduled_at = None
        subscription.status = HostedSubscription.Status.ACTIVE
        subscription.save(update_fields=[
            'cancellation_type', 'cancelled_at', 'cancellation_reason',
            'termination_scheduled_at', 'status', 'updated_at',
        ])

        # Notify update server to resume instance + clear termination
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
                'next_billing_date': subscription.next_billing_date.strftime('%d %B %Y') if subscription.next_billing_date else '',
            },
            label='cancellation reversed',
        )

        messages.success(request, _('Your cancellation has been reversed. Your subscription will continue as normal.'))
        return redirect('accounts:hosting_detail')

    context = {
        'subscription': subscription,
        'next_billing_date': subscription.next_billing_date,
    }
    return render(request, 'accounts/hosting/undo_cancel_confirm.html', context)


# ── Reactivate ─────────────────────────────────────────────────────────

@login_required
def hosting_reactivate(request):
    """Reactivate a suspended or cancelled subscription (charges immediately)."""
    subscription = _get_subscription(request)

    if subscription.status not in (
        HostedSubscription.Status.SUSPENDED,
        HostedSubscription.Status.CANCELLED,
    ):
        messages.error(request, _('This subscription does not need reactivation.'))
        return redirect('accounts:hosting_detail')

    amount = subscription.billing_amount

    if request.method == 'POST':
        from dateutil.relativedelta import relativedelta

        now = timezone.now()

        # Create billing log for the reactivation charge
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
            messages.error(request, _(
                'Payment failed. Please update your payment method first, then try reactivating.'
            ))
            return redirect('accounts:hosting_update_payment')

        # Payment succeeded — reactivate
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

        # Notify update server
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
            label='reactivation confirmed',
        )

        messages.success(request, _('Your subscription has been reactivated! Your store is being resumed.'))
        return redirect('accounts:hosting_detail')

    context = {
        'subscription': subscription,
        'amount': amount,
    }
    return render(request, 'accounts/hosting/reactivate_confirm.html', context)


# ── Update Payment Method ──────────────────────────────────────────────

@login_required
def hosting_update_payment(request):
    """Update the payment method for a hosted subscription.

    GET: Show current payment info and Airwallex card form.
    POST: Process the payment method update after Airwallex card capture.
    """
    subscription = _get_subscription(request)

    if subscription.status == HostedSubscription.Status.CANCELLED:
        messages.error(request, _('Please reactivate your subscription first.'))
        return redirect('accounts:hosting_detail')

    if request.method == 'POST':
        # The Airwallex Drop-in SDK handles card capture client-side.
        # After successful capture, it POSTs the payment_intent_id back.
        payment_intent_id = request.POST.get('payment_intent_id', '')

        if not payment_intent_id:
            messages.error(request, _('Payment method update failed. Please try again.'))
            return redirect('accounts:hosting_update_payment')

        try:
            from payment_providers.models import PaymentProviderAccount
            from subscriptions.provider_base import get_provider

            # Use the current active provider (may be different from the subscription's stored one)
            provider_account = PaymentProviderAccount.objects.filter(
                is_active=True, connection_status='connected',
            ).first()

            if not provider_account:
                messages.error(request, _('Payment system is currently unavailable. Please try again later.'))
                return redirect('accounts:hosting_detail')

            sub_provider = get_provider(provider_account)

            # Get the completed payment intent to extract payment method
            intent_details = sub_provider.get_payment_intent(payment_intent_id)
            payment_method_id = intent_details.get('latest_payment_attempt', {}).get(
                'payment_method', {}
            ).get('id', '')

            if not payment_method_id:
                messages.error(request, _('Could not retrieve payment method. Please try again.'))
                return redirect('accounts:hosting_update_payment')

            # Create or get Airwallex customer on the current provider
            customer_id = subscription.airwallex_customer_id
            if not customer_id:
                customer_result = sub_provider.create_customer(
                    request.user, subscription.email,
                )
                customer_id = customer_result.get('customer_id', '')

            # Create payment consent (token) for recurring charges
            consent_result = sub_provider.create_payment_token(
                customer_id=customer_id,
                payment_method_data={'payment_method_id': payment_method_id},
            )
            new_consent_id = consent_result.get('token_id', '')

            if not new_consent_id:
                messages.error(request, _('Could not set up recurring payment. Please try again.'))
                return redirect('accounts:hosting_update_payment')

            # Update subscription with new provider + consent
            subscription.airwallex_consent_id = new_consent_id
            subscription.airwallex_customer_id = customer_id
            subscription.payment_provider_account = provider_account
            subscription.save(update_fields=[
                'airwallex_consent_id', 'airwallex_customer_id',
                'payment_provider_account', 'updated_at',
            ])

            # Send confirmation email
            from license_checkout.services import _send_hosting_email
            _send_hosting_email(
                to_email=subscription.email,
                template_type='hosted_payment_method_updated',
                context={
                    'store_name': subscription.store_name,
                    'plan_name': subscription.hosted_plan.name,
                },
                label='payment method updated',
            )

            # If subscription was past_due, attempt immediate charge with new method
            if subscription.status == HostedSubscription.Status.PAST_DUE:
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

                    messages.success(request, _('Payment method updated and outstanding balance paid successfully!'))
                else:
                    messages.warning(request, _(
                        'Payment method updated, but the outstanding charge could not be processed. '
                        'We will retry automatically.'
                    ))
            else:
                messages.success(request, _('Payment method updated successfully.'))

            return redirect('accounts:hosting_detail')

        except Exception as e:
            logger.error('Payment method update failed for %s: %s', subscription.store_slug, e)
            messages.error(request, _('An error occurred. Please try again or contact support.'))
            return redirect('accounts:hosting_update_payment')

    # GET — prepare Airwallex payment form
    payment_config = {}
    try:
        from payment_providers.models import PaymentProviderAccount
        from subscriptions.provider_base import get_provider

        provider_account = PaymentProviderAccount.objects.filter(
            is_active=True, connection_status='connected',
        ).first()

        if provider_account:
            sub_provider = get_provider(provider_account)
            # Create a verification intent (small amount, auto-voided)
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
                'provider_slug': provider_account.component.slug if provider_account.component else '',
                'env': 'demo' if provider_account.test_mode else 'prod',
            }
    except Exception as e:
        logger.error('Failed to create verification intent for %s: %s', subscription.store_slug, e)

    context = {
        'subscription': subscription,
        'payment_config': payment_config,
    }
    return render(request, 'accounts/hosting/update_payment.html', context)


# ── Change Billing Interval ────────────────────────────────────────────

@login_required
def hosting_change_interval(request):
    """Switch between monthly and annual billing."""
    subscription = _get_subscription(request)

    if subscription.status != HostedSubscription.Status.ACTIVE:
        messages.error(request, _('You can only change billing interval on an active subscription.'))
        return redirect('accounts:hosting_detail')

    plan = subscription.hosted_plan
    current_interval = subscription.billing_interval
    new_interval = 'annual' if current_interval == 'monthly' else 'monthly'

    # Calculate pricing
    monthly_price = plan.monthly_price.amount if plan.monthly_price else Decimal('0')
    annual_price = plan.annual_price.amount if plan.annual_price else Decimal('0')
    annual_total = annual_price * 12

    # POS addon
    pos_monthly = Decimal('29.00') if subscription.pos_addon and not plan.includes_pos else Decimal('0')
    pos_annual = pos_monthly * 12

    if new_interval == 'annual':
        # Monthly → Annual: charge prorated amount
        now = timezone.now()
        if subscription.current_period_end and subscription.current_period_start:
            total_days = (subscription.current_period_end - subscription.current_period_start).days
            remaining_days = max((subscription.current_period_end - now).days, 0)
            daily_rate = (monthly_price + pos_monthly) / max(total_days, 1)
            credit = daily_rate * remaining_days
        else:
            credit = Decimal('0')

        charge_amount = (annual_total + pos_annual) - credit
        charge_amount = max(charge_amount, Decimal('0'))
        savings = (monthly_price + pos_monthly) * 12 - (annual_total + pos_annual)
    else:
        # Annual → Monthly: no charge, takes effect at next renewal
        charge_amount = Decimal('0')
        credit = Decimal('0')
        savings = Decimal('0')

    if request.method == 'POST':
        if new_interval == 'annual' and charge_amount > 0:
            # Charge the prorated annual amount
            from dateutil.relativedelta import relativedelta
            now = timezone.now()

            billing_log = HostedBillingLog.objects.create(
                subscription=subscription,
                cycle_number=subscription.billing_cycle_count + 1,
                billing_date=now,
                amount=charge_amount,
                status=HostedBillingLog.Status.PROCESSING,
            )

            from license_checkout.tasks import _charge_subscription
            success = _charge_subscription(subscription, charge_amount, billing_log)

            if not success:
                messages.error(request, _('Payment failed. Please update your payment method and try again.'))
                return redirect('accounts:hosting_detail')

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
            # Annual → Monthly: just change the interval, effective at renewal
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
                'next_billing_date': subscription.next_billing_date.strftime('%d %B %Y') if subscription.next_billing_date else '',
            },
            label='interval changed',
        )

        messages.success(request, _('Billing interval changed to %(interval)s.') % {
            'interval': new_interval,
        })
        return redirect('accounts:hosting_detail')

    context = {
        'subscription': subscription,
        'current_interval': current_interval,
        'new_interval': new_interval,
        'monthly_price': monthly_price + pos_monthly,
        'annual_total': annual_total + pos_annual,
        'annual_monthly_equivalent': (annual_total + pos_annual) / 12,
        'charge_amount': charge_amount,
        'credit': credit,
        'savings': savings,
    }
    return render(request, 'accounts/hosting/change_interval_confirm.html', context)
