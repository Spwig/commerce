---
slug: voucher-codes
title_i18n_key: Voucher Codes
category: promotions
component: vouchers
keywords:
  - vouchers
  - coupons
  - discount codes
  - promo codes
  - coupon codes
  - gift cards
  - free shipping
  - percentage discount
  - fixed discount
url_patterns:
  - /admin/vouchers/vouchercode/
related:
  - sales-promotions
  - loyalty-program
published: true
---

Voucher Codes let you create discount codes, coupons, and gift cards that customers enter at checkout to receive a discount. Navigate to **Marketing > Vouchers** in the admin sidebar.

![Voucher list](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Voucher Dashboard

The voucher page shows an overview with:

- **Stats Cards** — Active, Inactive, Redemptions, and Total voucher counts
- **Filters** — Search by code or name, filter by Type, Status, and Scope
- **Voucher Cards** — Each voucher displayed with usage and status details

## Creating a Voucher

1. Click **+ Add Voucher** in the top right
2. Fill in the voucher details:
   - **Code** — The code customers enter at checkout (e.g., "SAVE20", "FREESHIP")
   - **Name/Description** — Internal description for your reference
   - **Discount Type** — Choose how the discount is applied
   - **Discount Value** — The amount or percentage off
3. Configure usage rules:
   - **Usage Limit** — Maximum total redemptions (0 = unlimited)
   - **Per-Customer Limit** — Maximum uses per customer
   - **Minimum Order Value** — Minimum cart total required
4. Set the **scope**:
   - **Entire Cart** — Discount applies to the whole order
   - **Specific Products** — Only applies to selected items
   - **Specific Categories** — Only applies to items in selected categories
5. Optionally set expiry:
   - **Expiry Date** — When the voucher stops working
6. Click **Save**

## Voucher Types

| Type | Description | Example |
|------|-------------|---------|
| **Fixed Amount** | Deducts a fixed dollar amount | $20 off the order |
| **Percentage** | Deducts a percentage of the total | 15% off the order |
| **Free Shipping** | Removes shipping charges | Free shipping on any order |

## Managing Vouchers

### Voucher Cards

Each voucher card shows:
- **Code** — The voucher code in bold
- **Description** — What the voucher does
- **Status badge** — Active or Inactive
- **Discount details** — Type and value (e.g., "$ 20.00" or "15.00%")
- **Scope** — Whether it applies to the entire cart or specific items
- **Usage count** — How many times the voucher has been redeemed
- **Created date** — When the voucher was created
- **Expiry** — Expiry date or "No expiry"

### Voucher Actions

Each card has action buttons:
- **Edit** — Modify the voucher settings
- **View History** — See redemption history
- **Delete** — Remove the voucher

### Filtering Vouchers

Use the filter bar to find specific vouchers:
- **Search** — Find by code, name, or description
- **Type** — Fixed Amount, Percentage, or Free Shipping
- **Status** — Active or Inactive
- **Scope** — Entire Cart or product-specific

## Bulk Voucher Generation

For large campaigns, you can generate vouchers in bulk:
1. The system auto-generates unique codes (e.g., "COUPONX1600406498")
2. Set common parameters for all generated vouchers
3. Distribute codes through email, social media, or print

## Customer Experience

When a customer has a voucher code:
1. They proceed to **checkout**
2. Enter the code in the **discount code** field
3. The discount is applied immediately if the voucher is valid
4. The order summary updates to show the discount

If a voucher is invalid (expired, usage limit reached, minimum not met), the customer sees a clear error message.

## Tips

- Use memorable codes for marketing campaigns (e.g., "SUMMER20" instead of random strings).
- Set per-customer limits to prevent abuse of valuable discounts.
- Use minimum order values to maintain profitability (e.g., "$10 off orders over $50").
- Monitor the Redemptions count on the dashboard to track campaign effectiveness.
- Create time-limited vouchers for urgency (e.g., "Valid this weekend only").
- Use the Active/Inactive status to pause vouchers without deleting them.
