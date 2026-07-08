"""
Communication preference constants for email and SMS message types.

This module defines the taxonomy of communication types across the platform,
used for permission checking and preference management.
"""

# Transactional emails (always on, not user-controllable)
# These are essential for account and order management
TRANSACTIONAL_EMAIL_TYPES = [
    'account_invitation',
    'order_confirmation',
    'order_shipped',
    'order_delivered',
    'payment_confirmation',
    'payment_failed',
    'refund_notification',
    'password_reset',
    'email_verification',
    'account_verification',
    'subscription_payment_success',
    'subscription_payment_failed',
    'pos_receipt',
    'license_purchase_confirmation',
    'license_trial_welcome',
    'order_cancelled',
    'order_note_notification',
    'order_status_update',
    'return_request_approved',
    'return_request_rejected',
    'return_received',
    'return_refund_processed',
    'staff_invitation',
    'hosted_subscription_confirmation',
    'hosted_provision_complete',
    'hosted_provision_failed',
    'hosted_onboarding_tips',
    'hosted_onboarding_day3',
    'hosted_onboarding_day7',
    'hosted_onboarding_day14',
]

# Marketing emails (user-controllable, default opt-out per GDPR)
MARKETING_EMAIL_TYPES = [
    'newsletter',
    'promotional_offers',
    'product_recommendations',
    'back_in_stock',
]

# App-specific email types (user-controllable per app)
# Each app can define its own communication types
APP_EMAIL_TYPES = {
    'blog': [
        'blog_post_published',
        'blog_weekly_digest',
        'blog_monthly_digest',
    ],
    'loyalty': [
        'loyalty_points_earned',
        'loyalty_tier_upgraded',
        'loyalty_tier_downgraded',
        'loyalty_reward_unlocked',
        'loyalty_points_expiring',
        'loyalty_points_expired',
        'loyalty_birthday_bonus',
        'loyalty_anniversary_bonus',
        'loyalty_campaign_offer',
    ],
    'referrals': [
        'referral_reward_issued_referrer',
        'referral_reward_issued_referee',
        'referral_successful',
        'referral_reward_expiring',
        'referral_invitation',
    ],
    'affiliate': [
        'affiliate_commission_earned',
        'affiliate_commission_approved',
        'affiliate_commission_rejected',
        'affiliate_payout_processed',
        'affiliate_payout_completed',
        'affiliate_payout_failed',
        'affiliate_monthly_report',
    ],
}

# SMS message types (all require opt-in per TCPA compliance)
TRANSACTIONAL_SMS_TYPES = [
    'order_confirmation',
    'order_shipped',
    'order_delivered',
    'delivery_notification',
    'password_reset',
    'verification_code',
]

MARKETING_SMS_TYPES = [
    'promotional_offers',
    'flash_sales',
    'marketing',
]

# All message types combined (for validation)
ALL_EMAIL_TYPES = (
    TRANSACTIONAL_EMAIL_TYPES +
    MARKETING_EMAIL_TYPES +
    [msg for msgs in APP_EMAIL_TYPES.values() for msg in msgs]
)

ALL_SMS_TYPES = TRANSACTIONAL_SMS_TYPES + MARKETING_SMS_TYPES


def get_message_type_category(message_type):
    """
    Determine the category of a message type.

    Args:
        message_type: Email or SMS message type string

    Returns:
        Tuple of (category, app) where category is 'transactional', 'marketing', or 'app_specific'
        and app is the app name if app_specific, else None
    """
    if message_type in TRANSACTIONAL_EMAIL_TYPES or message_type in TRANSACTIONAL_SMS_TYPES:
        return ('transactional', None)

    if message_type in MARKETING_EMAIL_TYPES or message_type in MARKETING_SMS_TYPES:
        return ('marketing', None)

    for app, types in APP_EMAIL_TYPES.items():
        if message_type in types:
            return ('app_specific', app)

    # Unknown type - treat as transactional (safer default)
    return ('transactional', None)


def is_locked_message_type(message_type):
    """
    Check if a message type is locked (not user-controllable).

    Transactional messages are locked for security and compliance reasons.
    """
    return message_type in TRANSACTIONAL_EMAIL_TYPES or message_type in TRANSACTIONAL_SMS_TYPES
