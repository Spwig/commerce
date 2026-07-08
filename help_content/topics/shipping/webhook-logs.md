---
slug: webhook-logs
title_i18n_key: Webhook Logs
category: orders-shipping
component: shipping
keywords:
  - webhook logs
  - carrier webhooks
  - webhook debugging
  - API webhooks
  - webhook monitoring
  - webhook errors
  - carrier integration
  - webhook audit
  - tracking webhooks
url_patterns:
  - /admin/shipping/webhooklog/
related:
  - tracking-events
  - shipping-provider-accounts
published: true
---

Webhook logs provide permanent audit trail of all incoming carrier webhook requests—capturing request method, endpoint URL, headers, payload, processing status (pending/processed/failed), and response. Every webhook is logged before processing to ensure no events are lost if processing fails. Logs enable debugging webhook integration issues, monitoring carrier API reliability, and reconstructing delivery timelines for customer support.

This read-only admin page helps troubleshoot webhook failures and verify carrier integration health.

## Webhook Log Structure

Each log entry records:

**Request Details**:
- **Provider Key**: Which carrier sent webhook (fedex, ups, dhl)
- **Endpoint**: Webhook URL path (e.g., `/webhooks/shipping/fedex/`)
- **Method**: HTTP method (typically POST)
- **Headers**: Request headers (JSON)
- **Payload**: Request body (JSON)

**Processing**:
- **Processing Status**: pending, processed, failed
- **Error Message**: Failure reason (if status=failed)
- **Response**: HTTP response sent to carrier
- **Response Status Code**: 200, 400, 500, etc.

**Timestamps**:
- **Received At**: When webhook arrived
- **Processed At**: When processing completed

---

## Processing Status Values

**pending**: Webhook received, awaiting processing
- Normal for brief moment after receipt
- If stuck pending, indicates processing queue backlog

**processed**: Webhook successfully processed
- TrackingEvent created
- Customer notification sent (if applicable)
- Response 200 sent to carrier

**failed**: Webhook processing failed
- Check error_message for reason
- Common causes: Invalid JSON, unknown shipment, duplicate event

---

## Webhook Flow

**Normal Workflow**:
```
1. Carrier scans package
   ↓
2. Carrier sends POST to Spwig webhook endpoint
   ↓
3. Spwig creates WebhookLog (status=pending)
   ↓
4. Background worker processes webhook
   ↓
5. Parse JSON payload
   ↓
6. Find matching Shipment (by tracking number)
   ↓
7. Create TrackingEvent
   ↓
8. Update WebhookLog (status=processed)
   ↓
9. Send HTTP 200 response to carrier
```

**Failure Scenarios**:
- **Invalid JSON**: Carrier sent malformed data → status=failed, error="JSON parse error"
- **Unknown Shipment**: Tracking number doesn't match any shipment → status=failed, error="Shipment not found"
- **Duplicate**: Event already exists → status=failed, error="Duplicate event"

---

## Debugging Webhook Failures

**Step-by-Step**:

**1. Filter by Status=Failed**
- Navigate to Shipping > Webhook Logs
- Filter: Processing Status = "failed"
- Review recent failures

**2. Check Error Message**
- Click log entry
- Read error_message field
- Common errors:
  - "Shipment not found" → Tracking number mismatch
  - "JSON decode error" → Carrier sent invalid JSON
  - "Missing required field" → Payload missing expected data

**3. Inspect Payload**
- View raw JSON payload
- Verify structure matches expected format
- Check for missing fields (tracking_id, event_type, etc.)

**4. Verify Shipment Exists**
- Extract tracking number from payload
- Search Shipments for tracking number
- Ensure shipment exists and uses correct carrier

**5. Check Provider Configuration**
- Verify provider account active
- Confirm webhook endpoint URL correct
- Test provider API credentials

**6. Retry Processing** (if applicable)
- Some webhook processors support manual retry
- Fix underlying issue first
- Retry failed webhook

---

## Common Webhook Issues

**Issue 1: "Shipment not found"**

**Cause**: Tracking number in webhook doesn't match any shipment
- Typo when creating shipment
- Webhook for different account
- Shipment deleted before webhook received

**Solution**:
- Verify tracking number spelling
- Check shipment carrier matches webhook provider
- Recreate shipment if necessary

---

**Issue 2: "JSON decode error"**

**Cause**: Carrier sent malformed JSON
- Rare, usually carrier API bug
- Character encoding issues

**Solution**:
- Contact carrier support with raw payload
- Check headers for charset encoding
- Verify endpoint URL in carrier dashboard

---

**Issue 3: Duplicate webhooks**

**Cause**: Carrier sends same event multiple times
- Retry logic (carrier didn't receive 200 response)
- Carrier bug

**Solution**:
- System auto-rejects duplicates (normal behavior)
- Verify response_status_code is 200
- If persistent, contact carrier support

---

**Issue 4: Missing webhooks**

**Cause**: Expected webhook never received
- Carrier didn't send (scan missed)
- Webhook endpoint misconfigured in carrier dashboard
- Firewall blocking requests

**Solution**:
- Check carrier dashboard webhook configuration
- Verify endpoint URL public and reachable
- Test endpoint with curl/Postman
- Check server firewall rules

---

## Webhook Endpoint Configuration

**Typical Webhook URLs**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Carrier Dashboard Setup**:
1. Log into carrier developer portal
2. Navigate to webhook settings
3. Enter Spwig webhook URL
4. Select events to subscribe (tracking updates, delivery, exceptions)
5. Save configuration
6. Test webhook with carrier's test tool

**Security**:
- Webhooks require HTTPS (not HTTP)
- Some carriers sign requests (verify signature)
- IP whitelist (if carrier provides static IPs)

---

## Monitoring Webhook Health

**Key Metrics**:

**Success Rate**:
```
Success Rate = (Processed / Total) × 100%

Target: >98%
```

**Processing Time**:
```
Avg Time = Processed At - Received At

Target: <2 seconds
```

**Failure Patterns**:
- Sudden spike in failures → Carrier API change or outage
- Consistent "shipment not found" → Tracking number sync issue
- All webhooks failed → Endpoint configuration problem

**Monitoring Strategy**:
- Check failure rate daily
- Alert if failure rate >5%
- Review error messages weekly
- Compare against carrier status page

---

## Webhook Retention

**Logs are permanent** - never auto-deleted

**Why Permanent**:
- Audit compliance
- Customer support (reconstruct delivery timeline)
- Dispute resolution
- Webhook debugging

**Storage**: Logs stored efficiently (compressed JSON)

---

## Tips

- **Webhooks are permanent audit log** - Never delete, even if processed successfully
- **Check failed webhooks daily** - Catch integration issues early
- **Monitor processing lag** - Long delay indicates performance issue
- **Save raw payloads** - Essential for debugging carrier API changes
- **Test endpoint configuration** - Use carrier test tools to verify setup
- **Enable webhook signing** - Verify requests actually from carrier
- **Whitelist carrier IPs** - If carrier provides static IP ranges
- **Set up alerts** - Notify when failure rate exceeds threshold
- **Compare with carrier status** - Webhook gaps may indicate carrier outage
- **Document carrier payload formats** - Helps when carrier updates API
- **Keep webhook URLs stable** - Changing URLs requires carrier dashboard update
