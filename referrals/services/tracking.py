"""
Referral tracking service.

Handles click tracking, cookie management, signup/order event logging.
"""

import hashlib
import secrets
from datetime import timedelta
from io import BytesIO

from django.utils import timezone

from ..models import ReferralEvent, ReferralIdentity, ReferralProgram


def generate_token(length=12):
    """
    Generate a secure random token for referral links.

    Args:
        length (int): Length of the token (default 12 characters)

    Returns:
        str: Secure random token
    """
    return secrets.token_urlsafe(length)[:length]


def generate_qr_code(identity):
    """
    Generate QR code image for referral identity.

    Args:
        identity (ReferralIdentity): Referral identity instance

    Returns:
        BytesIO: QR code image buffer
    """
    try:
        import qrcode
    except ImportError:
        # QR code library not installed, return None
        return None

    # Get referral link
    referral_link = identity.get_referral_link()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(referral_link)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def track_click(token, request):
    """
    Log referral link click event and set tracking cookie.

    Args:
        token (str): Referral token from URL parameter
        request (HttpRequest): HTTP request object

    Returns:
        tuple: (success: bool, identity: ReferralIdentity or None, message: str)
    """
    try:
        # Get referral identity
        identity = ReferralIdentity.objects.select_related("customer").get(token=token)
    except ReferralIdentity.DoesNotExist:
        return False, None, "Invalid referral token"

    # Get program
    program = ReferralProgram.get_program()

    if not program.is_active():
        return False, None, "Referral program is not active"

    # Extract tracking data from request
    tracking_data = _extract_tracking_data(request)

    # Log click event
    ReferralEvent.log_event(
        event_type="click", program=program, referrer_identity=identity, **tracking_data
    )

    # Increment click counter
    identity.increment_clicks()

    return True, identity, "Click tracked successfully"


def track_signup(customer, request):
    """
    Log referral signup event when new customer creates account.

    Args:
        customer (User): Newly created customer
        request (HttpRequest): HTTP request object

    Returns:
        tuple: (success: bool, identity: ReferralIdentity or None, message: str)
    """
    # Get referral token from cookie
    token = get_ref_token_from_cookie(request)

    if not token:
        return False, None, "No referral cookie found"

    try:
        # Get referral identity
        identity = ReferralIdentity.objects.select_related("customer").get(token=token)
    except ReferralIdentity.DoesNotExist:
        return False, None, "Invalid referral token"

    # Get program
    program = ReferralProgram.get_program()

    # Extract tracking data
    tracking_data = _extract_tracking_data(request)

    # Log signup event
    ReferralEvent.log_event(
        event_type="signup",
        program=program,
        referrer_identity=identity,
        customer=customer,
        **tracking_data,
    )

    # Increment signup counter
    identity.increment_signups()

    return True, identity, "Signup tracked successfully"


def track_order(order, request):
    """
    Log referral order event when customer completes first purchase.

    This should be called from order completion signal.

    Args:
        order (Order): Completed order
        request (HttpRequest): HTTP request object (if available)

    Returns:
        tuple: (success: bool, identity: ReferralIdentity or None, message: str)
    """
    # Get referral token from cookie
    token = get_ref_token_from_cookie(request) if request else None

    if not token:
        return False, None, "No referral cookie found"

    try:
        # Get referral identity
        identity = ReferralIdentity.objects.select_related("customer").get(token=token)
    except ReferralIdentity.DoesNotExist:
        return False, None, "Invalid referral token"

    # Check if this is referrer's own order (self-referral)
    if identity.customer == order.user:
        return False, None, "Self-referral not allowed"

    # Get program
    program = ReferralProgram.get_program()

    # Extract tracking data
    tracking_data = _extract_tracking_data(request) if request else {}

    # Log order event
    ReferralEvent.log_event(
        event_type="order",
        program=program,
        referrer_identity=identity,
        customer=order.user,
        order=order,
        **tracking_data,
    )

    return True, identity, "Order tracked successfully"


def get_ref_token_from_cookie(request):
    """
    Extract referral token from cookie.

    Args:
        request (HttpRequest): HTTP request object

    Returns:
        str or None: Referral token if found
    """
    return request.COOKIES.get("ref_token")


def set_ref_cookie(response, token, ttl_days=30):
    """
    Set referral tracking cookie on response.

    Args:
        response (HttpResponse): HTTP response object
        token (str): Referral token to store
        ttl_days (int): Cookie TTL in days (default 30)

    Returns:
        HttpResponse: Response with cookie set
    """
    max_age = ttl_days * 24 * 60 * 60  # Convert days to seconds
    expires = timezone.now() + timedelta(days=ttl_days)

    response.set_cookie(
        key="ref_token",
        value=token,
        max_age=max_age,
        expires=expires,
        httponly=True,
        samesite="Lax",
        secure=False,  # Set to True in production with HTTPS
    )

    return response


def hash_ip_address(ip_address):
    """
    Hash IP address for privacy.

    Args:
        ip_address (str): IP address to hash

    Returns:
        str: Hashed IP address (first 16 chars of SHA256)
    """
    if not ip_address:
        return ""

    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]


def hash_device_fingerprint(user_agent, ip_address):
    """
    Generate device fingerprint from user agent and IP.

    Args:
        user_agent (str): Browser user agent string
        ip_address (str): IP address

    Returns:
        str: Device fingerprint hash
    """
    fingerprint_string = f"{user_agent}:{ip_address}"
    return hashlib.sha256(fingerprint_string.encode()).hexdigest()[:32]


def _extract_tracking_data(request):
    """
    Extract tracking data from HTTP request.

    Args:
        request (HttpRequest): HTTP request object

    Returns:
        dict: Tracking data for event logging
    """
    # Get IP address
    ip_address = _get_client_ip(request)

    # Get user agent
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # Generate device fingerprint
    device_fingerprint = hash_device_fingerprint(user_agent, ip_address)

    # Get referrer URL
    referrer_url = request.META.get("HTTP_REFERER", "")

    # Get landing URL
    landing_url = request.build_absolute_uri()

    # Extract UTM parameters
    utm_params = {
        "utm_source": request.GET.get("utm_source", ""),
        "utm_medium": request.GET.get("utm_medium", ""),
        "utm_campaign": request.GET.get("utm_campaign", ""),
        "utm_term": request.GET.get("utm_term", ""),
        "utm_content": request.GET.get("utm_content", ""),
    }

    # Remove empty UTM params
    utm_params = {k: v for k, v in utm_params.items() if v}

    return {
        "ip_address": hash_ip_address(ip_address),  # Store hashed IP for privacy
        "user_agent": user_agent,
        "device_fingerprint": device_fingerprint,
        "referrer_url": referrer_url,
        "landing_url": landing_url,
        "metadata": {
            "utm": utm_params,
            "browser": _parse_user_agent(user_agent),
        },
    }


def _get_client_ip(request):
    """
    Get client IP address from request.

    Args:
        request (HttpRequest): HTTP request object

    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
    return ip


def _parse_user_agent(user_agent):
    """
    Parse user agent string to extract browser info.

    Args:
        user_agent (str): User agent string

    Returns:
        dict: Parsed browser info (basic)
    """
    # Basic user agent parsing (can be enhanced with user-agents library)
    browser_info = {
        "is_mobile": "Mobile" in user_agent or "Android" in user_agent,
        "is_tablet": "Tablet" in user_agent or "iPad" in user_agent,
        "is_desktop": "Windows" in user_agent or "Macintosh" in user_agent or "Linux" in user_agent,
    }

    return browser_info
