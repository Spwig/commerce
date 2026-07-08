---
slug: sms-outbox
title_i18n_key: SMS Outbox
category: store-config
component: sms_system
keywords:
  - SMS outbox
  - sent SMS
  - SMS delivery status
  - failed SMS
  - SMS history
  - message log
  - delivery tracking
  - SMS troubleshooting
  - SMS failed
  - message status
  - retry SMS
  - SMS skipped
url_patterns:
  - /admin/sms_system/smsoutbox/
related:
  - sms-setup
  - sms-templates
published: true
---

The SMS Outbox is a complete record of every text message your store has attempted to send. Use it to confirm that notifications reached customers, investigate delivery failures, and understand your overall messaging activity.

Navigate to **SMS System > SMS Outbox** to view the message log.

![SMS Outbox list with status badges](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Reading the outbox

Each row in the outbox represents one message attempt and shows:

- **Phone** — the recipient's phone number
- **Message Type** — SMS or WhatsApp
- **Status** — the current delivery status (see below)
- **Created** — when the message was created
- **Sent At** — when the message was dispatched to the provider

The summary bar at the top shows aggregate counts for the most important statuses at a glance.

## Message statuses

| Status | Meaning |
|--------|---------|
| Pending | Message is waiting to be picked up by the sending queue |
| Queued | Message has been queued and will be sent shortly |
| Sent | The provider accepted the message for delivery |
| Delivered | The provider confirmed the message reached the recipient's device |
| Failed | The provider rejected or could not deliver the message |
| Skipped | Sending was skipped intentionally (see skip reasons below) |
| Sandbox Logged | Message was logged only (store is in test/sandbox mode) |

> **Sent vs Delivered:** A **Sent** status means the message left your store and was accepted by the provider. A **Delivered** status means the provider received a delivery receipt from the carrier. Not all providers support delivery receipts — if your provider does not, messages may show **Sent** but never progress to **Delivered**, which is normal.

## Viewing message details

Click any row in the outbox to see the full details of that message:

- The complete **Message** text that was sent
- The **Provider Message ID** — the reference number from the SMS provider (useful when contacting provider support)
- The **Error Message** (for failed messages) — the exact error returned by the provider
- The **Retry Count** — how many times Spwig has attempted to send the message
- All timestamps (created, queued, sent, delivered)

## Filtering the outbox

Use the filters on the right-hand side to narrow the list:

- **Status** — show only messages with a particular status
- **Message Type** — show only SMS or only WhatsApp messages
- **Date** — filter by the day a message was created

The search box at the top lets you search by phone number, message content, or provider message ID.

## Understanding skip reasons

Skipped messages were not sent because Spwig determined sending was inappropriate or unnecessary. Common skip reasons:

| Skip Reason | What it means |
|-------------|---------------|
| `user_preference_disabled` | The customer turned off SMS notifications in their account settings |
| `unsubscribed` | The customer has unsubscribed from SMS messages |
| `no_provider` | No active default SMS provider account is configured |
| `template_inactive` | The template for this notification type is inactive |

A skipped message is not a failure — it means the system worked as intended. However, a high count of `no_provider` skips indicates you need to configure and activate an SMS provider account.

## Troubleshooting failed deliveries

If messages show a **Failed** status, follow these steps:

1. Click the failed message to view its **Error Message**
2. Common error causes:

   | Error | Likely cause |
   |-------|-------------|
   | Invalid phone number | The customer's phone number is missing or not in E.164 format |
   | Authentication failed | Your provider credentials are invalid or expired — update them in **SMS Provider Accounts** |
   | Account suspended | Your provider account has been suspended — log in to the provider's dashboard |
   | Insufficient funds | Your provider account balance is too low — top it up |
   | Carrier rejection | The destination carrier blocked the message (often due to content filtering) |

3. After fixing the underlying issue, future messages will send normally — the outbox is a read-only log and individual messages cannot be manually resent

## Outbox is read-only

The SMS Outbox is a record only. You cannot add messages to the outbox manually, and you cannot resend individual messages from here. Messages are sent automatically by Spwig when the relevant events occur (e.g., an order is placed).

## Tips

- Review the outbox after a busy period to confirm all order confirmation messages were delivered successfully
- If a customer says they did not receive an SMS, search the outbox by their phone number to see whether the message was sent, failed, or skipped
- A sudden spike in **Failed** messages usually indicates an issue with your provider credentials or account balance — check these immediately
- If you see many **Skipped** messages with reason `no_provider`, navigate to **SMS System > SMS Provider Accounts** and ensure an active default account is configured
- The date hierarchy at the top of the list lets you quickly navigate by day, month, or year to review historical messages
