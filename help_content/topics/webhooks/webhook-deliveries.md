---
slug: webhook-deliveries
title_i18n_key: Webhook Delivery Logs
category: store-config
component: webhooks
keywords:
  - webhook delivery
  - webhook log
  - delivery status
  - failed webhook
  - retry webhook
  - webhook debugging
  - webhook response
  - webhook payload
  - webhook history
  - delivery attempt
  - HTTP response code
  - webhook error
url_patterns:
  - /admin/webhooks/webhookdelivery/
related:
  - webhooks-overview
published: true
---

Every time your store attempts to send a webhook, a delivery log entry is created. These logs let you see exactly what was sent, whether it succeeded, and what happened during any retry attempts. This guide explains how to read the delivery logs and debug problems when deliveries fail.

## Viewing delivery logs

Navigate to **Integrations > Webhook Deliveries** to see the complete history of all webhook delivery attempts across all your endpoints.

![Webhook delivery logs](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

The list shows each delivery's endpoint name, event type, status, HTTP response code, response time, and how many attempts were made.

Delivery logs are read-only — they are created automatically when events fire and cannot be edited.

## Delivery statuses

Each delivery has one of these statuses:

| Status | What it means |
|--------|---------------|
| **Pending** | The delivery is queued and has not been attempted yet |
| **Success** | The receiving server responded with an HTTP 2xx status code — delivery confirmed |
| **Failed** | All delivery attempts have been exhausted — the delivery will not be retried again |
| **Retrying** | The most recent attempt failed, but the system will try again at the scheduled retry time |
| **Sandbox Blocked** | The delivery was blocked because the endpoint URL is not accessible in the current environment |

A delivery is considered successful when the receiving server returns any HTTP 2xx response code (200, 201, 202, etc.). Any other response — including 3xx redirects or 4xx/5xx errors — is treated as a failure.

## Filtering deliveries

Use the filter panel on the right to narrow down the list:

- **Status** — View only failed, retrying, or successful deliveries
- **Event Type** — See all deliveries for a specific event (e.g., all `order.created` deliveries)
- **Endpoint** — View deliveries for a specific endpoint
- **Created At** — Filter by date range

Use the search bar to search by event type or endpoint name, or to find a specific delivery by its ID.

## Reading a delivery detail

Click on any delivery to see its full detail. Delivery records are read-only.

### Summary

- **ID** — The unique identifier for this delivery attempt
- **Endpoint** — Which webhook endpoint this was sent to (links to the endpoint record)
- **Event Type** — The event that triggered this delivery (e.g., `order.paid`)
- **Status** — Current delivery status

### Payload

The **Payload** section shows the exact JSON data that was sent to your endpoint. This includes the event type, a timestamp, and the full event data. Use this to verify that your receiving server is getting the correct data structure.

### Response

The **Response** section shows what your server replied with:

- **Response Status Code** — The HTTP status code returned by your server. Color-coded: green for 2xx (success), yellow for 4xx (client error), red for 5xx (server error).
- **Response Time** — How long your server took to respond in milliseconds. Color-coded: green under 500ms, yellow up to 2 seconds, red above 2 seconds.
- **Response Body** — The body of your server's response (truncated to 1,000 characters). This can help identify why your server rejected the webhook.
- **Response Headers** — The headers returned by your server.

### Error details

If the delivery failed, the **Error Details** section shows the error message — for example, `Connection refused`, `Timeout after 30s`, or the HTTP error from your server.

### Retry information

- **Attempt Count** — How many delivery attempts have been made (including the first attempt)
- **Next Retry At** — When the next retry will be attempted (only shown for deliveries in **Retrying** status)

Retries follow an exponential back-off schedule — the gap between retries increases with each attempt to avoid overwhelming a server that is temporarily unavailable. With a maximum of 5 retries (the default), the retry schedule spans several hours.

## Manually retrying failed deliveries

If you want to immediately retry a delivery without waiting for the automatic schedule:

1. Select the checkboxes next to the deliveries you want to retry
2. From the **Action** dropdown, choose **Retry selected deliveries**
3. Click **Go**

Only deliveries that are not already in **Success** status will be queued for retry. Successful deliveries are skipped.

This is useful when you have fixed a problem with your receiving server and want to reprocess failed events without waiting.

## Diagnosing common failures

### HTTP 4xx response codes

A 4xx response from your server usually means there is a problem with the request — authentication failed, the endpoint URL changed, or your server rejected the payload format. Check:

- Is the endpoint URL correct?
- Is your server verifying the HMAC signature correctly? A mismatch causes many servers to return 401 or 403.
- Has the payload structure changed? Check the payload in the delivery log against what your server expects.

### HTTP 5xx response codes

A 5xx response means your server encountered an internal error while processing the webhook. Check your server's own error logs to diagnose the problem.

### Connection refused / Timeout

These errors mean Spwig could not reach your server at all:

- Is the server running and publicly accessible?
- Is the URL correct (including the correct protocol — http or https)?
- Is a firewall blocking incoming requests?
- Is the server's response time exceeding the configured timeout? If so, increase the **Timeout** setting on the endpoint or optimise your server's webhook handler to respond quickly (ideally within 5 seconds).

### Sandbox Blocked

Deliveries are blocked to localhost URLs or internal network addresses. Webhook endpoints must be publicly reachable. Use a tool like ngrok during development to expose a local server publicly.

## Tips

- Address **Failed** deliveries promptly — the event data is still in the payload, and you can manually retry once the issue is fixed.
- If you see many **Retrying** deliveries for one endpoint, open the endpoint record and check the **Health** section — the endpoint may be about to be auto-disabled.
- Response time matters: configure your webhook handler to respond quickly (within a few seconds) and process the payload asynchronously in the background. A slow handler causes timeout failures even if your logic is correct.
- Use the **Event Type** filter to check delivery history for a specific event type when investigating whether your integration is receiving the right events.
- Delivery logs accumulate over time. Use the date filter to focus on recent deliveries and avoid wading through old history.
