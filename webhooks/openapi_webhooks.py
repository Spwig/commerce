"""
OpenAPI webhook definitions for documentation.

This module provides webhook schema definitions that appear in
the OpenAPI/Swagger documentation alongside REST API endpoints.

Note: These are documentation-only - they describe what webhooks
merchants will receive, not endpoints they call.
"""
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import serializers


# =============================================================================
# Webhook Payload Schemas (for documentation)
# =============================================================================

class WebhookPayloadBase(serializers.Serializer):
    """Base schema for all webhook payloads."""
    event = serializers.CharField(help_text="The event type (e.g., 'order.created')")
    created_at = serializers.DateTimeField(help_text="When the event occurred (ISO 8601)")


class OrderWebhookData(serializers.Serializer):
    """Schema for order data in webhooks."""
    id = serializers.IntegerField(help_text="Order ID")
    order_number = serializers.CharField(help_text="Human-readable order number")
    status = serializers.CharField(help_text="Order status (pending, processing, shipped, delivered, cancelled, refunded)")
    total = serializers.DecimalField(max_digits=12, decimal_places=2, help_text="Order total amount")
    currency = serializers.CharField(help_text="3-letter currency code")
    customer_email = serializers.EmailField(help_text="Customer email address")
    customer_id = serializers.IntegerField(help_text="Customer ID", allow_null=True)
    items_count = serializers.IntegerField(help_text="Number of items in order")
    created_at = serializers.DateTimeField(help_text="Order creation time")
    updated_at = serializers.DateTimeField(help_text="Last update time")


class ProductWebhookData(serializers.Serializer):
    """Schema for product data in webhooks."""
    id = serializers.IntegerField(help_text="Product ID")
    sku = serializers.CharField(help_text="Product SKU")
    name = serializers.CharField(help_text="Product name")
    slug = serializers.CharField(help_text="URL slug")
    status = serializers.CharField(help_text="Product status")
    price = serializers.DecimalField(max_digits=12, decimal_places=2, help_text="Regular price", allow_null=True)
    sale_price = serializers.DecimalField(max_digits=12, decimal_places=2, help_text="Sale price", allow_null=True)
    stock_quantity = serializers.IntegerField(help_text="Current stock quantity", allow_null=True)
    is_published = serializers.BooleanField(help_text="Whether product is published")
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CustomerWebhookData(serializers.Serializer):
    """Schema for customer data in webhooks."""
    id = serializers.IntegerField(help_text="Customer ID")
    email = serializers.EmailField(help_text="Customer email")
    first_name = serializers.CharField(help_text="First name")
    last_name = serializers.CharField(help_text="Last name")
    created_at = serializers.DateTimeField(help_text="Registration time")


class ShipmentWebhookData(serializers.Serializer):
    """Schema for shipment data in webhooks."""
    id = serializers.IntegerField(help_text="Shipment ID")
    order_id = serializers.IntegerField(help_text="Associated order ID")
    order_number = serializers.CharField(help_text="Order number")
    tracking_number = serializers.CharField(help_text="Carrier tracking number")
    carrier = serializers.CharField(help_text="Shipping carrier name", allow_null=True)
    status = serializers.CharField(help_text="Shipment status")
    shipped_at = serializers.DateTimeField(help_text="Ship date", allow_null=True)
    delivered_at = serializers.DateTimeField(help_text="Delivery date", allow_null=True)
    created_at = serializers.DateTimeField()


class InventoryWebhookData(serializers.Serializer):
    """Schema for inventory event data in webhooks."""
    product_id = serializers.IntegerField(help_text="Product ID")
    product_sku = serializers.CharField(help_text="Product SKU")
    product_name = serializers.CharField(help_text="Product name")
    previous_stock = serializers.IntegerField(help_text="Stock level before change")
    current_stock = serializers.IntegerField(help_text="Stock level after change")
    low_stock_threshold = serializers.IntegerField(help_text="Configured low stock threshold", allow_null=True)


class SubscriptionWebhookData(serializers.Serializer):
    """Schema for subscription data in webhooks."""
    id = serializers.IntegerField(help_text="Subscription ID")
    customer_id = serializers.IntegerField(help_text="Customer ID")
    customer_email = serializers.EmailField(help_text="Customer email")
    plan_name = serializers.CharField(help_text="Subscription plan name")
    status = serializers.CharField(help_text="Subscription status")
    current_period_start = serializers.DateTimeField()
    current_period_end = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


