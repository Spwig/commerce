---
slug: email-outbox
title_i18n_key: Email Outbox
category: store-config
component: email_system
keywords:
  - email outbox
  - sent emails
  - email delivery status
  - failed email
  - email history
  - scheduled email
  - held email
  - email log
  - email troubleshooting
  - bounced email
  - email queue
  - release email
  - email delivery
url_patterns:
  - /admin/email_system/emailoutbox/
  - /admin/email_system/scheduledemail/
related:
  - email-templates
  - sms-outbox
published: true
---

The Email Outbox is a complete log of every email your store has sent or attempted to send — order confirmations, shipping updates, admin reports, and all other transactional messages. Use it to confirm deliveries, investigate failures, and manage the email queue.

Navigate to **Email System > Email Outbox** to view the email log.

![Email Outbox list with status badges](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Reading the outbox

The summary bar at the top shows counts for each status category. The list below shows individual emails with:

- **Subject** — the email subject line
- **To** — the recipient's email address
- **From** — the sender address used
- **Status** — the current delivery status
- **Queued At** — when the email entered the queue
- **Sent At** — when the email was dispatched to the provider
- **Retry Count** — how many send attempts have been made

## Email statuses

| Status | Meaning |
|--------|---------|
| Queued | The email is waiting in the queue to be sent |
| Sending | The email is currently being sent to the provider |
| Sent | The provider accepted the email |
| Held | The email is paused and will not send until released |
| Logged | The email was recorded but not sent (test mode or logging-only setup) |
| Failed | The provider rejected or could not deliver the email |
| Bounced | The email was sent but bounced back from the recipient's mail server |
| Skipped | Sending was skipped for a system reason |

## Viewing email details

Click any email in the list to see the full details:

- The complete **HTML Body** and **Text Body** of the email
- **Provider Message ID** — the reference from your email provider (use this when contacting provider support)
- **Error Message** — the exact error for failed or bounced emails
- **Retry Count** and **Max Retries** — how many times sending was attempted
- All timestamps: created, queued, sent, and failed

## Filtering the outbox

Use the filters on the right to narrow your view:

- **Status** — show emails of a specific delivery status
- **Date** — filter by when emails were created or sent
- **Template Type** — show only emails of a specific notification type (e.g., order confirmations only)

The search box at the top searches by subject, recipient address, sender address, or provider message ID.

## Releasing held emails

Emails in **Held** status are paused — they will not be sent until you release them. An email may be held if your store was in maintenance mode when it was generated, or if an admin action placed it on hold.

To release held emails:
1. Select the emails you want to release (check the boxes on the left)
2. Choose **Release held emails for delivery** from the **Actions** dropdown
3. Click **Go**

Released emails move to **Queued** status and are sent on the next queue processing cycle.

## Scheduled emails

Some emails are scheduled to send at a future time — weekly digest reports, for example, are scheduled to go out on a specific day and time. Navigate to **Email System > Scheduled Emails** to view upcoming scheduled sends.

The scheduled emails list shows:

- **Template Type** — the type of email scheduled
- **Recipient Email** — the address it will be sent to
- **Scheduled For** — the date and time it is due to send
- **Status** — Pending (not yet sent), Sent, or Failed

Scheduled emails are processed automatically when their scheduled time arrives — no manual action is needed.

## Troubleshooting failed deliveries

If emails show a **Failed** status, click through to see the error message and follow these steps:

### Common causes and fixes

| Symptom | Likely cause | What to do |
|---------|-------------|------------|
| "Authentication failed" | Email provider credentials are invalid | Update credentials in **Email System > Email Accounts** |
| "Connection refused" / "Timeout" | Your email server is unreachable | Check your email provider's status page; test the connection in **Email Accounts** |
| "Invalid recipient" | The customer's email address is malformed | Review the customer's account and correct their email |
| Bounced emails | Recipient's mail server rejected the email | The address may not exist or their inbox is full; do not retry excessively |
| High failure rate suddenly | Provider issue or credentials expired | Check provider status; re-test the connection in **Email Accounts** |

### Checking your email account connection

If many emails are failing, test your email account:

1. Navigate to **Email System > Email Accounts**
2. Find your active account and check its **Connection** status
3. If the connection shows an error, click on the account and use the **Test Connection** option to diagnose the issue

### Retry behaviour

Spwig automatically retries failed emails up to the **Max Retries** limit. The retry count shown on each email tells you how many attempts have been made. Once the retry limit is reached, the email stays in **Failed** status and no further automatic retries occur.

## Bounced emails

A **Bounced** email was sent but returned by the recipient's mail server. There are two bounce types:

- **Hard bounce** — the email address does not exist or the domain does not accept email. Do not retry hard bounces; the address is invalid
- **Soft bounce** — a temporary issue (inbox full, server temporarily unavailable). May succeed on retry

Repeated bounces to the same address can damage your sender reputation with email providers. If you see repeated bounces to the same customer address, update or remove that address from the customer's account.

## Tips

- Review the outbox after major events like a flash sale or large product launch to confirm all order confirmation emails were sent successfully
- If a customer says they did not receive an email, search the outbox by their email address to see whether it was sent, failed, or skipped
- A sudden increase in failures usually points to a credential or account issue — check **Email Accounts** immediately
- The **Held** status is not a failure — it just means the email is waiting. Release held emails when you are ready to send them
- Use the **Template Type** filter to quickly audit all emails of one type — for example, check that all order confirmations in the last 7 days have a **Sent** status
- The date hierarchy navigation (day / month / year) at the top of the list is useful for reviewing the outbox for a specific period
