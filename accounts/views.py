"""
Customer Account Views
Handles customer-facing account management including subscriptions.
"""
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from subscriptions.models import CustomerSubscription, PaymentToken, BillingCycleLog
from subscriptions.manager import SubscriptionManager


@login_required
def subscription_list(request):
    """
    Display list of customer's subscriptions
    """
    subscriptions = CustomerSubscription.objects.filter(
        user=request.user
    ).select_related('plan', 'product', 'variant', 'payment_token').order_by('-created_at')

    context = {
        'subscriptions': subscriptions,
        'active_count': subscriptions.filter(status__in=['active', 'trial']).count(),
    }

    return render(request, 'accounts/subscriptions/list.html', context)


@login_required
def subscription_detail(request, subscription_id):
    """
    Display detailed subscription information with billing history
    """
    subscription = get_object_or_404(
        CustomerSubscription.objects.select_related(
            'plan', 'product', 'variant', 'payment_token'
        ),
        subscription_id=subscription_id,
        user=request.user
    )

    # Get billing history
    billing_logs = BillingCycleLog.objects.filter(
        subscription=subscription
    ).order_by('-billing_date')[:12]  # Last 12 billing cycles

    # Get available payment tokens for updating payment method
    payment_tokens = PaymentToken.objects.filter(
        user=request.user,
        is_active=True
    )

    context = {
        'subscription': subscription,
        'billing_logs': billing_logs,
        'payment_tokens': payment_tokens,
        'can_pause': subscription.status in ['active', 'trial'],
        'can_resume': subscription.status == 'paused',
        'can_cancel': subscription.status not in ['canceled', 'expired'],
    }

    return render(request, 'accounts/subscriptions/detail.html', context)


