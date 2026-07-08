---
slug: subscription-discounts
title_i18n_key: Subscription Discounts
category: products
component: subscriptions
keywords:
  - subscription discount
  - coupon code
  - recurring discount
  - subscription promotion
  - percentage off subscription
  - fixed amount discount
  - price override
  - discount duration
  - subscription offer
  - subscriber coupon
url_patterns:
  - /admin/subscriptions/subscriptiondiscount/
related:
  - subscription-plans
  - managing-subscriptions
published: true
---

Subscription discounts let you apply price reductions to individual customer subscriptions — for example, rewarding loyal subscribers, honouring a promotional coupon, or resolving a billing dispute with a goodwill credit. Unlike plan-level pricing tiers, these discounts are applied directly to a specific subscription.

## Viewing subscription discounts

Navigate to **Subscriptions > Subscription Discounts** to see all discounts currently applied across your subscriptions.

Each entry shows the subscription it belongs to, the discount type and value, how long the discount lasts, and whether it is still active.

You can also find discounts attached to a specific subscription by opening **Subscriptions > Customer Subscriptions**, clicking on a subscription, and scrolling to the **Discounts** section at the bottom of the detail page.

## Adding a discount to a subscription

To add a new discount:

1. Navigate to **Subscriptions > Subscription Discounts**
2. Click **+ Add Subscription Discount**
3. Select the **Subscription** you want to apply the discount to
4. Configure the discount settings (described below)
5. Click **Save**

The discount takes effect at the next billing cycle.

## Discount types

Choose how the discount is calculated:

| Discount Type | How it works | Example |
|---------------|--------------|---------|
| **Percentage Off** | Reduces the bill by a percentage | `20` reduces a $50 bill to $40 |
| **Fixed Amount Off** | Subtracts a fixed amount from the bill | `10` reduces a $50 bill to $40 |
| **Fixed Price Override** | Sets the subscription to a specific price, regardless of the normal plan price | `29` sets the bill to $29/cycle |

Set the **Discount Value** field to the number corresponding to your chosen type (percentage, dollar amount, or fixed price).

### Example: retention offer

A customer contacts you wanting to cancel. You offer them 3 months at 25% off to stay:

| Field | Value |
|-------|-------|
| Discount Type | Percentage Off |
| Discount Value | `25` |
| Duration Type | Repeating |
| Duration (Months) | `3` |

## Discount duration

Control how long the discount applies to future billing cycles:

| Duration Type | When it applies |
|---------------|-----------------|
| **Apply Once** | Reduces only the next billing cycle's charge, then expires automatically |
| **Forever** | Applies to every future billing cycle until manually deactivated |
| **Repeating** | Applies for a set number of months, then expires |

For **Repeating** discounts, set the **Duration (Months)** field to the number of months the discount should last. The **Remaining Cycles** field tracks how many cycles are left — it counts down with each billing cycle.

## Coupon codes

If the discount was triggered by a promotional coupon code, enter it in the **Coupon Code** field. This is informational — it records which promotion the discount originated from for your own tracking purposes.

## Deactivating a discount

To stop a discount before it expires naturally, open the discount record and uncheck the **Active** checkbox, then save. The discount will no longer apply to future billing cycles. The subscription will return to its normal plan price at the next billing.

You can also set an **Expires At** date when creating the discount — the system will automatically deactivate it after that date.

## Tips

- Use **Apply Once** discounts for one-off goodwill gestures (e.g., compensating a subscriber for a service outage). They are clean and self-expiring.
- **Percentage Off** discounts are safer than **Fixed Amount Off** for variable-price subscriptions, since the discount scales with the actual bill amount.
- When offering a retention deal, use **Repeating** with a 3-month duration — it gives customers a reason to stay without permanently reducing your revenue.
- Keep the **Coupon Code** field consistent with whatever code customers used. This makes it easy to audit which promotions drove which discounts when reviewing your subscription revenue.
- Discounts are applied to individual subscriptions, not to plans. If you want to lower the price of a plan for all new subscribers, update the plan's pricing tiers instead.
