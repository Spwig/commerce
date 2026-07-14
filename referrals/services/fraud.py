"""
Fraud detection service for referral program.

Multi-layered fraud detection using IP, device fingerprint, velocity, and pattern analysis.
"""

from datetime import timedelta

from django.utils import timezone


def is_high_risk(order, identity, program):
    """
    Main fraud detection function.

    Calculates risk score and determines if referral is high risk.

    Args:
        order (Order): Order instance
        identity (ReferralIdentity): Referrer identity
        program (ReferralProgram): Program configuration

    Returns:
        tuple: (is_high_risk: bool, risk_score: int, fraud_signals: dict)
    """
    fraud_policy = program.fraud_policy
    fraud_signals = {}
    risk_score = 0

    # Check IP similarity
    if fraud_policy.get("check_ip", True):
        ip_risk, ip_signal = check_ip_similarity(identity, order)
        fraud_signals["ip_similarity"] = ip_signal
        risk_score += ip_risk

    # Check device fingerprint
    if fraud_policy.get("check_device", True):
        device_risk, device_signal = check_device_fingerprint(identity, order)
        fraud_signals["device_fingerprint"] = device_signal
        risk_score += device_risk

    # Check velocity (rapid referrals)
    if fraud_policy.get("check_velocity", True):
        velocity_window = fraud_policy.get("velocity_window_hours", 24)
        max_referrals = fraud_policy.get("max_referrals_per_window", 5)
        velocity_risk, velocity_signal = check_velocity(identity, velocity_window, max_referrals)
        fraud_signals["velocity"] = velocity_signal
        risk_score += velocity_risk

    # Check payment fingerprint similarity
    payment_risk, payment_signal = check_payment_fingerprint(identity, order)
    fraud_signals["payment_fingerprint"] = payment_signal
    risk_score += payment_risk

    # Check suspicious patterns
    pattern_risk, pattern_signal = check_suspicious_patterns(identity, order)
    fraud_signals["suspicious_patterns"] = pattern_signal
    risk_score += pattern_risk

    # Determine if high risk based on threshold
    auto_reject_threshold = fraud_policy.get("auto_reject_threshold", 80)
    is_high_risk = risk_score >= auto_reject_threshold

    return is_high_risk, risk_score, fraud_signals


def calculate_risk_score(attribution):
    """
    Calculate comprehensive risk score for an attribution.

    Args:
        attribution (ReferralAttribution): Attribution instance

    Returns:
        int: Risk score (0-100)
    """
    # Use validation_data from attribution if available
    if attribution.validation_data and "fraud_signals" in attribution.validation_data:
        fraud_signals = attribution.validation_data["fraud_signals"]

        # Sum up risk scores from all signals
        risk_score = 0
        for _signal_name, signal_data in fraud_signals.items():
            risk_score += signal_data.get("risk_points", 0)

        return min(risk_score, 100)  # Cap at 100

    return 0


def check_ip_similarity(identity, order):
    """
    Check if referrer and referee have similar IP addresses.

    Args:
        identity (ReferralIdentity): Referrer identity
        order (Order): Referee's order

    Returns:
        tuple: (risk_points: int, signal_data: dict)
    """
    from ..models import ReferralEvent

    # Get referrer's recent IP addresses
    referrer_events = (
        ReferralEvent.objects.filter(
            referrer_identity=identity, created_at__gte=timezone.now() - timedelta(days=30)
        )
        .values_list("ip_address", flat=True)
        .distinct()
    )

    # Get referee's recent IP addresses
    referee_events = (
        ReferralEvent.objects.filter(
            customer=order.user, created_at__gte=timezone.now() - timedelta(days=30)
        )
        .values_list("ip_address", flat=True)
        .distinct()
    )

    # Check for overlap
    common_ips = set(referrer_events) & set(referee_events)

    if common_ips:
        return 30, {
            "matched": True,
            "common_ips_count": len(common_ips),
            "risk_points": 30,
            "message": "Referrer and referee share IP addresses",
        }

    return 0, {"matched": False, "risk_points": 0, "message": "No IP similarity detected"}


def check_device_fingerprint(identity, order):
    """
    Check if referrer and referee have similar device fingerprints.

    Args:
        identity (ReferralIdentity): Referrer identity
        order (Order): Referee's order

    Returns:
        tuple: (risk_points: int, signal_data: dict)
    """
    from ..models import ReferralEvent

    # Get referrer's device fingerprints
    referrer_fingerprints = (
        ReferralEvent.objects.filter(
            referrer_identity=identity, created_at__gte=timezone.now() - timedelta(days=30)
        )
        .values_list("device_fingerprint", flat=True)
        .distinct()
    )

    # Get referee's device fingerprints
    referee_fingerprints = (
        ReferralEvent.objects.filter(
            customer=order.user, created_at__gte=timezone.now() - timedelta(days=30)
        )
        .values_list("device_fingerprint", flat=True)
        .distinct()
    )

    # Check for overlap
    common_fingerprints = set(referrer_fingerprints) & set(referee_fingerprints)

    if common_fingerprints:
        return 40, {
            "matched": True,
            "common_fingerprints_count": len(common_fingerprints),
            "risk_points": 40,
            "message": "Referrer and referee share device fingerprints",
        }

    return 0, {
        "matched": False,
        "risk_points": 0,
        "message": "No device fingerprint similarity detected",
    }