@login_required
def subscription_pause(request, subscription_id):
    """
    Pause a subscription
    """
    subscription = get_object_or_404(
        CustomerSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        if subscription.status not in ['active', 'trial']:
            messages.error(request, _('This subscription cannot be paused.'))
            return redirect('accounts:subscription_detail', subscription_id=subscription_id)

        try:
            manager = SubscriptionManager(subscription.payment_gateway)
            manager.pause_subscription(subscription, reason='Paused by customer')
            messages.success(request, _('Subscription paused successfully.'))
        except Exception as e:
            messages.error(request, _('Failed to pause subscription: {}').format(str(e)))

        return redirect('accounts:subscription_detail', subscription_id=subscription_id)

    return render(request, 'accounts/subscriptions/pause_confirm.html', {
        'subscription': subscription
    })


@login_required
def subscription_resume(request, subscription_id):
    """
    Resume a paused subscription
    """
    subscription = get_object_or_404(
        CustomerSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        if subscription.status != 'paused':
            messages.error(request, _('This subscription is not paused.'))
            return redirect('accounts:subscription_detail', subscription_id=subscription_id)

        try:
            manager = SubscriptionManager(subscription.payment_gateway)
            manager.resume_subscription(subscription)
            messages.success(request, _('Subscription resumed successfully.'))
        except Exception as e:
            messages.error(request, _('Failed to resume subscription: {}').format(str(e)))

        return redirect('accounts:subscription_detail', subscription_id=subscription_id)

    return render(request, 'accounts/subscriptions/resume_confirm.html', {
        'subscription': subscription
    })


@login_required
def subscription_cancel(request, subscription_id):
    """
    Cancel a subscription
    """
    subscription = get_object_or_404(
        CustomerSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        if subscription.status in ['canceled', 'expired']:
            messages.error(request, _('This subscription is already canceled.'))
            return redirect('accounts:subscription_detail', subscription_id=subscription_id)

        immediately = request.POST.get('immediately', 'false') == 'true'
        reason = request.POST.get('reason', 'Canceled by customer')

        try:
            manager = SubscriptionManager(subscription.payment_gateway)
            manager.cancel_subscription(
                subscription,
                immediately=immediately,
                reason=reason
            )

            if immediately:
                messages.success(request, _('Subscription canceled immediately.'))
            else:
                messages.success(request, _('Subscription will be canceled at the end of the current billing period.'))
        except Exception as e:
            messages.error(request, _('Failed to cancel subscription: {}').format(str(e)))

        return redirect('accounts:subscription_detail', subscription_id=subscription_id)

    context = {
        'subscription': subscription,
        'days_until_next_billing': subscription.days_until_next_billing(),
    }

    return render(request, 'accounts/subscriptions/cancel_confirm.html', context)


@login_required
def subscription_update_payment(request, subscription_id):
    """
    Update payment method for a subscription
    """
    subscription = get_object_or_404(
        CustomerSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        payment_token_id = request.POST.get('payment_token_id')

        if not payment_token_id:
            messages.error(request, _('Please select a payment method.'))
            return redirect('accounts:subscription_detail', subscription_id=subscription_id)

        try:
            payment_token = PaymentToken.objects.get(
                token_id=payment_token_id,
                user=request.user,
                is_active=True
            )
        except PaymentToken.DoesNotExist:
            messages.error(request, _('Invalid payment method selected.'))
            return redirect('accounts:subscription_detail', subscription_id=subscription_id)

        try:
            manager = SubscriptionManager(subscription.payment_gateway)
            manager.update_payment_method(subscription, payment_token)
            messages.success(request, _('Payment method updated successfully.'))
        except Exception as e:
            messages.error(request, _('Failed to update payment method: {}').format(str(e)))

        return redirect('accounts:subscription_detail', subscription_id=subscription_id)

    # Get available payment tokens
    payment_tokens = PaymentToken.objects.filter(
        user=request.user,
        is_active=True,
        gateway=subscription.payment_gateway
    )

    context = {
        'subscription': subscription,
        'payment_tokens': payment_tokens,
    }

    return render(request, 'accounts/subscriptions/update_payment.html', context)


@login_required
def payment_token_list(request):
    """
    Display list of customer's saved payment methods
    """
    tokens = PaymentToken.objects.filter(
        user=request.user
    ).order_by('-is_default', '-created_at')

    context = {
        'payment_tokens': tokens,
    }

    return render(request, 'accounts/payment_tokens/list.html', context)


@login_required
def payment_token_delete(request, token_id):
    """
    Delete a saved payment method
    """
    token = get_object_or_404(
        PaymentToken,
        token_id=token_id,
        user=request.user
    )

    if request.method == 'POST':
        # Check if token is being used by active subscriptions
        active_subs = CustomerSubscription.objects.filter(
            payment_token=token,
            status__in=['active', 'trial', 'past_due']
        ).exists()

        if active_subs:
            messages.error(
                request,
                _('Cannot delete this payment method - it is being used by active subscriptions.')
            )
            return redirect('accounts:payment_token_list')

        try:
            from subscriptions.provider_base import get_provider

            # Delete token at provider
            provider = get_provider(token.gateway)
            provider.delete_payment_token(token.gateway_token_id)

            # Delete local record
            token.delete()

            messages.success(request, _('Payment method deleted successfully.'))
        except Exception as e:
            messages.error(request, _('Failed to delete payment method: {}').format(str(e)))

        return redirect('accounts:payment_token_list')

    context = {
        'payment_token': token,
    }

    return render(request, 'accounts/payment_tokens/delete_confirm.html', context)


@login_required
def payment_token_set_default(request, token_id):
    """
    Set a payment method as default
    """
    if request.method == 'POST':
        token = get_object_or_404(
            PaymentToken,
            token_id=token_id,
            user=request.user
        )

        # Remove default from all other tokens
        PaymentToken.objects.filter(user=request.user, is_default=True).update(is_default=False)

        # Set this token as default
        token.is_default = True
        token.save()

        messages.success(request, _('Default payment method updated.'))

    return redirect('accounts:payment_token_list')


# ==========================================
# ADDRESS MANAGEMENT VIEWS
# ==========================================

@login_required
def customer_address_list(request):
    """
    Display list of customer's saved addresses (active only)
    """
    from orders.models import Address
    from orders.services.address_service import AddressService

    # Get active addresses with usage counts
    addresses = AddressService.get_address_with_usage(request.user)

    context = {
        'addresses': addresses,
    }

    return render(request, 'accounts/addresses/list.html', context)


@login_required
def customer_address_add(request):
    """
    Add a new address
    """
    from orders.models import Address
    from orders.services.address_service import AddressService

    if request.method == 'POST':
        try:
            # Create address using service
            address_data = {
                'name': request.POST.get('name'),
                'company': request.POST.get('company', ''),
                'address1': request.POST.get('address1'),
                'address2': request.POST.get('address2', ''),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'postal_code': request.POST.get('postal_code'),
                'country': request.POST.get('country'),
                'phone': request.POST.get('phone', ''),
                'address_type': request.POST.get('address_type', 'both'),
                'is_default': request.POST.get('is_default') == 'on',
            }

            # Validate required fields
            required_fields = ['name', 'address1', 'city', 'state', 'postal_code', 'country', 'address_type']
            missing_fields = [field for field in required_fields if not address_data.get(field)]

            if missing_fields:
                messages.error(request, _('Please fill in all required fields.'))
                return render(request, 'accounts/addresses/form.html', {'address': None})

            # Create address
            address = Address.objects.create(
                user=request.user,
                **address_data
            )

            messages.success(request, _('Address added successfully.'))
            return redirect('accounts:address_list')

        except Exception as e:
            messages.error(request, _('Failed to add address: {}').format(str(e)))

    return render(request, 'accounts/addresses/form.html', {'address': None})


@login_required
def customer_address_edit(request, address_id):
    """
    Edit an existing address with versioning support
    """
    from orders.models import Address
    from orders.services.address_service import AddressService

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user,
        is_active=True  # Only allow editing active addresses
    )

    # Check if address has been used in orders
    used_in_orders = address.is_used_in_orders()

    if request.method == 'POST':
        try:
            # Collect updated address data
            update_data = {
                'name': request.POST.get('name'),
                'company': request.POST.get('company', ''),
                'address1': request.POST.get('address1'),
                'address2': request.POST.get('address2', ''),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'postal_code': request.POST.get('postal_code'),
                'country': request.POST.get('country'),
                'phone': request.POST.get('phone', ''),
                'address_type': request.POST.get('address_type', 'both'),
                'is_default': request.POST.get('is_default') == 'on'
            }

            # Validate required fields
            required_fields = ['name', 'address1', 'city', 'state', 'postal_code', 'country']
            if not all(update_data.get(field) for field in required_fields):
                messages.error(request, _('Please fill in all required fields.'))
                return render(request, 'accounts/addresses/form.html', {
                    'address': address,
                    'used_in_orders': used_in_orders
                })

            # Use AddressService to handle versioning
            success, message, updated_address = AddressService.update_address(
                address=address,
                user=request.user,
                **update_data
            )

            if success:
                if used_in_orders and updated_address != address:
                    # A new version was created
                    messages.info(
                        request,
                        _('Address updated. A new version was created because this address was used in previous orders.')
                    )
                else:
                    messages.success(request, message)
                return redirect('accounts:address_list')
            else:
                messages.error(request, message)

        except Exception as e:
            messages.error(request, _('Failed to update address: {}').format(str(e)))

    context = {
        'address': address,
        'used_in_orders': used_in_orders,
        'order_count': address.get_order_count() if used_in_orders else 0,
    }

    return render(request, 'accounts/addresses/form.html', context)


@login_required
def customer_address_delete(request, address_id):
    """
    Delete an address
    """
    from orders.models import Address

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':
        try:
            address.delete()
            messages.success(request, _('Address deleted successfully.'))
            return redirect('accounts:address_list')
        except Exception as e:
            messages.error(request, _('Failed to delete address: {}').format(str(e)))
            return redirect('accounts:address_list')

    context = {
        'address': address,
    }

    return render(request, 'accounts/addresses/delete_confirm.html', context)


@login_required
def customer_address_set_default(request, address_id, address_type):
    """
    Set an address as default for a specific type
    """
    from orders.models import Address

    if request.method == 'POST':
        address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user
        )

        try:
            # Remove default from all other addresses of the same type
            Address.objects.filter(
                user=request.user,
                address_type=address_type,
                is_default=True
            ).exclude(id=address_id).update(is_default=False)

            # Set this address as default
            address.is_default = True
            address.save()

            messages.success(request, _('Default address updated.'))
        except Exception as e:
            messages.error(request, _('Failed to update default address: {}').format(str(e)))

    return redirect('accounts:address_list')


@login_required
def dashboard(request):
    """
    Customer account dashboard
    """
    from orders.models import Order, Address
    from subscriptions.models import CustomerSubscription
    from decimal import Decimal
    from django.db import models

    user = request.user

    # Get recent orders
    recent_orders = Order.objects.filter(
        user=user
    ).order_by('-created_at')[:5]

    # Get active subscriptions
    active_subscriptions = CustomerSubscription.objects.filter(
        user=user,
        status__in=['active', 'trial']
    ).count()

    # Get saved addresses
    saved_addresses = Address.objects.filter(
        user=user
    ).count()

    # Get loyalty information
    loyalty_member = None
    loyalty_balance = None
    loyalty_tier = None
    try:
        from loyalty.models import LoyaltyMember, LoyaltyBalance
        loyalty_member = LoyaltyMember.objects.select_related('current_tier').get(customer=user)
        loyalty_balance = LoyaltyBalance.objects.get(member=loyalty_member)
        loyalty_tier = loyalty_member.current_tier
    except (ImportError, LoyaltyMember.DoesNotExist, LoyaltyBalance.DoesNotExist):
        pass

    # Get referral information
    referral_identity = None
    referral_stats = None
    referral_rewards_pending = Decimal('0')
    referral_rewards_total = Decimal('0')
    try:
        from referrals.models import ReferralIdentity, ReferralReward
        referral_identity = ReferralIdentity.objects.get(customer=user)
        referral_stats = {
            'clicks': referral_identity.total_clicks,
            'signups': referral_identity.total_signups,
            'conversions': referral_identity.total_conversions,
            'conversion_rate': referral_identity.get_conversion_rate(),
        }

        # Get referral rewards
        referral_rewards = ReferralReward.objects.filter(referrer=user)
        referral_rewards_pending = referral_rewards.filter(status='pending').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0')
        referral_rewards_total = referral_rewards.filter(status__in=['issued', 'redeemed']).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0')
    except (ImportError, ReferralIdentity.DoesNotExist):
        pass

    # Get affiliate information
    is_affiliate = hasattr(user, 'affiliate_profile')
    affiliate_stats = None
    if is_affiliate:
        affiliate = user.affiliate_profile
        if affiliate.status == 'active':
            balance_summary = affiliate.get_balance_summary()
            affiliate_stats = {
                'total_earned': balance_summary['total_earned'],
                'pending': balance_summary['pending_approval'],
                'outstanding': balance_summary['outstanding_balance'],
                'total_paid': balance_summary['total_paid'],
                'affiliate_code': affiliate.affiliate_code,
            }

    # Get unread reply count for messages badge
    unread_reply_count = 0
    try:
        from admin_api.models import CustomerMessage
        from django.db.models import Q
        unread_reply_count = CustomerMessage.objects.filter(
            Q(user=user) | Q(email=user.email, user__isnull=True),
            status='replied'
        ).count()
    except Exception:
        pass

    context = {
        'recent_orders': recent_orders,
        'active_subscriptions': active_subscriptions,
        'saved_addresses': saved_addresses,
        # Loyalty
        'loyalty_member': loyalty_member,
        'loyalty_balance': loyalty_balance,
        'loyalty_tier': loyalty_tier,
        # Referrals
        'referral_identity': referral_identity,
        'referral_stats': referral_stats,
        'referral_rewards_pending': referral_rewards_pending,
        'referral_rewards_total': referral_rewards_total,
        # Affiliate
        'is_affiliate': is_affiliate,
        'affiliate_stats': affiliate_stats,
        # Messages
        'unread_reply_count': unread_reply_count,
    }

    # Hosted subscription (HQ only)
    if getattr(settings, 'SPWIG_IS_HQ', False):
        try:
            from license_checkout.models import HostedSubscription
            hosted_sub = HostedSubscription.objects.select_related('hosted_plan').filter(
                user=user,
            ).exclude(
                status=HostedSubscription.Status.TERMINATED,
            ).first()
            context['hosted_subscription'] = hosted_sub
        except Exception:
            pass

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """
    Customer profile settings page
    Allows customers to update their name and profile information
    """
    from datetime import datetime
    from .models import CustomerProfile

    # Get or create customer profile
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        try:
            # Update user information
            user = request.user
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.save()

            # Update profile information
            profile.phone = request.POST.get('phone', '').strip()

            # Handle date of birth
            date_of_birth_str = request.POST.get('date_of_birth', '').strip()
            if date_of_birth_str:
                try:
                    profile.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
                except ValueError:
                    pass  # Invalid date format, skip
            else:
                profile.date_of_birth = None

            # Update business information
            profile.is_business_customer = request.POST.get('is_business_customer') == 'on'
            if profile.is_business_customer:
                profile.company_name = request.POST.get('company_name', '').strip()
                profile.tax_number = request.POST.get('tax_number', '').strip()
            else:
                # Clear business fields if not a business customer
                profile.company_name = ''
                profile.tax_number = ''

            profile.save()

            messages.success(request, _('Profile updated successfully.'))
            return redirect('accounts:profile')

        except Exception as e:
            messages.error(request, _('Failed to update profile: {}').format(str(e)))

    context = {
        'user': request.user,
    }

    return render(request, 'accounts/profile.html', context)


def activate_guest_account(request, uidb64, token):
    """
    Activate a guest account by converting it to a registered account.
    This view is accessed via the activation link sent to guest customers.
    """
    from django.contrib.auth import get_user_model, login
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    from django.views.decorators.http import require_http_methods
    from django.db import transaction

    User = get_user_model()

    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Verify token and that user is a guest
    if user is not None and default_token_generator.check_token(user, token):
        # Verify this is actually a guest user
        if not user.username.startswith('guest_'):
            messages.error(request, _('This account is already registered.'))
            return redirect('accounts:dashboard')

        # Check if link has expired (48 hours = 172800 seconds)
        # Django's default_token_generator already handles expiration

        # Show activation form if GET request
        if request.method == 'GET':
            context = {
                'user': user,
                'uidb64': uidb64,
                'token': token,
                'email': user.email,
            }
            return render(request, 'accounts/activate_guest.html', context)

        # Process activation if POST request
        elif request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')

            # Validate passwords
            if not password or not password_confirm:
                messages.error(request, _('Please provide a password.'))
                context = {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'email': user.email,
                }
                return render(request, 'accounts/activate_guest.html', context)

            if password != password_confirm:
                messages.error(request, _('Passwords do not match.'))
                context = {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'email': user.email,
                }
                return render(request, 'accounts/activate_guest.html', context)

            # Password strength validation
            if len(password) < 8:
                messages.error(request, _('Password must be at least 8 characters long.'))
                context = {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'email': user.email,
                }
                return render(request, 'accounts/activate_guest.html', context)

            try:
                from accounts.services.account_creation_service import AccountCreationService

                success, message = AccountCreationService.convert_guest_to_full_account(
                    user=user,
                    password=password,
                    send_confirmation_email=False  # Already verified via token
                )

                if success:
                    # Log the user in
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    messages.success(
                        request,
                        _('Your account has been activated! Welcome to {}').format(request.get_host())
                    )
                    return redirect('accounts:dashboard')
                else:
                    messages.error(request, message)

            except Exception as e:
                messages.error(request, _('An error occurred while activating your account. Please try again.'))
                context = {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'email': user.email,
                }
                return render(request, 'accounts/activate_guest.html', context)
    else:
        # Invalid or expired token
        messages.error(
            request,
            _('The activation link is invalid or has expired. Please contact support for assistance.')
        )
        return redirect('catalog:home')  # Redirect to homepage


def unsubscribe(request, token):
    """
    One-click unsubscribe landing page.
    Accessible via token without login for GDPR compliance.

    GET: Show unsubscribe confirmation page
    POST: Process unsubscribe request
    """
    from accounts.models import CommunicationPreference
    from accounts.services.preference_service import PreferenceService
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        # Find user by unsubscribe token
        prefs = CommunicationPreference.objects.get(unsubscribe_token=token)
        user = prefs.user

        # Get message type from query param
        message_type = request.GET.get('type', '')

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'unsubscribe_type':
                # Unsubscribe from specific message type
                from accounts.constants import get_message_type_category

                category, app = get_message_type_category(message_type)

                if category == 'marketing':
                    prefs.email_marketing = False
                elif category == 'app_specific' and app:
                    if app in prefs.app_preferences:
                        prefs.app_preferences[app]['enabled'] = False

                prefs.save()

                # Invalidate cache
                PreferenceService.invalidate_cache(user.id, 'email', message_type)

                messages.success(
                    request,
                    _('You have been unsubscribed from {message_type} emails.').format(
                        message_type=message_type.replace('_', ' ').title()
                    )
                )

            elif action == 'unsubscribe_all':
                # Unsubscribe from all marketing
                reason = request.POST.get('reason', '')
                result = PreferenceService.unsubscribe_all(user, reason=reason)

                if result['success']:
                    messages.success(
                        request,
                        _('You have been unsubscribed from all marketing communications.')
                    )
                else:
                    messages.error(
                        request,
                        _('An error occurred. Please try again.')
                    )

            elif action == 'resubscribe':
                # Resubscribe to specific message type
                from accounts.constants import get_message_type_category

                category, app = get_message_type_category(message_type)

                if category == 'marketing':
                    prefs.email_marketing = True
                elif category == 'app_specific' and app:
                    if app not in prefs.app_preferences:
                        prefs.app_preferences[app] = CommunicationPreference.get_default_app_preferences()[app]
                    prefs.app_preferences[app]['enabled'] = True

                prefs.save()

                # Invalidate cache
                PreferenceService.invalidate_cache(user.id, 'email', message_type)

                messages.success(
                    request,
                    _('You have been resubscribed to {message_type} emails.').format(
                        message_type=message_type.replace('_', ' ').title()
                    )
                )

            # Redirect back to unsubscribe page to show updated state
            return redirect('accounts:unsubscribe', token=token)

        # GET request - show unsubscribe page
        from accounts.constants import get_message_type_category

        category, app = get_message_type_category(message_type)

        # Determine current subscription status
        is_subscribed = False
        if category == 'marketing':
            is_subscribed = prefs.email_marketing
        elif category == 'app_specific' and app:
            is_subscribed = prefs.app_preferences.get(app, {}).get('enabled', False)

        context = {
            'user': user,
            'message_type': message_type,
            'message_type_display': message_type.replace('_', ' ').title(),
            'is_subscribed': is_subscribed,
            'preferences_url': f'/accounts/preferences/',
        }

        return render(request, 'accounts/unsubscribe.html', context)

    except CommunicationPreference.DoesNotExist:
        messages.error(
            request,
            _('Invalid unsubscribe link. Please use the link from your email.')
        )
        return redirect('catalog:home')


@login_required
def communication_preferences(request):
    """
    Communication preferences center.
    Allows users to manage all email/SMS preferences in one place.
    """
    from accounts.models import CommunicationPreference
    from accounts.services.preference_service import PreferenceService

    # Get or create preferences
    prefs, created = PreferenceService.get_or_create_for_user(request.user)

    if request.method == 'POST':
        # Update preferences from form
        prefs.email_marketing = request.POST.get('email_marketing') == 'on'

        # Blog preferences
        blog_enabled = request.POST.get('blog_enabled') == 'on'
        blog_frequency = request.POST.get('blog_frequency', 'weekly')

        if 'blog' not in prefs.app_preferences:
            prefs.app_preferences['blog'] = CommunicationPreference.get_default_app_preferences()['blog']

        prefs.app_preferences['blog']['enabled'] = blog_enabled
        prefs.app_preferences['blog']['frequency'] = blog_frequency

        # Loyalty preferences
        loyalty_enabled = request.POST.get('loyalty_enabled') == 'on'

        if 'loyalty' not in prefs.app_preferences:
            prefs.app_preferences['loyalty'] = CommunicationPreference.get_default_app_preferences()['loyalty']

        prefs.app_preferences['loyalty']['enabled'] = loyalty_enabled
        prefs.app_preferences['loyalty']['points_earned'] = request.POST.get('loyalty_points_earned') == 'on'
        prefs.app_preferences['loyalty']['tier_changes'] = request.POST.get('loyalty_tier_changes') == 'on'
        prefs.app_preferences['loyalty']['rewards_available'] = request.POST.get('loyalty_rewards_available') == 'on'
        prefs.app_preferences['loyalty']['points_expiring'] = request.POST.get('loyalty_points_expiring') == 'on'

        # Referrals preferences
        referrals_enabled = request.POST.get('referrals_enabled') == 'on'

        if 'referrals' not in prefs.app_preferences:
            prefs.app_preferences['referrals'] = CommunicationPreference.get_default_app_preferences()['referrals']

        prefs.app_preferences['referrals']['enabled'] = referrals_enabled
        prefs.app_preferences['referrals']['reward_issued'] = request.POST.get('referrals_reward_issued') == 'on'
        prefs.app_preferences['referrals']['referral_converted'] = request.POST.get('referrals_referral_converted') == 'on'

        # Affiliate preferences
        affiliate_enabled = request.POST.get('affiliate_enabled') == 'on'

        if 'affiliate' not in prefs.app_preferences:
            prefs.app_preferences['affiliate'] = CommunicationPreference.get_default_app_preferences()['affiliate']

        prefs.app_preferences['affiliate']['enabled'] = affiliate_enabled
        prefs.app_preferences['affiliate']['commission_earned'] = request.POST.get('affiliate_commission_earned') == 'on'
        prefs.app_preferences['affiliate']['payout_processed'] = request.POST.get('affiliate_payout_processed') == 'on'
        prefs.app_preferences['affiliate']['monthly_report'] = request.POST.get('affiliate_monthly_report') == 'on'

        # Save changes
        prefs.save()

        # Invalidate cache
        PreferenceService.invalidate_cache(request.user.id)

        messages.success(request, _('Your communication preferences have been updated.'))
        return redirect('accounts:communication_preferences')

    # GET request - display form
    # Get app preferences with defaults
    blog_prefs = prefs.app_preferences.get('blog', CommunicationPreference.get_default_app_preferences()['blog'])
    loyalty_prefs = prefs.app_preferences.get('loyalty', CommunicationPreference.get_default_app_preferences()['loyalty'])
    referrals_prefs = prefs.app_preferences.get('referrals', CommunicationPreference.get_default_app_preferences()['referrals'])
    affiliate_prefs = prefs.app_preferences.get('affiliate', CommunicationPreference.get_default_app_preferences()['affiliate'])

    # Get smart suggestions (Enhancement 5)
    from accounts.services.smart_defaults_service import SmartDefaultsService
    smart_suggestions = SmartDefaultsService.get_recommendations_for_preference_center(request.user)

    context = {
        'prefs': prefs,
        'blog_prefs': blog_prefs,
        'loyalty_prefs': loyalty_prefs,
        'referrals_prefs': referrals_prefs,
        'affiliate_prefs': affiliate_prefs,
        'smart_suggestions': smart_suggestions,
    }

    return render(request, 'accounts/preferences.html', context)


@login_required
def preference_history(request):
    """
    Display chronological timeline of all preference changes.

    Shows audit trail with timestamps, actions, sources, and IP addresses.
    Paginated for performance (20 entries per page).
    """
    from accounts.models import PreferenceChangeLog
    from django.core.paginator import Paginator

    # Get user's preference change logs
    logs = PreferenceChangeLog.objects.filter(
        user=request.user
    ).order_by('-timestamp')

    # Paginate: 20 per page
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'has_logs': logs.exists(),
    }

    return render(request, 'accounts/preference_history.html', context)


# ========== Customer Messages ==========

@login_required
def message_list(request):
    """
    Display list of customer's messages from the portal.
    Queries by user FK first; includes email-matched anonymous messages.
    """
    from admin_api.models import CustomerMessage
    from django.db.models import Q

    user = request.user
    user_messages = CustomerMessage.objects.filter(
        Q(user=user) | Q(email=user.email, user__isnull=True)
    ).select_related('order').order_by('-created_at')

    context = {
        'messages_list': user_messages,
        'total_count': user_messages.count(),
    }
    return render(request, 'accounts/messages/list.html', context)


@login_required
def message_detail(request, message_id):
    """
    Show a single message thread including any merchant reply, with follow-up form.
    """
    from admin_api.models import CustomerMessage
    from django.db.models import Q
    from accounts.forms import FollowUpMessageForm

    user = request.user
    message_obj = get_object_or_404(
        CustomerMessage.objects.select_related('order', 'replied_by'),
        Q(user=user) | Q(email=user.email, user__isnull=True),
        pk=message_id
    )

    follow_up_form = None
    if message_obj.reply_text:
        if request.method == 'POST' and request.POST.get('action') == 'follow_up':
            follow_up_form = FollowUpMessageForm(request.POST)
            if follow_up_form.is_valid():
                full_name = f"{user.first_name} {user.last_name}".strip() or user.email
                CustomerMessage.objects.create(
                    user=user,
                    name=full_name,
                    email=user.email,
                    subject=f"Re: {message_obj.subject}",
                    message=follow_up_form.cleaned_data['message'],
                    message_type=message_obj.message_type,
                    order=message_obj.order,
                    status='unread',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                )
                messages.success(request, _('Your follow-up message has been sent.'))
                return redirect('accounts:message_detail', message_id=message_id)
        else:
            follow_up_form = FollowUpMessageForm()

    context = {
        'msg': message_obj,
        'follow_up_form': follow_up_form,
    }
    return render(request, 'accounts/messages/detail.html', context)


@login_required
def message_new(request):
    """
    New message form — allows customers to submit a message, optionally linked to an order.
    """
    from admin_api.models import CustomerMessage
    from orders.models import Order
    from accounts.forms import CustomerMessageForm

    user = request.user

    user_orders = Order.objects.filter(user=user).order_by('-created_at').only(
        'id', 'order_number', 'created_at'
    )

    if request.method == 'POST':
        form = CustomerMessageForm(request.POST)
        form.fields['order'].queryset = user_orders
        if form.is_valid():
            full_name = f"{user.first_name} {user.last_name}".strip() or user.email
            msg = CustomerMessage.objects.create(
                user=user,
                name=full_name,
                email=user.email,
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                message_type=form.cleaned_data['message_type'],
                order=form.cleaned_data.get('order'),
                status='unread',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            )
            messages.success(request, _('Your message has been submitted. We will respond shortly.'))
            return redirect('accounts:message_detail', message_id=msg.pk)
    else:
        initial = {}
        order_id = request.GET.get('order')
        if order_id:
            try:
                preselected = user_orders.get(pk=order_id)
                initial['order'] = preselected
            except Order.DoesNotExist:
                pass
        form = CustomerMessageForm(initial=initial)
        form.fields['order'].queryset = user_orders

    context = {
        'form': form,
    }
    return render(request, 'accounts/messages/new.html', context)


def guest_order_lookup(request):
    """
    Guest order lookup page.
    GET: Show email entry form
    POST: Send magic link email to the guest so they can view their orders
    """
    from django.contrib.auth import get_user_model
    from django.contrib.auth.tokens import default_token_generator
    from django.contrib.sites.models import Site
    from django.conf import settings as django_settings
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes

    User = get_user_model()

    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()

        if not email:
            messages.error(request, _('Please enter your email address.'))
            return render(request, 'accounts/guest_order_lookup.html')

        # Find guest user with this email (always show success to prevent enumeration)
        guest_user = User.objects.filter(
            email__iexact=email,
            username__startswith='guest_'
        ).order_by('-date_joined').first()

        if guest_user and guest_user.orders.exists():
            try:
                # Build magic link
                uid = urlsafe_base64_encode(force_bytes(guest_user.pk))
                token = default_token_generator.make_token(guest_user)

                try:
                    site = Site.objects.get_current()
                    site_url = (
                        f"http://{site.domain}"
                        if django_settings.DEBUG
                        else f"https://{site.domain}"
                    )
                except Exception:
                    site_url = getattr(django_settings, 'SITE_URL', 'http://localhost:8000')

                magic_link = f"{site_url}/{request.LANGUAGE_CODE}/accounts/guest-orders/{uid}/{token}/"

                # Send email with magic link
                from email_system.services.email_sender import EmailSendingService
                EmailSendingService.send_template_email(
                    to_email=email,
                    template_type='password_reset',  # Reuse existing template for now
                    context={
                        'customer_name': guest_user.first_name or _('Customer'),
                        'reset_url': magic_link,
                        'subject_override': _('View Your Orders'),
                    },
                    language=request.LANGUAGE_CODE,
                )
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Failed to send guest order magic link: {e}")

        # Always show success to prevent email enumeration
        messages.success(
            request,
            _('If we have orders for that email address, we\'ve sent you a link to view them.')
        )
        return render(request, 'accounts/guest_order_lookup.html', {'email_sent': True})

    return render(request, 'accounts/guest_order_lookup.html')


def guest_orders_view(request, uidb64, token):
    """
    Token-authenticated view of guest orders.
    Shows all orders for a guest user and offers account conversion.
    """
    from django.contrib.auth import get_user_model, login
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    from django.db import transaction
    from orders.models import Order

    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, _('This link is invalid or has expired.'))
        return redirect('accounts:guest_order_lookup')

    if not user.username.startswith('guest_'):
        messages.info(request, _('This account is already registered. Please log in.'))
        return redirect('account_login')

    # Handle account conversion (POST)
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not password or not password_confirm:
            messages.error(request, _('Please provide a password.'))
        elif password != password_confirm:
            messages.error(request, _('Passwords do not match.'))
        elif len(password) < 8:
            messages.error(request, _('Password must be at least 8 characters long.'))
        else:
            try:
                from accounts.services.account_creation_service import AccountCreationService
                with transaction.atomic():
                    success, message = AccountCreationService.convert_guest_to_full_account(
                        user=user,
                        password=password,
                        send_confirmation_email=True
                    )
                    if success:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        messages.success(request, _('Your account has been created! Welcome!'))
                        return redirect('accounts:dashboard')
                    else:
                        messages.error(request, message)
            except Exception:
                messages.error(request, _('An error occurred. Please try again.'))

    # Fetch orders
    orders = Order.objects.filter(user=user).order_by('-created_at')

    context = {
        'guest_user': user,
        'orders': orders,
        'order_count': orders.count(),
        'uidb64': uidb64,
        'token': token,
        'email': user.email,
    }
    return render(request, 'accounts/guest_orders.html', context)


