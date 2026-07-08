---
slug: voucher-examples
title_i18n_key: Voucher Examples
category: promotions
component: vouchers
keywords:
  - voucher example
  - discount code setup
  - percentage voucher
  - fixed amount voucher
  - free shipping voucher
  - first-time customer code
  - product voucher
  - category voucher
url_patterns:
  - /admin/vouchers/vouchercode/
related:
  - voucher-codes
  - voucher-campaign-ideas
  - combining-discounts
published: true
---

This guide provides concrete, field-by-field examples for the most common voucher types. Each example shows exactly what to enter when creating a voucher at **Marketing > Vouchers** → **+ Add Voucher**.

![Voucher Card](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Example 1: Percentage Off with Discount Cap

**Scenario:** Offer 20% off the entire cart, but cap the discount at $50 so high-value orders stay profitable. No expiry date.

| Field | Value |
|-------|-------|
| Code | `SAVE20` |
| Name | 20% Off — Max $50 |
| Discount Type | Percentage |
| Discount Value | 20 |
| Max Discount Amount | 50 |
| Application Scope | Entire Cart |
| Max Uses Total | *(empty — unlimited)* |
| Max Uses Per Customer | 1 |
| Min Order Value | *(empty — no minimum)* |

**How the cap works:** On a $200 order the discount is $40. On a $300 order it would be $60, but the cap limits it to $50. On a $500 order the discount is still $50. This lets you run a generous-sounding promotion while keeping the actual discount predictable.

## Example 2: Fixed Amount Off with Minimum

**Scenario:** Give customers $10 off any order over $75 to encourage larger carts.

| Field | Value |
|-------|-------|
| Code | `TAKE10` |
| Name | $10 Off Orders Over $75 |
| Discount Type | Fixed Amount |
| Discount Value | 10 |
| Application Scope | Entire Cart |
| Min Order Value | 75 |
| Max Uses Per Customer | 0 *(unlimited)* |
| End Date | *(empty — no expiry)* |

> **Note:** Setting a minimum order value protects your margins. Without it, a customer could use this code on a $12 order and wipe out your profit. Always pair fixed-amount vouchers with a sensible minimum.

## Example 3: Free Shipping

**Scenario:** Offer free shipping on any order with no minimum spend.

| Field | Value |
|-------|-------|
| Code | `FREESHIP` |
| Name | Free Shipping |
| Discount Type | Free Shipping |
| Application Scope | Entire Cart |
| Max Uses Total | *(empty — unlimited)* |
| Max Uses Per Customer | 1 |
| Min Order Value | *(empty — no minimum)* |

> **Note:** Select the **Free Shipping** discount type, which removes shipping charges from the order automatically. This is the cleanest approach and works regardless of which shipping method the customer selects.

## Example 4: First-Time Customer Welcome Code

**Scenario:** Give new customers 15% off their first order to encourage conversion.

| Field | Value |
|-------|-------|
| Code | `WELCOME15` |
| Name | Welcome — 15% Off First Order |
| Discount Type | Percentage |
| Discount Value | 15 |
| Application Scope | Entire Cart |
| Max Uses Per Customer | 1 |
| First Time Customers Only | Checked |

The system validates first-time status by checking whether the customer has any previous completed orders. If a customer with order history tries to apply this code, they see a clear error message at checkout.

## Example 5: Product-Specific Voucher

**Scenario:** Offer $5 off selected products — for example, to move slow-selling inventory.

| Field | Value |
|-------|-------|
| Code | `PICK5` |
| Name | $5 Off Selected Items |
| Discount Type | Fixed Amount |
| Discount Value | 5 |
| Application Scope | Specific Products |
| Eligible Products | *(select the target products)* |
| Max Uses Per Customer | 1 |

> **Note:** Use product scope when you want to discount individual SKUs. Use category scope (next example) when you want to discount everything in a department. Product scope gives you precise control; category scope is easier to maintain when your catalog changes frequently.

## Example 6: Category Voucher

**Scenario:** Run a 25% off promotion on all items in the Electronics category.

| Field | Value |
|-------|-------|
| Code | `ELEC25` |
| Name | 25% Off Electronics |
| Discount Type | Percentage |
| Discount Value | 25 |
| Application Scope | Specific Categories |
| Eligible Categories | Electronics |
| Max Uses Total | *(empty — unlimited)* |
| Max Uses Per Customer | 1 |

When scoped to a category, the discount applies only to qualifying items in the cart. Non-Electronics items are charged at full price.

## Discount Type Comparison

| Type | How It Works | Best For | Example |
|------|-------------|----------|---------|
| **Percentage** | Deducts a percentage of the qualifying total | Scaling discounts that grow with order size | 20% off entire cart |
| **Fixed Amount** | Deducts a flat dollar amount | Simple, predictable promotions | $10 off orders over $75 |
| **Free Shipping** | Removes shipping charges from the order | Reducing cart abandonment at checkout | Free shipping, no minimum |

## Scope Comparison

| Scope | How It Works | Best For |
|-------|-------------|----------|
| **Entire Cart** | Discount applies to the full order total | Store-wide promotions and welcome codes |
| **Specific Products** | Discount applies only to selected products in the cart | Clearing specific inventory or spotlight deals |
| **Specific Categories** | Discount applies only to items in selected categories | Department-wide sales and seasonal promotions |

## Tips

- **Use memorable codes** — `SUMMER20` converts better than `COUPONX1600406498`. Save auto-generated codes for bulk campaigns.
- **Test before distributing** — Place a test order with the voucher code to verify it applies correctly and respects all limits.
- **Monitor usage** — Check the Redemptions count on each voucher card to track campaign performance in real time.
- **Combine with the announcement bar** — Promote your voucher code in a site-wide announcement so customers see it before they start shopping.
