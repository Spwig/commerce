"""
Custom throttling classes for API rate limiting.

Implements comprehensive rate limiting to prevent abuse of public endpoints.
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class BurstRateThrottle(AnonRateThrottle):
    """
    Allows short bursts of requests from anonymous users.
    Used for endpoints that should allow quick successive calls but prevent sustained abuse.
    """
    scope = 'burst'


class SustainedRateThrottle(AnonRateThrottle):
    """
    Limits sustained request rate from anonymous users.
    Used in combination with burst throttle for comprehensive protection.
    """
    scope = 'sustained'


class PublicWriteThrottle(AnonRateThrottle):
    """
    Strict rate limiting for public write operations.
    Prevents spam and abuse of endpoints that create/modify data without authentication.
    """
    scope = 'public_write'


class VoucherValidationThrottle(UserRateThrottle):
    """
    Very strict rate limiting for voucher validation.
    Prevents brute-force enumeration of valid voucher codes.
    Applies to authenticated users (10 requests/minute).
    """
    scope = 'voucher_validation'


class ReferralTrackingThrottle(AnonRateThrottle):
    """
    Rate limiting for referral click tracking.
    Prevents token enumeration and fake click generation.
    """
    scope = 'referral_tracking'


class SocialTrackingThrottle(AnonRateThrottle):
    """
    Rate limiting for social sharing tracking.
    Prevents spam and database pollution from automated bots.
    """
    scope = 'social_tracking'


class AnonymousSocialTrackingThrottle(AnonRateThrottle):
    """
    Strict rate limiting for the anonymous social share tracking endpoint.

    The anonymous variant of share tracking is a public write endpoint
    available to guest visitors (unauthenticated headless frontends). It
    creates database rows without any user linkage, so it's a bigger spam
    target than the authenticated variant. Keep this rate low.
    """
    scope = 'social_tracking_anonymous'


class GeoIPThrottle(AnonRateThrottle):
    """
    Rate limiting for GeoIP resolution.
    Prevents abuse as a free IP lookup service.
    """
    scope = 'geoip'


class AuthenticatedUserThrottle(UserRateThrottle):
    """
    Rate limiting for authenticated users.
    More permissive than anonymous throttles but still prevents abuse.
    """
    scope = 'user'


class AuthenticatedBurstThrottle(UserRateThrottle):
    """
    Burst rate for authenticated users.
    Allows quick successive operations for normal user behavior.
    """
    scope = 'user_burst'


class MarketplaceCheckoutThrottle(AnonRateThrottle):
    """
    Strict rate limiting for marketplace checkout.
    Prevents abuse of financial operations (user creation, payment intent creation).
    Each request creates database records and calls external APIs.
    """
    scope = 'marketplace_checkout'


class MarketplaceStatusThrottle(AnonRateThrottle):
    """
    Rate limiting for marketplace payment status polling.
    Prevents enumeration and excessive polling.
    """
    scope = 'marketplace_status'


class POSAuthThrottle(AnonRateThrottle):
    """
    Rate limiting for POS login attempts.
    Prevents brute-force password attacks on POS terminals.
    """
    scope = 'pos_auth'


class POSPINThrottle(UserRateThrottle):
    """
    Rate limiting for POS PIN verification attempts.
    Prevents brute-force of 4-6 digit manager/cashier PINs.
    """
    scope = 'pos_pin'


class HostingWebhookThrottle(AnonRateThrottle):
    """
    Rate limiting for hosting provisioning webhooks from the update server.
    Prevents excessive email generation if the API key is compromised.
    """
    scope = 'hosting_webhook'
