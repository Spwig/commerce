"""
Test Data Factories

Helper functions to create test instances for referral program testing.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from ..models import (
    ReferralProgram,
    ReferralIdentity,
    ReferralAttribution,
    ReferralReward,
    ReferralEvent,
)
from orders.models import Order

User = get_user_model()


def create_user(email=None, **kwargs):
    """Create a test user."""
    if email is None:
        import uuid
        email = f"user_{uuid.uuid4().hex[:8]}@example.com"

    defaults = {
        'username': email,
        'email': email,
        'first_name': 'Test',
        'last_name': 'User',
    }
    defaults.update(kwargs)

    return User.objects.create_user(**defaults)


def create_referral_program(**kwargs):
    """Create a test referral program."""
    defaults = {
        'name': 'Test Referral Program',
        'status': 'active',
        'reward_config': {
            'referrer': {
                'kind': 'credit',
                'amount': 10.00
            },
            'referee': {
                'kind': 'coupon',
                'amount': 10.00
            }
        },
        'terms_and_conditions': 'Test terms',
        'eligibility_rules': {
            'new_customer_only': True,
            'min_order_value': 0,
        },
        'caps_config': {
            'referrer_monthly_cap': 10,
            'referrer_lifetime_cap': 100,
        },
        'fraud_policy': {
            'auto_approve_threshold': 30,
            'auto_reject_threshold': 90,
            'require_manual_review': True,
        },
        'tracking_config': {
            'cookie_ttl_days': 30,
        },
        'timing_config': {
            'reward_on': 'first_purchase',
        },
    }
    defaults.update(kwargs)

    # Delete any existing program (singleton)
    ReferralProgram.objects.all().delete()

    return ReferralProgram.objects.create(**defaults)


def create_referral_identity(customer=None, **kwargs):
    """Create a test referral identity."""
    if customer is None:
        customer = create_user()

    defaults = {
        'customer': customer,
    }
    defaults.update(kwargs)

    return ReferralIdentity.objects.create(**defaults)


def create_referral_event(referrer_identity=None, event_type='click', program=None, **kwargs):
    """Create a test referral event."""
    if referrer_identity is None:
        referrer_identity = create_referral_identity()

    if program is None:
        program = create_referral_program()

    defaults = {
        'program': program,
        'referrer_identity': referrer_identity,
        'event_type': event_type,
        'ip_address': '192.168.1.1',
        'user_agent': 'Mozilla/5.0',
        'metadata': {},
    }
    defaults.update(kwargs)

    return ReferralEvent.objects.create(**defaults)


def create_order(user=None, **kwargs):
    """Create a test order."""
    if user is None:
        user = create_user()

    defaults = {
        'user': user,
        'status': 'delivered',
        'total_amount': Decimal('50.00'),
        'order_number': f'ORDER-{user.id}-{timezone.now().timestamp()}',
        'email': user.email,
        'shipping_name': user.get_full_name() or user.email,
        'shipping_address1': '123 Test St',
        'shipping_city': 'Test City',
        'shipping_state': 'TS',
        'shipping_postal_code': '12345',
        'shipping_country': 'US',
        'subtotal': Decimal('50.00'),
    }
    defaults.update(kwargs)

    return Order.objects.create(**defaults)


def create_referral_attribution(
    referrer_identity=None,
    referee_customer=None,
    first_order=None,
    program=None,
    **kwargs
):
    """Create a test referral attribution."""
    if referrer_identity is None:
        referrer_identity = create_referral_identity()

    if referee_customer is None:
        referee_customer = create_user()

    if first_order is None:
        first_order = create_order(user=referee_customer)

    if program is None:
        program = create_referral_program()

    defaults = {
        'program': program,
        'referrer_identity': referrer_identity,
        'referee_customer': referee_customer,
        'first_order': first_order,
        'status': 'pending',
        'risk_score': 25,
        'validation_data': {
            'ref_token': referrer_identity.token,
            'clicked_at': timezone.now().isoformat(),
        },
    }
    defaults.update(kwargs)

    return ReferralAttribution.objects.create(**defaults)


def create_referral_reward(
    attribution=None,
    customer=None,
    program=None,
    **kwargs
):
    """Create a test referral reward."""
    if attribution is None:
        attribution = create_referral_attribution()

    if customer is None:
        customer = attribution.referrer_identity.customer

    if program is None:
        program = attribution.program

    defaults = {
        'program': program,
        'attribution': attribution,
        'customer': customer,
        'referrer_identity': attribution.referrer_identity,
        'recipient_type': 'referrer',
        'kind': 'credit',
        'amount': Decimal('10.00'),
        'status': 'pending',
    }
    defaults.update(kwargs)

    return ReferralReward.objects.create(**defaults)


def create_complete_referral_flow():
    """
    Create a complete referral flow for testing.

    Returns:
        dict: Dictionary containing all created objects:
            - program: ReferralProgram
            - referrer: User (referrer customer)
            - referrer_identity: ReferralIdentity
            - referee: User (referee customer)
            - order: Order (referee's first order)
            - attribution: ReferralAttribution
            - referrer_reward: ReferralReward (for referrer)
            - referee_reward: ReferralReward (for referee)
    """
    # Create program
    program = create_referral_program()

    # Create referrer
    referrer = create_user(email='referrer@example.com')
    referrer_identity = create_referral_identity(customer=referrer)

    # Create referee
    referee = create_user(email='referee@example.com')
    order = create_order(user=referee, total_amount=Decimal('100.00'))

    # Create attribution (approved)
    attribution = create_referral_attribution(
        referrer_identity=referrer_identity,
        referee_customer=referee,
        first_order=order,
        status='approved',
        risk_score=15,
    )

    # Create rewards (issued)
    referrer_reward = create_referral_reward(
        attribution=attribution,
        customer=referrer,
        referrer_identity=referrer_identity,
        recipient_type='referrer',
        kind='credit',
        amount=Decimal('10.00'),
        status='issued',
    )

    referee_reward = create_referral_reward(
        attribution=attribution,
        customer=referee,
        referrer_identity=None,
        recipient_type='referee',
        kind='coupon',
        amount=Decimal('10.00'),
        status='issued',
    )

    return {
        'program': program,
        'referrer': referrer,
        'referrer_identity': referrer_identity,
        'referee': referee,
        'order': order,
        'attribution': attribution,
        'referrer_reward': referrer_reward,
        'referee_reward': referee_reward,
    }