# ========== Customer Bookings ==========

@login_required
def booking_list(request):
    """
    Display list of customer's bookings split into upcoming and past.
    """
    from catalog.models import Booking
    from django.utils import timezone as tz

    now = tz.now()
    profile = getattr(request.user, 'profile', None)

    if profile:
        base_qs = Booking.objects.filter(
            customer=profile
        ).select_related('product', 'resource', 'order')
    else:
        base_qs = Booking.objects.none()

    upcoming_bookings = base_qs.filter(
        start_datetime__gt=now,
        status__in=['pending_confirmation', 'confirmed'],
    ).order_by('start_datetime')

    past_bookings = base_qs.exclude(
        pk__in=upcoming_bookings.values_list('pk', flat=True)
    ).order_by('-start_datetime')

    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    }
    return render(request, 'accounts/bookings/list.html', context)


@login_required
def booking_detail(request, booking_id):
    """
    Display single booking detail with cancel/reschedule actions.
    """
    from catalog.models import Booking, BookingNote

    profile = getattr(request.user, 'profile', None)
    booking = get_object_or_404(
        Booking.objects.select_related('product', 'resource', 'order'),
        pk=booking_id,
        customer=profile,
    )

    visible_notes = BookingNote.objects.filter(
        booking=booking,
        is_customer_visible=True,
    ).order_by('-created_at')

    ical_url = None
    if booking.ical_uid:
        from django.urls import reverse
        ical_url = reverse(
            'catalog_api:booking-ical',
            kwargs={'product_slug': booking.product.slug, 'ical_uid': booking.ical_uid},
        )

    context = {
        'booking': booking,
        'visible_notes': visible_notes,
        'ical_url': ical_url,
        'can_cancel': booking.status in ('pending_confirmation', 'confirmed'),
        'can_reschedule': booking.status in ('pending_confirmation', 'confirmed') and booking.is_upcoming,
    }
    return render(request, 'accounts/bookings/detail.html', context)


