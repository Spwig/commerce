"""
Referral validation service.

Validates referral eligibility, checks caps, and prevents abuse.
"""

from datetime import timedelta

from django.utils import timezone

from .fraud import calculate_risk_score

# List of known disposable email domains
DISPOSABLE_EMAIL_DOMAINS = [
    "tempmail.com",
    "guerrillamail.com",
    "10minutemail.com",
    "mailinator.com",
    "throwaway.email",
    "temp-mail.org",
    "getnada.com",
    "fakeinbox.com",
    "trashmail.com",
    "maildrop.cc",
    "sharklasers.com",
    "guerrillamail.info",
    "grr.la",
    "guerrillamail.biz",
    "guerrillamail.de",
    "spam4.me",
    "yopmail.com",
    "mytemp.email",
    "mohmal.com",
    "emailondeck.com",
]


def validate_referral(order, identity, program):
    """
    Main validation function for referral attribution.

    Checks all eligibility rules and returns validation result.

    Args:
        order (Order): First order from referee
        identity (ReferralIdentity): Referrer identity
        program (ReferralProgram): Referral program configuration

    Returns:
        tuple: (is_valid: bool, reason: str, validation_data: dict)
    """
    validation_data = {}

    # Check self-referral
    is_valid, reason = check_self_referral(order, identity)
    validation_data["self_referral_check"] = {"passed": is_valid, "reason": reason}
    if not is_valid:
        return False, reason, validation_data

    # Check new customer
    is_valid, reason = check_new_customer(order.user, program)
    validation_data["new_customer_check"] = {"passed": is_valid, "reason": reason}
    if not is_valid:
        return False, reason, validation_data

    # Check minimum order value
    is_valid, reason = check_min_order_value(order, program)
    validation_data["min_order_value_check"] = {"passed": is_valid, "reason": reason}
    if not is_valid:
        return False, reason, validation_data

    # Check monthly cap
    is_valid, reason = check_monthly_cap(identity, program)
    validation_data["monthly_cap_check"] = {"passed": is_valid, "reason": reason}
    if not is_valid:
        return False, reason, validation_data

    # Check disposable email
    is_valid, reason = check_disposable_email(order.user.email)
    validation_data["disposable_email_check"] = {"passed": is_valid, "reason": reason}
    if not is_valid:
        return False, reason, validation_data

    # All checks passed
    return True, "ok", validation_data


def validate_attribution(attribution):
    """
    Validate a ReferralAttribution and calculate risk score.

    This is a convenience wrapper around validate_referral that works
    with attribution objects directly.

    Args:
        attribution (ReferralAttribution): Attribution to validate

    Returns:
        tuple: (is_valid: bool, validation_data: dict, risk_score: int)
            - is_valid: Whether attribution passes all validation checks
            - validation_data: Dict with details of each validation check
            - risk_score: Fraud risk score (0-100)
    """
    from ..models import ReferralProgram

    # Get program
    program = ReferralProgram.get_program()
    if not program:
        return False, {"error": "No active referral program"}, 100

    # Validate using existing function
    is_valid, reason, validation_data = validate_referral(
        attribution.first_order, attribution.referrer_identity, program
    )

    # Calculate risk score
    risk_score = calculate_risk_score(attribution)

    return is_valid, validation_data, risk_score


def check_self_referral(order, identity):
    """
    Check if referee is the same as referrer (self-referral).

    Args:
        order (Order): Order instance
        identity (ReferralIdentity): Referrer identity

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    if order.user == identity.customer:
        return False, "self_referral"

    return True, "ok"


def check_new_customer(customer, program):
    """
    Check if customer is new (first order).

    Args:
        customer (User): Customer instance
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    # Check if program requires new customers only
    if not program.eligibility_rules.get("new_customer_only", True):
        return True, "ok"

    # Check if customer has previous orders
    from orders.models import Order

    previous_orders = Order.objects.filter(
        user=customer, status__in=["completed", "delivered", "shipped"]
    ).count()

    if previous_orders > 1:  # > 1 because current order is already counted
        return False, "not_new_customer"

    return True, "ok"


