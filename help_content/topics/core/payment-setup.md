---
slug: payment-setup
title_i18n_key: Payment Setup
category: store-config
component: payment_providers
keywords:
  - payment
  - payment provider
  - stripe
  - paypal
  - checkout
  - payment dashboard
  - webhook
  - transaction
  - credit card
  - payment method
url_patterns:
  - /admin/payment-providers/dashboard/
  - /admin/payment_providers/paymentprovideraccount/
related:
  - store-settings
published: true
---

Payment providers connect your store to payment gateways so you can accept credit cards, digital wallets, and other payment methods at checkout. Spwig supports multiple providers simultaneously, giving your customers flexible payment options.

![Payment providers](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Available Providers

| Provider | Description |
|----------|-------------|
| **Stripe** | Credit cards, Apple Pay, Google Pay, and 135+ currencies |
| **PayPal** | PayPal balance, credit/debit cards, and Pay Later options |
| **Airwallex** | Multi-currency payments optimized for cross-border commerce |
| **Adyen** | Enterprise-grade payments with 250+ payment methods worldwide |
| **Square** | In-person and online payments with integrated POS support |
| **Revolut** | Fast European payments with competitive FX rates |

## Connecting a Provider

Navigate to **Settings > Payment Providers** and click **Connect Provider** to launch the setup wizard.

### Step 1: Select Provider

Choose from the available payment providers. Each card shows the provider's supported features and regions.

### Step 2: Setup Instructions

Review the provider-specific setup guide. This includes:
- How to create an account with the provider (if you don't have one)
- Where to find your API credentials in the provider's dashboard
- Any prerequisites (e.g., business verification)

### Step 3: Enter Credentials

Enter your API credentials:
- **API Key / Secret Key** — Your authentication credentials from the provider's dashboard
- **Checkout Mode** — Choose how customers interact with the payment form:

| Mode | Description |
|------|-------------|
| **Hosted** | Customers are redirected to the provider's payment page (e.g., Stripe Checkout). Simplest setup, PCI compliance handled by the provider. |
| **Integrated** | The payment form is embedded directly in your checkout page. Seamless experience, but requires the provider's JavaScript SDK. |

- **Sandbox / Live Mode** — Start in sandbox mode for testing, then switch to live when ready

### Step 4: Test Connection

Click **Test Connection** to verify your credentials are valid. The wizard checks:
- API key authentication
- Account permissions
- Webhook endpoint accessibility

### Step 5: Configure and Save

Finalize the provider settings:
- **Active** — Enable or disable the provider
- **Default Provider** — Set as the primary payment method at checkout
- **Display Name** — The name shown to customers during checkout
- **Sort Order** — Controls the order providers appear at checkout (lower numbers appear first)

## Payment Dashboard

Navigate to **Settings > Payment Dashboard** for an overview of your payment activity:

### Actions Required

Alert cards at the top highlight issues needing attention:
- **Failed Transactions** — Payments that couldn't be processed
- **Pending Captures** — Authorized payments awaiting capture
- **Connection Errors** — Providers with connectivity issues

### Revenue Analytics

- **Revenue Chart** — Visual breakdown of payment volume over time, grouped by day, week, or month
- **Performance Metrics** — Total revenue, success rate, average transaction value, and refund rate
- **Provider Comparison** — Side-by-side performance cards for each connected provider

### Transaction Breakdown

- **Status Distribution** — Completed, pending, failed, and refunded transaction counts
- **Payment Method Mix** — Which payment methods customers use most (credit card, PayPal, digital wallets)

## Managing Payment Methods

Each provider supports different payment methods. You can enable or disable specific methods per country:

1. Navigate to a provider's configuration page
2. Scroll to the **Payment Methods** section
3. Toggle individual methods on or off
4. Use country-level controls to restrict methods to specific markets

This is useful when a payment method is popular in one region but not another (e.g., iDEAL in the Netherlands, Bancontact in Belgium).

## Webhooks

Webhooks keep your store synchronized with the payment provider in real time. They handle events like:
- Payment completed or failed
- Refunds processed
- Disputes and chargebacks opened
- Subscription renewals

### Automatic Setup

When you connect a provider, Spwig automatically registers a webhook endpoint with the provider. The webhook URL is displayed on the provider's configuration page for reference.

### Webhook Monitoring

Each incoming webhook is logged with:
- **Event type** (e.g., payment_intent.succeeded)
- **Timestamp** and processing status
- **Payload** for debugging

If a webhook fails to process, it's logged as an error so you can investigate.

## Using Multiple Providers

You can connect multiple payment providers simultaneously:

- **Default Provider** — The provider selected by default at checkout. Mark one provider as default in its configuration.
- **Sort Order** — Controls the display order at checkout. Customers see all active providers and can choose their preferred one.
- **Failover** — If a provider experiences downtime, customers can still pay using an alternative provider.

## Tips

- Start with **Stripe** or **PayPal** — they cover the widest range of payment methods and regions.
- Use **sandbox/test mode** to process test transactions before going live. Each provider has test card numbers in their documentation.
- Enable **multiple providers** so customers have a backup payment option if one provider has issues.
- Set a **low sort order** for your preferred provider so it appears first at checkout.
- Monitor the Payment Dashboard weekly to catch failed transactions and connection issues early.
- Keep your API credentials secure — they are stored encrypted in the database but should never be shared.