@login_required
def booking_cancel_action(request, booking_id):
    """
    Cancel a booking from the customer account page.
    """
    from catalog.models import Booking
    from catalog.services.booking_service import BookingLifecycleService

    if request.method != 'POST':
        return redirect('accounts:booking_detail', booking_id=booking_id)

    profile = getattr(request.user, 'profile', None)
    booking = get_object_or_404(Booking, pk=booking_id, customer=profile)

    if booking.status not in ('pending_confirmation', 'confirmed'):
        messages.error(request, _('This booking cannot be cancelled.'))
        return redirect('accounts:booking_detail', booking_id=booking_id)

    reason = request.POST.get('reason', '').strip()
    try:
        BookingLifecycleService.cancel_booking(
            booking=booking,
            author=request.user,
            reason=reason,
            initiated_by='customer',
        )
        messages.success(request, _('Your booking has been cancelled.'))
    except Exception as e:
        messages.error(request, _('Failed to cancel booking: {}').format(str(e)))

    return redirect('accounts:booking_detail', booking_id=booking_id)


@login_required
def booking_reschedule_action(request, booking_id):
    """
    Reschedule a booking from the customer account page.
    """
    from catalog.models import Booking
    from catalog.services.booking_service import BookingLifecycleService
    from datetime import datetime

    if request.method != 'POST':
        return redirect('accounts:booking_detail', booking_id=booking_id)

    profile = getattr(request.user, 'profile', None)
    booking = get_object_or_404(Booking, pk=booking_id, customer=profile)

    if booking.status not in ('pending_confirmation', 'confirmed') or not booking.is_upcoming:
        messages.error(request, _('This booking cannot be rescheduled.'))
        return redirect('accounts:booking_detail', booking_id=booking_id)

    date_str = request.POST.get('date', '')
    time_start_str = request.POST.get('time_start', '')
    time_end_str = request.POST.get('time_end', '')

    if not all([date_str, time_start_str, time_end_str]):
        messages.error(request, _('Please provide a date and times.'))
        return redirect('accounts:booking_detail', booking_id=booking_id)

    try:
        from django.utils import timezone as tz
        new_start = tz.make_aware(datetime.strptime(f'{date_str} {time_start_str}', '%Y-%m-%d %H:%M'))
        new_end = tz.make_aware(datetime.strptime(f'{date_str} {time_end_str}', '%Y-%m-%d %H:%M'))
    except (ValueError, TypeError):
        messages.error(request, _('Invalid date or time format.'))
        return redirect('accounts:booking_detail', booking_id=booking_id)

    try:
        BookingLifecycleService.reschedule_booking(
            booking=booking,
            new_start=new_start,
            new_end=new_end,
            new_resource_id=None,
            author=request.user,
        )
        messages.success(request, _('Your booking has been rescheduled.'))
    except Exception as e:
        messages.error(request, _('Failed to reschedule booking: {}').format(str(e)))

    return redirect('accounts:booking_detail', booking_id=booking_id)
