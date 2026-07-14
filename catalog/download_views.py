"""
Digital Product Download Delivery Views

Handles secure file streaming for digital product downloads with:
- Token-based authentication
- Download limit enforcement
- Rate limiting
- Progress tracking
- File streaming from MinIO
"""

import logging

from django.core.cache import cache
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from catalog.models import DigitalAsset, DigitalDownload
from orders.models import OrderItem

logger = logging.getLogger(__name__)


def generate_download_token(asset_id: int, order_item_id: int) -> str:
    """
    Generate a signed download token for a digital asset.

    Token format: "{asset_id}:{order_item_id}:{timestamp}"

    Args:
        asset_id: DigitalAsset ID
        order_item_id: OrderItem ID

    Returns:
        Signed token string
    """
    signer = TimestampSigner()
    token_data = f"{asset_id}:{order_item_id}"
    signed_token = signer.sign(token_data)
    return signed_token


def verify_download_token(signed_token: str, max_age: int = 3600) -> tuple:
    """
    Verify and decode a download token.

    Args:
        signed_token: Signed token from URL
        max_age: Maximum age in seconds (default: 1 hour)

    Returns:
        Tuple of (asset_id, order_item_id) or None if invalid

    Raises:
        SignatureExpired: If token has expired
        BadSignature: If token is invalid
    """
    signer = TimestampSigner()
    token_data = signer.unsign(signed_token, max_age=max_age)
    asset_id, order_item_id = token_data.split(":")
    return int(asset_id), int(order_item_id)


def check_rate_limit(ip_address: str, asset_id: int) -> bool:
    """
    Check if download request exceeds rate limit.

    Rate limit: 10 downloads per hour per IP per asset

    Args:
        ip_address: Client IP address
        asset_id: DigitalAsset ID

    Returns:
        True if rate limit exceeded, False otherwise
    """
    cache_key = f"download_rate_limit:{ip_address}:{asset_id}"

    # Get current request count
    request_count = cache.get(cache_key, 0)

    # Check if exceeded
    if request_count >= 10:
        logger.warning(
            f"Rate limit exceeded for IP {ip_address} on asset {asset_id} "
            f"({request_count} requests)"
        )
        return True

    # Increment counter
    cache.set(cache_key, request_count + 1, 3600)  # 1 hour TTL
    return False


def get_client_ip(request) -> str:
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    return ip


def file_iterator(file_handle, chunk_size=8192):
    """
    Generator that yields file chunks for streaming.

    Args:
        file_handle: File object to read from
        chunk_size: Size of each chunk in bytes (default: 8KB)

    Yields:
        File chunks
    """
    try:
        while True:
            chunk = file_handle.read(chunk_size)
            if not chunk:
                break
            yield chunk
    finally:
        file_handle.close()


@never_cache
@require_http_methods(["GET"])
def download_digital_asset(request, token):
    """
    Download digital asset with token-based authentication.

    Security features:
    - Signed token with expiration (1 hour)
    - Ownership verification
    - Download limit enforcement
    - Rate limiting (10/hour per IP)
    - Purchase expiration checking

    Args:
        request: HTTP request
        token: Signed download token

    Returns:
        StreamingHttpResponse with file data
    """
    try:
        # Verify token
        try:
            asset_id, order_item_id = verify_download_token(token, max_age=3600)
        except SignatureExpired:
            logger.warning(f"Expired download token: {token}")
            return HttpResponse(
                "Download link has expired. Please request a new download link from your account.",
                status=410,  # Gone
            )
        except BadSignature:
            logger.warning(f"Invalid download token: {token}")
            return HttpResponse(
                "Invalid download link.",
                status=400,  # Bad Request
            )
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return HttpResponse("Invalid download link.", status=400)

        # Get client IP for rate limiting
        client_ip = get_client_ip(request)

        # Check rate limit
        if check_rate_limit(client_ip, asset_id):
            return HttpResponse(
                "Too many download attempts. Please try again in an hour.",
                status=429,  # Too Many Requests
            )

        # Get digital asset
        try:
            asset = DigitalAsset.objects.get(pk=asset_id, is_active=True)
        except DigitalAsset.DoesNotExist:
            logger.warning(f"Digital asset {asset_id} not found or inactive")
            raise Http404("Digital product not found")

        # Get order item
        try:
            order_item = OrderItem.objects.select_related("order").get(pk=order_item_id)
        except OrderItem.DoesNotExist:
            logger.warning(f"Order item {order_item_id} not found")
            raise Http404("Order not found")

        # Verify ownership (order item matches asset)
        if order_item.product_id != asset.product_id:
            logger.warning(
                f"Ownership mismatch: order_item {order_item_id} does not own asset {asset_id}"
            )
            return HttpResponse(
                "You do not have access to this digital product.",
                status=403,  # Forbidden
            )

        # Verify order status
        if order_item.order.status not in ["processing", "completed", "delivered"]:
            logger.warning(
                f"Invalid order status for download: {order_item.order.status} "
                f"(order: {order_item.order.order_number})"
            )
            return HttpResponse("This order is not eligible for download yet.", status=403)

        # Check download limit
        if asset.is_download_limit_exceeded(order_item):
            download_count = asset.downloads.filter(order_item=order_item).count()
            logger.warning(
                f"Download limit exceeded for asset {asset_id} "
                f"({download_count}/{asset.download_limit})"
            )
            return HttpResponse(
                f"Download limit exceeded ({asset.download_limit} downloads allowed).", status=403
            )

        # Check expiration
        if asset.is_download_expired(order_item.order.created_at):
            logger.warning(
                f"Download expired for asset {asset_id} (purchased: {order_item.order.created_at})"
            )
            return HttpResponse(
                "Download access has expired.",
                status=410,  # Gone
            )

        # Create or get download record
        download = DigitalDownload.create_download_record(
            digital_asset=asset,
            order_item=order_item,
            user=order_item.order.user,
            ip_address=client_ip,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

        logger.info(
            f"Starting download: asset={asset_id}, order={order_item.order.order_number}, "
            f"ip={client_ip}, download_id={download.id}"
        )

        # Open file from MinIO storage
        try:
            file_handle = asset.file.open("rb")
        except Exception as e:
            logger.error(f"Failed to open file from MinIO for asset {asset_id}: {e}")
            download.mark_failed(str(e))
            return HttpResponse(
                "Failed to retrieve digital product. Please contact support.", status=500
            )

        # Determine MIME type
        content_type = asset.file_type or "application/octet-stream"

        # Create streaming response
        response = StreamingHttpResponse(file_iterator(file_handle), content_type=content_type)

        # Set headers for download
        response["Content-Disposition"] = f'attachment; filename="{asset.filename}"'
        response["Content-Length"] = asset.file_size
        response["X-Download-ID"] = download.id

        # Add caching headers (no caching)
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        # Mark download as completed (optimistic - assumes successful stream)
        # In production, you might want to track this via middleware or signals
        download.mark_completed()

        logger.info(
            f"Download started successfully: asset={asset.filename}, "
            f"size={asset.get_file_size_display()}, download_id={download.id}"
        )

        return response

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in download_digital_asset: {e}", exc_info=True)
        return HttpResponse(
            "An error occurred while processing your download. Please contact support.", status=500
        )