def check_velocity(identity, window_hours=24, max_referrals=5):
    """
    Check if referrer is creating referrals too quickly.

    Args:
        identity (ReferralIdentity): Referrer identity
        window_hours (int): Time window in hours
        max_referrals (int): Max referrals allowed in window

    Returns:
        tuple: (risk_points: int, signal_data: dict)
    """
    from ..models import ReferralAttribution

    window_start = timezone.now() - timedelta(hours=window_hours)

    recent_count = ReferralAttribution.objects.filter(
        referrer_identity=identity, created_at__gte=window_start
    ).count()

    if recent_count > max_referrals:
        # Higher velocity = higher risk
        excess = recent_count - max_referrals
        risk_points = min(20 + (excess * 5), 50)  # Cap at 50

        return risk_points, {
            "exceeded": True,
            "recent_count": recent_count,
            "max_allowed": max_referrals,
            "window_hours": window_hours,
            "risk_points": risk_points,
            "message": f"{recent_count} referrals in {window_hours} hours (max {max_referrals})",
        }

    return 0, {
        "exceeded": False,
        "recent_count": recent_count,
        "risk_points": 0,
        "message": "Velocity within normal range",
    }


def check_payment_fingerprint(identity, order):
    """
    Check if referrer and referee use similar payment methods.

    Args:
        identity (ReferralIdentity): Referrer identity
        order (Order): Referee's order

    Returns:
        tuple: (risk_points: int, signal_data: dict)
    """
    # This is a placeholder - actual implementation depends on payment method structure
    # In a real system, you would compare:
    # - BIN (first 6 digits of card)
    # - Last 4 digits
    # - Payment gateway tokens
    # - PayPal email addresses

    # For now, return low risk
    return 0, {
        "matched": False,
        "risk_points": 0,
        "message": "Payment fingerprint check not implemented",
    }


def check_suspicious_patterns(identity, order):
    """
    Check for suspicious patterns in referral behavior.

    Args:
        identity (ReferralIdentity): Referrer identity
        order (Order): Referee's order

    Returns:
        tuple: (risk_points: int, signal_data: dict)
    """
    from ..models import ReferralAttribution

    risk_points = 0
    patterns = []

    # Get order amount as numeric value (total_amount is a Money object)
    order_value = (
        order.total_amount.amount if hasattr(order.total_amount, "amount") else order.total_amount
    )

    # Check for round-number orders (often fraud)
    if order_value % 10 == 0 or order_value % 100 == 0:
        risk_points += 5
        patterns.append("Round number order total")

    # Check for same-day signup and purchase
    if order.user.date_joined.date() == order.created_at.date():
        risk_points += 10
        patterns.append("Same-day signup and purchase")

    # Check for multiple referrals with similar order values
    # Note: For Money fields, we need to compare the amount directly
    # Convert to Decimal for multiplication to avoid Decimal * float error
    from decimal import Decimal

    similar_value_count = ReferralAttribution.objects.filter(
        referrer_identity=identity,
        first_order__total_amount__gte=order_value * Decimal("0.95"),
        first_order__total_amount__lte=order_value * Decimal("1.05"),
    ).count()

    if similar_value_count >= 3:
        risk_points += 15
        patterns.append(f"{similar_value_count} referrals with similar order values")

    # Check for sequential referee signups (within 1 hour)
    recent_attributions = ReferralAttribution.objects.filter(
        referrer_identity=identity, created_at__gte=timezone.now() - timedelta(hours=1)
    ).count()

    if recent_attributions >= 3:
        risk_points += 20
        patterns.append(f"{recent_attributions} referrals within 1 hour")

    if patterns:
        return risk_points, {
            "detected": True,
            "patterns": patterns,
            "risk_points": risk_points,
            "message": f"Suspicious patterns detected: {', '.join(patterns)}",
        }

    return 0, {"detected": False, "risk_points": 0, "message": "No suspicious patterns detected"}


def get_fraud_policy_thresholds(policy_name):
    """
    Get fraud policy configuration by name.

    Args:
        policy_name (str): Policy name (strict, balanced, lenient)

    Returns:
        dict: Policy configuration
    """
    policies = {
        "strict": {
            "auto_reject_threshold": 50,
            "auto_approve_threshold": 20,
            "check_ip": True,
            "check_device": True,
            "check_velocity": True,
            "velocity_window_hours": 12,
            "max_referrals_per_window": 3,
        },
        "balanced": {
            "auto_reject_threshold": 80,
            "auto_approve_threshold": 30,
            "check_ip": True,
            "check_device": True,
            "check_velocity": True,
            "velocity_window_hours": 24,
            "max_referrals_per_window": 5,
        },
        "lenient": {
            "auto_reject_threshold": 90,
            "auto_approve_threshold": 40,
            "check_ip": True,
            "check_device": False,
            "check_velocity": True,
            "velocity_window_hours": 48,
            "max_referrals_per_window": 10,
        },
    }

    return policies.get(policy_name, policies["balanced"])