def check_min_order_value(order, program):
    """
    Check if order meets minimum order value requirement.

    Args:
        order (Order): Order instance
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    min_order_value = program.get_min_order_value()

    # order.total_amount is a Money object, get the numeric amount
    order_value = (
        order.total_amount.amount if hasattr(order.total_amount, "amount") else order.total_amount
    )

    if min_order_value and order_value < min_order_value:
        return False, "below_minimum"

    return True, "ok"


def check_monthly_cap(identity, program):
    """
    Check if referrer has exceeded monthly referral cap.

    Args:
        identity (ReferralIdentity): Referrer identity
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    monthly_cap = program.get_monthly_cap()

    if not monthly_cap:
        return True, "ok"

    # Count successful referrals in current month
    from ..models import ReferralAttribution

    start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    monthly_count = ReferralAttribution.objects.filter(
        referrer_identity=identity, status="approved", created_at__gte=start_of_month
    ).count()

    if monthly_count >= monthly_cap:
        return False, "cap_exceeded"

    return True, "ok"


def check_lifetime_cap(identity, program):
    """
    Check if referrer has exceeded lifetime referral cap.

    Args:
        identity (ReferralIdentity): Referrer identity
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    lifetime_cap = program.get_lifetime_cap()

    if not lifetime_cap:
        return True, "ok"

    # Count all successful referrals
    from ..models import ReferralAttribution

    lifetime_count = ReferralAttribution.objects.filter(
        referrer_identity=identity, status="approved"
    ).count()

    if lifetime_count >= lifetime_cap:
        return False, "cap_exceeded"

    return True, "ok"


def check_disposable_email(email):
    """
    Check if email is from a disposable email domain.

    Args:
        email (str): Email address to check

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    if not email:
        return False, "disposable_email"

    domain = email.split("@")[-1].lower()

    if is_disposable_email(domain):
        return False, "disposable_email"

    return True, "ok"


def is_disposable_email(domain):
    """
    Check if domain is in disposable email list.

    Args:
        domain (str): Email domain

    Returns:
        bool: True if disposable
    """
    return domain.lower() in DISPOSABLE_EMAIL_DOMAINS


def exceeds_monthly_cap(referrer_customer_id, monthly_cap):
    """
    Helper function to check if referrer exceeds monthly cap.

    Args:
        referrer_customer_id (int): Referrer customer ID
        monthly_cap (int): Monthly cap limit

    Returns:
        bool: True if cap exceeded
    """
    if not monthly_cap:
        return False

    from ..models import ReferralAttribution, ReferralIdentity

    try:
        identity = ReferralIdentity.objects.get(customer_id=referrer_customer_id)
    except ReferralIdentity.DoesNotExist:
        return False

    start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    monthly_count = ReferralAttribution.objects.filter(
        referrer_identity=identity, status="approved", created_at__gte=start_of_month
    ).count()

    return monthly_count >= monthly_cap


def check_velocity(identity, window_hours=24, max_referrals=5):
    """
    Check if referrer is creating referrals too quickly (velocity check).

    Args:
        identity (ReferralIdentity): Referrer identity
        window_hours (int): Time window in hours (default 24)
        max_referrals (int): Max referrals allowed in window (default 5)

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    from ..models import ReferralAttribution

    window_start = timezone.now() - timedelta(hours=window_hours)

    recent_count = ReferralAttribution.objects.filter(
        referrer_identity=identity, created_at__gte=window_start
    ).count()

    if recent_count >= max_referrals:
        return False, "velocity_exceeded"

    return True, "ok"


def check_order_excludes(order, program):
    """
    Check if order should be excluded from referral program.

    Args:
        order (Order): Order instance
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    eligibility_rules = program.eligibility_rules

    # Check if discounted orders are excluded
    if eligibility_rules.get("exclude_discounts", False):
        if hasattr(order, "discount_amount") and order.discount_amount > 0:
            return False, "discounted_order"

    # Check if gift card orders are excluded
    if eligibility_rules.get("exclude_gift_cards", False):
        has_gift_cards = order.items.filter(product__product_type="gift_card").exists()
        if has_gift_cards:
            return False, "gift_card_order"

    return True, "ok"


def check_staff_account(customer, program):
    """
    Check if customer is a staff account that should be excluded.

    Args:
        customer (User): Customer instance
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    eligibility_rules = program.eligibility_rules

    if eligibility_rules.get("exclude_staff", True):
        if customer.is_staff or customer.is_superuser:
            return False, "staff_account"

    return True, "ok"
