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
  - selling-products-as-subscriptions
published: true
---

Subscription plans let you offer recurring billing for your products — ideal for consumables, services, curated boxes, or any product that customers buy repeatedly. This guide explains how to create and configure plans, set up pricing tiers, add trial periods, and attach optional add-ons.

## Getting started

Navigate to **Subscriptions > Subscription Plans** in the admin sidebar. The plan list shows all your plans with their pricing model, active subscriber count, and visibility status.

![Subscription plans list](/static/core/admin/img/help/subscription-plans/plan-list.webp)

To create a new plan, click the **Create with Wizard** button — this opens the plan creation wizard, which walks you through the setup step by step. The **+ Add Plan** button next to it opens a blank form for merchants who prefer to configure everything by hand instead.

A plan on its own isn't purchasable — it's a template. Once you've built it here, attach it to one or more products from the product's **Subscriptions** tab (Simple, Variable, and Digital products only) so customers can actually subscribe. See [Selling Products as Subscriptions](/help/selling-products-as-subscriptions) for that step.

## The plan editor

Opening an existing plan (click its name, or the pencil icon, from the list) takes you to the plan editor. The header shows the plan name, its pricing model, **Active**/**Inactive** and **Public**/**Private** status badges, and the date it was created. The two buttons in the top-right corner of the header save your changes — the check-circle icon saves and returns to the list, the plain check icon saves and keeps you on the page so you can continue editing.

Below the header, a stats strip summarizes the plan at a glance: **Active Subscriptions**, **Pricing Tiers**, **Add-ons**, and **Total Revenue**.

The rest of the form is organized into five tabs:

| Tab | What it contains |
|-----|-------------------|
| **General** | Plan Information (name, slug, description) and Status (active/public) |
| **Pricing** | Pricing Configuration, Trial Period, and Limits & Restrictions |
| **Tiers & Add-ons** | The Pricing Tiers and Add-ons editors |
| **Lifecycle** | Cancellation Policy and Plan Change Behavior |
| **Advanced** | Provider Integration and Statistics |

The sections below walk through each tab's settings. When you create a brand-new plan directly from **+ Add Plan** (rather than the wizard), the same fields appear in a single scrollable form instead of tabs — save the plan once and reopen it to get the full tabbed editor.

## Plan information (General tab)

The **Plan Information** card captures the core identity of your plan.

- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.
- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.
- **Description** — Optional text describing what the plan includes. Supports translations.

