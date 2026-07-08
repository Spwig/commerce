"""
Referrals services.

Export all service functions for easy importing.
"""
from .tracking import (
    generate_token,
    generate_qr_code,
    track_click,
    track_signup,
    track_order,
    get_ref_token_from_cookie,
    set_ref_cookie,
    hash_ip_address,
    hash_device_fingerprint,
)

from .validation import (
    validate_referral,
    validate_attribution,
    check_self_referral,
    check_new_customer,
    check_min_order_value,
    check_monthly_cap,
    check_lifetime_cap,
    check_disposable_email,
    is_disposable_email,
    exceeds_monthly_cap,
    check_velocity,
    check_order_excludes,
    check_staff_account,
)

from .fraud import (
    is_high_risk,
    calculate_risk_score,
    check_ip_similarity,
    check_device_fingerprint,
    check_payment_fingerprint,
    check_suspicious_patterns,
    get_fraud_policy_thresholds,
)

from .rewards import (
    create_rewards,
    issue_reward,
    redeem_reward,
    revoke_reward,
    expire_old_rewards,
    create_wallet_credit,
    create_coupon_code,
    create_percentage_coupon,
)

from .analytics import (
    get_referral_dashboard_stats,
    get_referral_performance_over_time,
)

__all__ = [
    # Tracking
    'generate_token',
    'generate_qr_code',
    'track_click',
    'track_signup',
    'track_order',
    'get_ref_token_from_cookie',
    'set_ref_cookie',
    'hash_ip_address',
    'hash_device_fingerprint',
    # Validation
    'validate_referral',
    'validate_attribution',
    'check_self_referral',
    'check_new_customer',
    'check_min_order_value',
    'check_monthly_cap',
    'check_lifetime_cap',
    'check_disposable_email',
    'is_disposable_email',
    'exceeds_monthly_cap',
    'check_velocity',
    'check_order_excludes',
    'check_staff_account',
    # Fraud
    'is_high_risk',
    'calculate_risk_score',
    'check_ip_similarity',
    'check_device_fingerprint',
    'check_payment_fingerprint',
    'check_suspicious_patterns',
    'get_fraud_policy_thresholds',
    # Rewards
    'create_rewards',
    'issue_reward',
    'redeem_reward',
    'revoke_reward',
    'expire_old_rewards',
    'create_wallet_credit',
    'create_coupon_code',
    'create_percentage_coupon',
    # Analytics
    'get_referral_dashboard_stats',
    'get_referral_performance_over_time',
]
