---
slug: webhooks-overview
title_i18n_key: Webhooks Overview
category: store-config
component: webhooks
keywords:
  - webhook
  - webhook endpoint
  - event notification
  - store integration
  - HTTP notification
  - order webhook
  - payment webhook
  - signing secret
  - HMAC signature
  - webhook events
  - real-time notification
  - third party integration
  - automation
url_patterns:
  - /admin/webhooks/webhookendpoint/
  - /admin/webhooks/webhookendpoint/add/
  - /admin/webhooks/webhookendpoint/\d+/change/
related:
  - webhook-deliveries
published: true
---

Webhooks let your store automatically notify external systems — such as inventory tools, ERPs, fulfilment services, or custom applications — whenever something happens in your store. Instead of those systems repeatedly asking "did anything change?", your store pushes a notification the moment an event occurs.

## What webhooks do

When an event happens in your store (an order is placed, a payment is received, a product goes out of stock), Spwig sends an HTTP POST request with the event data to a URL you configure. The receiving system can then act on that data immediately — for example, updating inventory, triggering a shipping label, or sending a custom notification.

Common uses for webhooks include:

- Syncing orders in real time with a fulfilment partner
- Updating inventory in an ERP when stock changes
- Triggering SMS or push notifications for order status changes
- Logging events in a data warehouse for reporting
- Connecting to automation tools like Zapier or Make

## Viewing and managing endpoints

Navigate to **Integrations > Webhooks** to see all your configured webhook endpoints.

![Webhook endpoints list](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

The list shows each endpoint's name, URL, active status, how many events it subscribes to, its health status, and when it last received a delivery.

### Health indicators

The **Health** column shows at a glance how well each endpoint is performing:

- **Healthy** — All recent deliveries have succeeded
- **Degraded** — Some recent failures but the endpoint is still active
- **Unhealthy / Disabled** — The endpoint was automatically disabled after too many consecutive failures (10 by default). You must manually re-enable it once the underlying issue is fixed.

## Creating a webhook endpoint

Click **+ Add Webhook Endpoint** to open the setup wizard. The wizard guides you through four steps.

### Step 1: Basic information

- **Name** — A friendly label to identify this endpoint (e.g., `Order Fulfilment Service` or `Inventory Sync`).
- **URL** — The full URL of the server that will receive the webhook POST requests. This must be publicly reachable (not a localhost URL).
- **Description** — Optional notes about what this endpoint is used for.
- **Active** — Whether this endpoint should receive deliveries. Uncheck to temporarily pause without deleting the endpoint.

### Step 2: Event subscriptions

Choose which events should trigger a delivery to this endpoint. Events are grouped by category:

#### Order events

| Event | When it fires |
|-------|---------------|
| `order.created` | A new order is placed |
| `order.paid` | Payment for an order is confirmed |
| `order.cancelled` | An order is cancelled |
| `order.fulfilled` | All items in an order are shipped |
| `order.partially_fulfilled` | Some items in an order are shipped |
| `order.status_changed` | The order status changes |
| `order.note_added` | A note is added to an order |

#### Payment events

| Event | When it fires |
|-------|---------------|
| `payment.received` | A payment is received |
| `payment.failed` | A payment attempt fails |
| `payment.pending` | A payment is awaiting confirmation |

#### Shipment events

| Event | When it fires |
|-------|---------------|
| `shipment.created` | A shipment is created |
| `shipment.shipped` | A shipment is dispatched |
| `shipment.delivered` | A shipment is delivered |
| `shipment.returned` | A shipment is returned |
| `shipment.tracking_updated` | Tracking information is updated |

#### Inventory events

| Event | When it fires |
|-------|---------------|
| `inventory.low_stock` | Stock falls below the threshold |
| `inventory.out_of_stock` | A product goes out of stock |
| `inventory.restocked` | A product is restocked |
| `inventory.adjusted` | Inventory is manually adjusted |

#### Product events

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

#### Customer events

`customer.created`, `customer.updated`, `customer.deleted`

#### Subscription events

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Other events

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

To receive all events, subscribe to `*` (wildcard). This is useful for general-purpose logging endpoints but creates more traffic — subscribe only to the events you actually need for production integrations.

### Step 3: Configuration

- **Max Retries** — How many times Spwig should retry a failed delivery before giving up (default: 5). Each retry uses exponential back-off spacing.
- **Timeout (Seconds)** — How long to wait for the receiving server to respond before marking the delivery as failed (default: 30 seconds). Increase this only if your server is known to be slow.

### Step 4: Security

Every webhook endpoint gets an automatically generated **signing secret** — a 64-character random key. Spwig uses this secret to sign every webhook payload with an HMAC-SHA256 signature.

The signature is included in the `X-Webhook-Signature` request header. Your receiving server should verify this signature to confirm that the request genuinely came from your store and was not tampered with.

The secret is shown masked in the admin. To see or rotate the secret, use the Spwig API. Rotate your secret immediately if you suspect it has been compromised.

## Enabling and disabling endpoints

To quickly enable or disable one or more endpoints without opening each one:

1. Select the checkboxes next to the endpoints you want to change
2. Use the **Action** dropdown to choose **Enable selected endpoints** or **Disable selected endpoints**
3. Click **Go**

To re-enable an endpoint that was automatically disabled by failures, select it and use the **Reset failure count** action, then re-enable it. Fix whatever caused the failures first, otherwise it will be disabled again quickly.

## Tips

- Subscribe only to the events you actually need — unnecessary events create noise in your logs and increase delivery load.
- Always verify the webhook signature in your receiving server before processing the payload. This protects you against spoofed requests.
- Use the **Description** field to record what system or integration this endpoint connects to. This helps when troubleshooting months later.
- Set a **Timeout** slightly above your server's typical response time. A timeout of 10–15 seconds is sufficient for most integrations.
- If an endpoint goes **Unhealthy**, check the delivery logs first (see **Webhook Deliveries**) to understand the failure pattern before re-enabling it.
- For testing, point webhooks at a tool like [webhook.site](https://webhook.site) to inspect the raw payloads without needing a live server.