The **Status** card on the same tab controls the **Active** and **Public** toggles — see [Visibility and status](#visibility-and-status) below.

![General tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Pricing model (Pricing tab)

The **Pricing Configuration** card controls how pricing is structured for this plan:

| Pricing Model | Best For |
|---------------|----------|
| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |
| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |
| **Flat Rate** | A single fixed price with no variations |

For **Quantity-Based** plans, check **Allow Quantity** and set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Pricing tiers (Tiers & Add-ons tab)

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** card on the **Tiers & Add-ons** tab, alongside the Add-ons editor.

Each tier has these fields:

- **Tier Name** — The label shown to customers (e.g., `Monthly`, `Annual — Save 20%`). Supports translations.
- **Billing Cycle** — How often the customer is charged: Daily, Weekly, Monthly, Quarterly, Semi-Annual, or Annual.
- **Billing Interval** — The multiplier for the billing cycle. Set to `2` with Monthly to bill every 2 months.
- **Discount Percentage** — The discount applied to the product price for this tier. Set to `0` for full price, or `20` to give 20% off. This discount stacks on top of any sale pricing on the product itself.
- **Default Tier** — Mark one tier as the default to pre-select it for customers when they view the subscription options.

The discount applies starting from the customer's very first billing cycle, not just on renewals — a tier with a 20% discount charges 20% off from day one (or from the first charge after a trial, if the plan has one).

### Example: tiered plan with three options

For a "Coffee Club" subscription plan:

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Plan add-ons (Tiers & Add-ons tab)

Add-ons are optional extras that subscribers can attach to their plan. Add them in the **Add-ons** card, directly below Pricing Tiers on the same tab:

- **Add-on Name** — The name shown to customers. Supports translations.
- **Description** — What the add-on provides.
- **Price** — Cost of the add-on.
- **Billing Frequency** — Whether the add-on is charged **Per Billing Cycle** (recurring) or **One-Time** at subscription start.
- **Allow Quantity** — Enable to let customers purchase multiple units of the add-on.
- **Required** — Check this to automatically include the add-on on all new subscriptions. Required add-ons cannot be removed by the customer.

![Tiers & Add-ons tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Trial period (Pricing tab)

A trial period lets customers try your subscription before their first full charge. Configure this in the **Trial Period** card, below Pricing Configuration:

- **Trial Period (Days)** — Number of free trial days. Set to `0` to disable trials. Maximum is 365 days.
- **Trial Price** — Optional reduced price during the trial (e.g., $1 for the first month). Leave empty for a completely free trial.

## Limits and restrictions (Pricing tab)

The **Limits & Restrictions** card, also on the Pricing tab, holds:

- **Maximum Billing Cycles** — The total number of billing cycles before the subscription automatically ends. Leave empty for unlimited recurring billing. Useful for installment plans or time-limited subscriptions.

**Setup Fee** and **Sort Order** are not part of this card — they're set once, when you first create the plan through the **Create with Wizard** flow, and can't be changed from the edit screen afterward. If you need to adjust either value, deactivate the plan and recreate it with the wizard rather than editing the existing one. Note that setup fees are not yet charged automatically at checkout in this release — treat the field as reserved for a future update rather than a working charge.

## Cancellation policy (Lifecycle tab)

Control how customers can cancel their subscription in the **Cancellation Policy** card:

| Policy | Description |
|--------|-------------|
| **Cancel Anytime** | Customers can cancel immediately at any time |
| **Cancel at Period End** | Cancellation takes effect at the end of the paid period — customers keep access until expiry |
| **Minimum Commitment Required** | Customers must complete a minimum number of billing cycles before cancelling |

Additional settings:

- **Minimum Commitment (Cycles)** — When using the commitment policy, set the required number of billing cycles (e.g., `3` for a 3-month minimum).
- **Grace Period (Days)** — Days of continued access after a payment failure before the subscription is suspended. Set to `0` for immediate suspension.
- **Reactivation Period (Days)** — Days after cancellation during which a customer can reactivate their subscription without re-subscribing from scratch.

## Plan change behavior (Lifecycle tab)

The **Plan Change Behavior** card, below Cancellation Policy, controls what happens when customers upgrade or downgrade between plans:

- **Upgrade Behavior** — Set to **Immediate** (charge prorated amount now) or **At Renewal** (switch at the next billing date).
- **Downgrade Behavior** — Set to **Immediate** (apply credit to the next bill) or **At Renewal** (switch at the next billing date).

![Lifecycle tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Advanced tab

The **Advanced** tab holds settings you'll rarely need day to day:

- **Provider Integration** — Map this plan to plan/price IDs from your payment providers (e.g., `{"stripe": "price_xxx", "paypal": "P-xxx"}`), for stores that manage subscriptions natively through the provider rather than Spwig's own billing engine.
- **Statistics** — Read-only figures: **Active Subscriptions**, **Total Revenue**, and the plan's **Created At** / **Updated At** timestamps. These mirror the stats strip at the top of the page.

![Advanced tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Visibility and status (General tab)

- **Active** — Uncheck to deactivate a plan so no new subscriptions can be created. Existing subscriptions are not affected.
- **Public** — Uncheck to hide the plan from customer-facing pages (useful for internal or legacy plans that existing subscribers remain on).

## Tips

- Use a **trial period** to reduce hesitation — even a short 7-day free trial can significantly improve conversion rates on subscription products.
- Set up **three pricing tiers** (monthly, quarterly, annual) with increasing discounts to encourage annual commitments and improve your cash flow.
- For service-based subscriptions, set **Cancellation Policy** to **Cancel at Period End** so customers keep access through their paid period — this feels fair and reduces chargebacks.
- Keep the **Grace Period** at 3–7 days for payment failures. This gives customers time to update their payment method before losing access.
- Use the **Required** flag on add-ons sparingly — only use it for things that are genuinely mandatory (e.g., a service agreement), not as a way to inflate pricing.
- Deactivate plans with no subscribers rather than deleting them — this preserves historical data for any customers who previously subscribed.
