---
slug: subscription-plans
title_i18n_key: Subscription Plans
category: products
component: subscriptions
keywords:
  - subscription plan
  - recurring billing
  - subscription pricing
  - billing interval
  - monthly subscription
  - annual subscription
  - trial period
  - plan add-on
  - per seat pricing
  - subscription tier
  - setup fee
  - cancellation policy
  - plan wizard
url_patterns:
  - /admin/subscriptions/subscriptionplan/
  - /admin/subscriptions/subscriptionplan/add/
  - /admin/subscriptions/subscriptionplan/\d+/change/
related:
  - managing-subscriptions
  - subscription-discounts
published: true
---

Subscription plans let you offer recurring billing for your products — ideal for consumables, services, curated boxes, or any product that customers buy repeatedly. This guide explains how to create and configure plans, set up pricing tiers, add trial periods, and attach optional add-ons.

## Getting started

Navigate to **Subscriptions > Subscription Plans** in the admin sidebar. The plan list shows all your plans with their pricing model, active subscriber count, and visibility status.

To create a new plan, click the **+ Add Subscription Plan** button — this opens the plan creation wizard, which walks you through the setup step by step.

![Subscription plans list](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Plan information

The first section captures the core identity of your plan.

- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.
- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.
- **Description** — Optional text describing what the plan includes. Supports translations.

## Pricing model

Choose how pricing is structured for this plan:

| Pricing Model | Best For |
|---------------|----------|
| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |
| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |
| **Flat Rate** | A single fixed price with no variations |

For **Quantity-Based** plans, set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

## Pricing tiers

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** section below the main form.

Each tier has these fields:

- **Tier Name** — The label shown to customers (e.g., `Monthly`, `Annual — Save 20%`). Supports translations.
- **Billing Cycle** — How often the customer is charged: Daily, Weekly, Monthly, Quarterly, Semi-Annual, or Annual.
- **Billing Interval** — The multiplier for the billing cycle. Set to `2` with Monthly to bill every 2 months.
- **Discount Percentage** — The discount applied to the product price for this tier. Set to `0` for full price, or `20` to give 20% off. This discount stacks on top of any sale pricing on the product itself.
- **Default Tier** — Mark one tier as the default to pre-select it for customers when they view the subscription options.

### Example: tiered plan with three options

For a "Coffee Club" subscription plan:

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Trial period

A trial period lets customers try your subscription before their first full charge. Configure this in the **Trial Period** section:

- **Trial Period (Days)** — Number of free trial days. Set to `0` to disable trials. Maximum is 365 days.
- **Trial Price** — Optional reduced price during the trial (e.g., $1 for the first month). Leave empty for a completely free trial.

## Cancellation policy

Control how customers can cancel their subscription in the **Cancellation Policy** section:

| Policy | Description |
|--------|-------------|
| **Cancel Anytime** | Customers can cancel immediately at any time |
| **Cancel at Period End** | Cancellation takes effect at the end of the paid period — customers keep access until expiry |
| **Minimum Commitment Required** | Customers must complete a minimum number of billing cycles before cancelling |

Additional settings:

- **Minimum Commitment (Cycles)** — When using the commitment policy, set the required number of billing cycles (e.g., `3` for a 3-month minimum).
- **Grace Period (Days)** — Days of continued access after a payment failure before the subscription is suspended. Set to `0` for immediate suspension.
- **Reactivation Period (Days)** — Days after cancellation during which a customer can reactivate their subscription without re-subscribing from scratch.

## Plan change behavior

When customers upgrade or downgrade between plans, you can control when the change takes effect:

- **Upgrade Behavior** — Set to **Immediate** (charge prorated amount now) or **At Renewal** (switch at the next billing date).
- **Downgrade Behavior** — Set to **Immediate** (apply credit to the next bill) or **At Renewal** (switch at the next billing date).

## Limits and restrictions

- **Maximum Billing Cycles** — The total number of billing cycles before the subscription automatically ends. Leave empty for unlimited recurring billing. Useful for installment plans or time-limited subscriptions.
- **Setup Fee** — A one-time charge collected when the subscription is first created (e.g., onboarding or activation fee). Set to `0.00` for no setup fee.

## Plan add-ons

Add-ons are optional extras that subscribers can attach to their plan. Add them in the **Plan Add-ons** section:

- **Add-on Name** — The name shown to customers. Supports translations.
- **Description** — What the add-on provides.
- **Price** — Cost of the add-on.
- **Billing Frequency** — Whether the add-on is charged **Per Billing Cycle** (recurring) or **One-Time** at subscription start.
- **Allow Quantity** — Enable to let customers purchase multiple units of the add-on.
- **Required** — Check this to automatically include the add-on on all new subscriptions. Required add-ons cannot be removed by the customer.

## Visibility and status

- **Active** — Uncheck to deactivate a plan so no new subscriptions can be created. Existing subscriptions are not affected.
- **Public** — Uncheck to hide the plan from customer-facing pages (useful for internal or legacy plans that existing subscribers remain on).
- **Sort Order** — Controls the display order on subscription selection pages. Lower numbers appear first.

## Tips

- Use a **trial period** to reduce hesitation — even a short 7-day free trial can significantly improve conversion rates on subscription products.
- Set up **three pricing tiers** (monthly, quarterly, annual) with increasing discounts to encourage annual commitments and improve your cash flow.
- For service-based subscriptions, set **Cancellation Policy** to **Cancel at Period End** so customers keep access through their paid period — this feels fair and reduces chargebacks.
- Keep the **Grace Period** at 3–7 days for payment failures. This gives customers time to update their payment method before losing access.
- Use the **Required** flag on add-ons sparingly — only use it for things that are genuinely mandatory (e.g., a service agreement), not as a way to inflate pricing.
- Deactivate plans with no subscribers rather than deleting them — this preserves historical data for any customers who previously subscribed.