# =============================================================================
# Webhook Documentation Strings
# =============================================================================

WEBHOOK_SIGNATURE_DOCS = """
## Signature Verification

All webhooks are signed using HMAC-SHA256. To verify a webhook:

1. Extract the timestamp and signature from the `X-Spwig-Signature` header:
   ```
   X-Spwig-Signature: t=1234567890,v1=abc123def456...
   ```

2. Compute the expected signature:
   ```
   signature_payload = f"{timestamp}.{raw_request_body}"
   expected = hmac.sha256(your_secret, signature_payload).hexdigest()
   ```

3. Compare signatures using constant-time comparison.

4. Verify the timestamp is within 5 minutes to prevent replay attacks.

### Headers Sent

| Header | Description |
|--------|-------------|
| `X-Spwig-Signature` | `t={timestamp},v1={signature}` |
| `X-Spwig-Event` | Event type (e.g., `order.created`) |
| `X-Spwig-Delivery-Id` | Unique delivery ID (UUID) |
| `X-Spwig-Timestamp` | Unix timestamp |
| `Content-Type` | `application/json; charset=utf-8` |
| `User-Agent` | `Spwig-Webhooks/1.0` |

### Retry Behavior

Failed deliveries are retried with exponential backoff:
- Attempt 1: Immediate
- Attempt 2: 1 minute
- Attempt 3: 2 minutes
- Attempt 4: 4 minutes
- Attempt 5: 8 minutes

Webhooks expecting 2xx response are considered successful.
After 5 failed attempts, the delivery is marked as failed.
After 10 consecutive failures, the endpoint is auto-disabled.

### Code Examples

**Python:**
```python
import hmac
import hashlib

def verify_webhook(payload, signature_header, secret):
    parts = dict(p.split('=', 1) for p in signature_header.split(','))
    timestamp = parts['t']
    signature = parts['v1']

    expected = hmac.new(
        secret.encode(),
        f"{timestamp}.{payload}".encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
```

**Node.js:**
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signatureHeader, secret) {
    const parts = Object.fromEntries(
        signatureHeader.split(',').map(p => p.split('='))
    );
    const timestamp = parts.t;
    const signature = parts.v1;

    const expected = crypto
        .createHmac('sha256', secret)
        .update(`${timestamp}.${payload}`)
        .digest('hex');

    return crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expected)
    );
}
```
"""


# =============================================================================
# Webhook Event Documentation
# =============================================================================

def get_webhook_documentation():
    """
    Get documentation content for webhook events.

    This can be used to generate documentation pages or
    include in API responses.
    """
    from .events import get_events_by_category

    docs = {
        'overview': '''
# Webhooks

Spwig webhooks allow you to receive real-time HTTP notifications when
events occur in your store. This enables you to build integrations,
sync data with external systems, and automate workflows.

## Getting Started

1. Create a webhook endpoint in your admin dashboard
2. Subscribe to the events you want to receive
3. Implement signature verification in your receiver
4. Handle the webhook payloads

## Best Practices

- Always verify webhook signatures
- Respond quickly (within 30 seconds) with 2xx status
- Process webhooks asynchronously if needed
- Handle duplicate deliveries idempotently
- Store the delivery ID to detect duplicates
''',
        'signature_verification': WEBHOOK_SIGNATURE_DOCS,
        'events_by_category': get_events_by_category(),
    }

    return docs


# =============================================================================
# Schema Generation Helpers
# =============================================================================

def get_webhook_payload_schema(event_type: str):
    """
    Get the appropriate payload schema for an event type.

    Args:
        event_type: The webhook event type

    Returns:
        Serializer class for the payload
    """
    prefix = event_type.split('.')[0] if '.' in event_type else event_type

    schemas = {
        'order': OrderWebhookData,
        'product': ProductWebhookData,
        'customer': CustomerWebhookData,
        'shipment': ShipmentWebhookData,
        'inventory': InventoryWebhookData,
        'subscription': SubscriptionWebhookData,
    }

    return schemas.get(prefix, serializers.DictField)
