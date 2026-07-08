---
slug: managing-subscriptions
title_i18n_key: Managing Customer Subscriptions
category: products
component: subscriptions
keywords:
  - customer subscription
  - subscription status
  - cancel subscription
  - pause subscription
  - billing history
  - billing cycle log
  - subscription management
  - past due
  - subscription renewal
  - subscription trial
  - subscription expired
  - reactivate subscription
  - subscription grace period
url_patterns:
  - /admin/subscriptions/customersubscription/
  - /admin/subscriptions/customersubscription/\d+/change/
  - /admin/subscriptions/billingcyclelog/
related:
  - subscription-plans
  - subscription-discounts
published: true
---

The customer subscriptions section gives you a complete view of all active, paused, and cancelled recurring subscriptions in your store. From here you can monitor billing health, view individual subscription details, and take action when issues arise.

## Viewing customer subscriptions

Navigate to **Subscriptions > Customer Subscriptions** to see the full list of subscriptions across all customers.

![Customer subscriptions list](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

The list shows each subscription's customer, plan name, current status, next billing date, and the number of completed billing cycles.

### Filtering and searching

Use the filter panel on the right to narrow down subscriptions by:

- **Status** — Filter by Active, Trial, Past Due, Paused, Canceled, or Expired
- **Plan** — View subscriptions for a specific plan
- **Provider Mode** — Native (Stripe/PayPal-managed) or Fallback (internal billing)

Use the search bar to find subscriptions by customer email address.

## Subscription statuses

Understanding each status helps you identify subscriptions that need attention:

| Status | What it means |
|--------|---------------|
| **Trial** | Customer is in the free or reduced-price trial period |
| **Active** | Subscription is healthy — billing is current and access is active |
| **Past Due** | A payment attempt failed — the system is retrying. The customer retains access during the grace period |
| **Paused** | Subscription is temporarily suspended — no billing, no access |
| **Canceled** | Cancellation has been requested. Customer may still have access until the period end date |
| **Expired** | Subscription has fully ended — trial expired, maximum billing cycles reached, or cancellation period elapsed |

Subscriptions that are **Past Due** require the most attention — if payment continues to fail and the grace period runs out, the subscription will be suspended.

## Viewing a subscription's details

Click on any subscription to open the detail view. This shows:

### Current billing period

- **Current Period Start / End** — The dates of the active billing window
- **Next Billing Date** — When the next charge will be attempted
- **Last Billing Date** and **Last Billing Status** — Result of the most recent billing attempt
- **Billing Cycle Count** — How many successful billing cycles have completed

### Subscription information

- **Plan** and **Pricing Tier** — Which plan and billing frequency the customer is on
- **Product / Variant** — The catalog product linked to this subscription (if applicable)
- **Quantity** — Number of seats or units (for quantity-based plans)
- **Payment Token** — The stored payment method being used for recurring billing

### Trial details

If the subscription is in trial, the **Trial End Date** shows when the customer's trial expires and full billing begins.

### Cancellation details

For canceled subscriptions, you can see:

- **Cancellation Type** — Whether cancellation was immediate, at period end, or scheduled
- **Canceled At** — When the cancellation was requested
- **Cancellation Reason** — Notes about why the customer cancelled (if recorded)
- **Reactivation Deadline** — The last date the customer can reactivate without re-subscribing from scratch

### Grace period and commitments

- **Grace Period End Date** — If a payment has failed, this shows the deadline before access is suspended
- **Minimum Commitment End Date** — For plans with minimum commitments, the earliest cancellation date

## Pausing a subscription

A paused subscription stops billing temporarily while also suspending access. This is useful for customers who want to take a break without fully cancelling.

To view paused subscriptions, filter by **Status: Paused**. The detail view shows:

- **Paused At** — When the pause began
- **Pause Reason** — Notes on why it was paused
- **Auto Resume Date** — If set, the date the subscription will automatically resume billing and access

Subscriptions resume either on the auto-resume date or when the customer manually reactivates.

## Billing cycle logs

Every billing attempt — successful or failed — is recorded in the billing cycle log. Navigate to **Subscriptions > Billing Cycle Logs** to view this history.

![Billing cycle log list](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Reading a billing cycle log entry

Each log entry records:

- **Subscription** — Which customer subscription this billing attempt belongs to
- **Cycle Number** — Sequential billing cycle (Cycle 1 = first charge after trial)
- **Billing Date** — When the charge was attempted
- **Status** — Pending, Processing, Successful, Failed, or Retrying
- **Amount breakdown**:
  - **Base Amount** — The plan price before any adjustments
  - **Quantity Amount** — Additional charge for the quantity of seats/units
  - **Add-ons Amount** — Total cost of active add-ons
  - **Discount Amount** — Total discounts applied
  - **Total Amount** — The final amount charged (or attempted)
- **Payment Method** — The card or payment method used
- **Provider Transaction ID** — The payment provider's reference number (useful for refund lookups)
- **Failure Reason** — If the billing failed, why it failed (e.g., card declined, insufficient funds)

### Diagnosing payment failures

If a customer contacts you about a billing issue, find their subscription and check the billing cycle logs. The **Failure Reason** field explains what went wrong. Common failure reasons include:

- **Card declined** — The customer's card was rejected by their bank
- **Insufficient funds** — The account balance was too low at billing time
- **Card expired** — The saved payment method has expired
- **Network error** — A temporary connection issue with the payment provider — usually resolves on retry

For persistent failures, direct the customer to update their payment method in their account settings.

## Tips

- Check the **Past Due** filter weekly to catch subscriptions at risk of churning. A quick email to the customer often resolves payment issues before the grace period expires.
- Billing cycle logs are read-only — they are created automatically and cannot be modified. This ensures a reliable audit trail.
- If a customer's subscription shows **Past Due** but they have already updated their payment method, the next automated retry will pick up the new card. Retries follow the grace period schedule configured in the plan.
- **Expired** subscriptions are not deleted — they remain visible for reporting. Use the date filters to focus on currently active subscriptions.
- For subscriptions in **Trial**, check the **Trial End Date** to anticipate upcoming first charges and proactively address any payment method issues.
