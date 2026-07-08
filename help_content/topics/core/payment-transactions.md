---
slug: payment-transactions
title_i18n_key: Payment Transactions
category: payments
component: payment_providers
keywords:
  - payment transaction
  - payment status
  - transaction history
  - payment webhook
  - payment intent
  - charge
  - refund
  - authorisation
  - capture
  - void
  - payment failed
  - payment log
  - webhook log
  - payment provider
  - checkout payment
url_patterns:
  - /admin/payment_providers/paymenttransaction/
  - /admin/payment_providers/paymentwebhook/
  - /admin/payment_providers/paymentintent/
related:
  - payment-setup
published: true
---

Payment transactions is the complete record of every payment event processed through your store — charges, refunds, authorisations, and more. This section also includes webhook logs from your payment providers and payment intents created during checkout.

## Payment transactions

Navigate to **Payments > Payment Transactions** to see every transaction your store has processed.

### Transaction types

| Type | What it means |
|------|--------------|
| **Charge** | An immediate payment — funds are collected at the time of the transaction |
| **Authorize** | Funds are held on the customer's card but not yet collected |
| **Capture** | Collects the funds from a previous authorisation |
| **Void** | Cancels an authorisation before it is captured |
| **Refund** | Returns payment to the customer |

### Transaction statuses

| Status | What it means |
|--------|--------------|
| **Pending** | Transaction has been initiated but not yet processed |
| **Processing** | Being processed by the payment provider |
| **Authorized** | Funds are held — awaiting capture |
| **Completed** | Payment was successful |
| **Failed** | Payment was declined or an error occurred |
| **Voided** | The authorisation was cancelled before capture |
| **Refunded** | A full refund has been issued |
| **Partially Refunded** | Part of the payment has been returned |

### What you can see on a transaction record

Each transaction shows:
- **Transaction ID** — Spwig's internal reference
- **Provider Transaction ID** — The reference from your payment provider (e.g., Stripe charge ID)
- **Amount** — The transaction amount and currency
- **Status** and **Type**
- **Customer Email** and **Customer Name**
- **Payment Method** — Type (credit card, bank transfer, etc.) and last 4 digits
- **Order** — The order this transaction belongs to
- **Provider Account** — Which payment provider processed it
- **Provider Response** — The raw technical response from the payment provider
- **Error Message** — If the transaction failed, the reason given by the provider
- Timestamps for creation, last update, and completion

### Filtering transactions

Use the admin filters to narrow down transactions by:
- Status (e.g., show only failed transactions)
- Type (e.g., show only refunds)
- Provider account
- Date range

This is useful for end-of-day reconciliation or investigating a specific customer's payment history.

### When can a transaction be refunded?

A transaction can be refunded when:
- Its status is **Completed**
- Its type is **Charge** or **Capture**

To issue a refund, use the **Refund** action from the order detail page. Refunds processed through the order create a new transaction record of type **Refund**.

### Authorise and capture flow

Some payment methods (and some payment providers) support separate authorise and capture. This is useful if you want to verify payment before shipping:

1. **Authorise** — Funds are held on the customer's card (status: `Authorized`)
2. **Capture** — Triggered when the order ships or is fulfilled
3. If not captured within the authorisation window, the hold **expires** automatically

The **Expires At** field on the transaction shows when an authorisation will lapse.

## Payment webhooks

Payment providers send webhook events to notify your store of payment status changes — for example, when a payment succeeds, fails, or a dispute is raised. Spwig logs all incoming webhooks.

Navigate to **Payments > Payment Webhooks** to view the log.

### What webhook records show

| Field | Description |
|-------|-------------|
| **Provider** | Which payment provider sent the webhook |
| **Event ID** | The provider's unique event identifier |
| **Event Type** | The type of event (e.g., `payment_intent.succeeded`, `charge.refunded`) |
| **Processed** | Whether Spwig has acted on this webhook |
| **Signature Verified** | Whether the webhook's security signature was valid |
| **Payload** | The full data sent by the provider |
| **Processing Result** | What Spwig did in response |
| **Processing Error** | Any error that occurred during processing |
| **Received At** | When the webhook arrived |

### Using webhook logs for troubleshooting

If a payment appears stuck or an order status did not update after payment:

1. Navigate to **Payments > Payment Webhooks**
2. Filter by the provider and look for recent events
3. Check the **Processed** column — an unprocessed webhook may indicate a delivery issue
4. Check **Signature Verified** — a failed signature may mean your webhook secret is misconfigured
5. Review **Processing Error** for any error messages

Duplicate events are handled automatically — the `Event ID` and provider combination is unique, so the same webhook cannot be processed twice.

## Payment intents

A payment intent tracks the lifecycle of a checkout payment from the moment a customer begins the payment process to the final outcome. Payment intents are created automatically when a customer reaches the payment step at checkout.

Navigate to **Payments > Payment Intents** to view the list.

### Payment intent statuses

| Status | Meaning |
|--------|---------|
| **Created** | Intent has been created, awaiting payment method |
| **Requires Payment Method** | Waiting for the customer to enter their card details |
| **Requires Confirmation** | Payment details entered, awaiting confirmation |
| **Requires Action** | Customer needs to complete an action (e.g., 3D Secure authentication) |
| **Processing** | Payment is being processed |
| **Succeeded** | Payment completed successfully |
| **Canceled** | The payment was abandoned or cancelled |
| **Failed** | Payment attempt failed |

### Payment intent to order flow

1. Customer reaches checkout payment step → Spwig creates a **Payment Intent** and a draft **Order** (unpaid)
2. Customer enters payment details and confirms
3. Payment provider processes the payment
4. On success, the Order is updated to **Paid** and the Payment Intent moves to **Succeeded**
5. A **Payment Transaction** record is created with the final charge details

The payment intent links together the checkout session, the provider account, and the order — giving you a complete picture of a customer's checkout journey.

### Using payment intents for support

If a customer reports that they paid but their order shows as unpaid:

1. Find the customer's order in **Orders**
2. Navigate to **Payments > Payment Intents** and search for intents linked to that order
3. Check the intent status — if it is **Succeeded**, check the linked transaction
4. If the intent is **Requires Action**, the customer may not have completed 3D Secure authentication
5. If the intent is **Failed**, the error details explain why the payment was declined

## Tips

- Review failed transactions daily — patterns of failures (e.g., a specific payment method or country) may indicate a configuration issue or fraud attempt.
- Webhook logs are invaluable when investigating payment discrepancies. If an order was paid but not confirmed, the webhook log will usually tell you what went wrong.
- Authorisation holds expire automatically — if you use authorise-then-capture, ensure your fulfilment process captures funds before the expiry window closes (typically 7 days for most providers).
- The **Provider Response** field on transactions contains the raw data from the payment provider. Share this with your provider's support team if you need help resolving a specific transaction issue.
- Signature verification failures on webhooks should be investigated immediately — they may indicate a misconfigured webhook secret or an attempt to send fraudulent webhook events to your store.
