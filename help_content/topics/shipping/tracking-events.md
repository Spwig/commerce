---
slug: tracking-events
title_i18n_key: Tracking Events
category: orders-shipping
component: shipping
keywords:
  - tracking events
  - shipment tracking
  - delivery status
  - tracking updates
  - carrier events
  - tracking history
  - shipment status
  - delivery tracking
  - tracking checkpoints
url_patterns:
  - /admin/shipping/trackingevent/
related:
  - webhook-logs
  - carrier-presets
  - shipping-provider-accounts
published: true
---

Tracking events record shipment status checkpoints throughout delivery lifecycle—each event captures status (in transit, out for delivery, delivered), timestamp, location, description, and raw carrier data. Events are created automatically via carrier webhook notifications or manually by merchants. Customers see tracking event history in their account and order confirmation emails, providing real-time delivery visibility.

This admin page displays read-only event history for audit and customer support purposes.

## Tracking Event Structure

Each event contains:

**Status Information**:
- **Status**: in_transit, out_for_delivery, delivered, exception, failed, returned
- **Description**: Human-readable status (e.g., "Package arrived at sorting facility")
- **Carrier Status Code**: Original carrier status (e.g., "DEP" for departed)

**Location Data**:
- **City**: Event location city
- **State**: Event location state/province
- **Country**: Event location country
- **Postal Code**: Event location ZIP/postal code

**Timestamps**:
- **Occurred At**: When event actually happened (carrier time)
- **Created At**: When event recorded in Spwig (system time)

**Metadata**:
- **Raw Data**: Full JSON response from carrier API
- **Shipment**: Linked shipment ID

---

## Event Status Types

**in_transit**: Package moving through carrier network
- Examples: "Departed facility", "Arrived at hub", "In transit to next facility"

**out_for_delivery**: Package on delivery vehicle
- Examples: "Out for delivery", "On delivery vehicle"

**delivered**: Package successfully delivered
- Examples: "Delivered to front door", "Left at reception", "Handed to recipient"

**exception**: Delivery issue requiring attention
- Examples: "Weather delay", "Incorrect address", "Delivery attempt failed"

**failed**: Delivery failed permanently
- Examples: "Undeliverable as addressed", "Refused by recipient"

**returned**: Package being returned to sender
- Examples: "Return to sender initiated", "Package returning"

---

## How Tracking Events Are Created

### Automatic (Carrier Webhooks)

**Workflow**:
1. Carrier scans package (departure, arrival, delivery)
2. Carrier sends webhook to Spwig webhook endpoint
3. Webhook logged in WebhookLog table
4. System parses webhook payload
5. TrackingEvent created with extracted data
6. Customer email notification sent (if configured)

**Benefits**:
- Real-time updates (no polling needed)
- Accurate timestamps from carrier
- Full event history automatically maintained

### Manual (Merchant Entry)

**Workflow**:
1. Navigate to Shipment detail
2. Click "Add Tracking Event"
3. Select status from dropdown
4. Enter description
5. Optional: Enter location data
6. Set occurred_at timestamp
7. Save

**Use Cases**:
- Carriers without webhook support
- Manual shipment corrections
- Local delivery (non-carrier)
- Internal status updates

---

## Event Display Order

Events displayed in **reverse chronological order** (newest first):

**Example Display**:
```
Feb 13, 2026 10:30 AM - Delivered (Brooklyn, NY)
Feb 13, 2026 08:15 AM - Out for delivery (Brooklyn, NY)
Feb 12, 2026 11:45 PM - Arrived at local facility (Brooklyn, NY)
Feb 12, 2026 06:30 PM - In transit (Newark, NJ)
Feb 12, 2026 02:15 PM - Departed origin (Philadelphia, PA)
Feb 12, 2026 09:00 AM - Picked up (Philadelphia, PA)
```

---

## Customer Visibility

Tracking events shown to customers in:

**Order Confirmation Email**:
- Latest event status
- Estimated delivery date
- Tracking link

**Customer Account > Order Details**:
- Full event timeline
- Event descriptions
- Location history
- Timestamps

**Tracking Page** (if enabled):
- Dedicated tracking URL
- Visual timeline
- Carrier logo
- Delivery map (if location data available)

---

## Filtering Tracking Events

**Useful Filters**:
- **Shipment**: View events for specific shipment
- **Status**: Filter by event type (delivered, in_transit, etc.)
- **Date Range**: Events within timeframe
- **Location**: Events in specific city/state

**Use Cases**:
- "Show all delivered shipments today"
- "Find all exceptions in last week"
- "Track shipments currently in_transit"

---

## Raw Data (Debugging)

**Raw Data Field**:
- Stores complete carrier API response as JSON
- Useful for debugging webhook issues
- Contains carrier-specific metadata

**Example Raw Data** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Out for delivery",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**When To Check Raw Data**:
- Event description unclear
- Missing location data
- Webhook processing errors
- Carrier support escalation

---

## Event Timing

**Occurred At** vs **Created At**:

**Occurred At**: When carrier event actually happened
- Example: Package scanned at 10:30 AM

**Created At**: When Spwig received webhook
- Example: Webhook received at 10:32 AM (2 min delay)

**Why Different?**:
- Network latency
- Carrier batch processing
- Webhook retry delays

**Use Occurred At for customer display** - more accurate reflection of actual delivery progress.

---

## Tips

- **Events are read-only** - Cannot edit after creation (audit integrity)
- **Check raw data for details** - More info than displayed fields
- **Monitor webhook lag** - Large delay between occurred_at and created_at indicates webhook issues
- **Use for customer support** - Event timeline helps diagnose delivery issues
- **Track delivery patterns** - Analyze event timing for carrier performance
- **Set up notifications** - Auto-email customers on key events (out_for_delivery, delivered)
- **Don't delete events** - Preserve full audit trail
- **Check WebhookLog for failures** - Missing events may indicate webhook processing errors
- **Location data varies by carrier** - Some carriers provide detailed location, others minimal
- **Exception events need attention** - Monitor and follow up on delivery exceptions
