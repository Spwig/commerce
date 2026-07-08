---
slug: voucher-restrictions
title_i18n_key: Voucher Restrictions
category: promotions
component: vouchers
keywords:
  - voucher restrictions
  - usage limit
  - per-customer limit
  - minimum order
  - discount cap
  - max discount
  - exclude sale items
  - combine vouchers
  - first-time customer
  - voucher abuse prevention
url_patterns:
  - /admin/vouchers/vouchercode/
related:
  - voucher-codes
  - voucher-examples
  - combining-discounts
published: true
---

Voucher restrictions control who can use a voucher, when, and how often. Configure these settings when creating or editing a voucher at **Marketing > Vouchers**.

![Restriction Rules](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Usage Limits

Set global and per-customer caps in the **Usage Limits** section of the voucher form.

- **Max uses total** — The maximum number of times this voucher can be redeemed across all customers. Leave empty for unlimited.
- **Max uses per customer** — How many times a single customer can use this voucher. Set to 1 for most campaigns.

| Pattern | Max Total | Per Customer | Use Case |
|---------|-----------|--------------|----------|
| Limited campaign | 100 | 1 | "First 100 customers" scarcity |
| Unlimited shared code | (empty) | 1 | Ongoing marketing code |
| Unlimited multi-use | (empty) | (empty) | Internal/staff discount |
| Single-use unique codes | 1 | 1 | Bulk-generated campaign codes |

## Minimum Order Value

The **Min order value** field protects your margins by requiring a cart total before the voucher applies. For example, "$10 off orders over $50" ensures you never discount a small order into unprofitability.

| Discount | Suggested Minimum | Ratio |
|----------|-------------------|-------|
| $5 off | $30+ | ~6:1 |
| $10 off | $50+ | ~5:1 |
| $20 off | $100+ | ~5:1 |
| 15% off | $40+ | Depends on catalog |

## Discount Cap (Max Discount Amount)

The **Max discount amount** field in **Discount Configuration** caps how much a percentage voucher can deduct. This only applies to percentage-type vouchers and prevents runaway discounts on high-value carts.

Example: "20% off, max $50 discount"
- $200 cart = $40 discount (20%)
- $300 cart = $50 discount (capped)
- $1,000 cart = still $50 discount (capped)

Add a discount cap on any percentage voucher you share publicly.

## Combination Rules

The **Restrictions & Rules** fieldset (click to expand) contains checkboxes that control how vouchers interact with other discounts.

| Setting | What It Does | When to Enable |
|---------|--------------|----------------|
| **Exclude sale items** | Voucher skips products already on sale | Most campaigns — protects sale margins |
| **Cannot combine with other vouchers** | Only one voucher per order | Default for most vouchers |
| **Cannot combine with sale items** | Blocks voucher if cart has ANY sale items | Strict campaigns where voucher replaces sale pricing |
| **First time customers only** | Only customers with zero previous orders | Welcome/acquisition campaigns |

## Customer Restrictions

For simple targeting, check **First time customers only** in the Restrictions & Rules fieldset.

For advanced targeting, use the **Voucher Restrictions** inline table at the bottom of the form. Click **+ Add another Voucher restriction** to add rows. Each restriction has three fields:

- **Type** — The restriction category (dropdown)
- **Value** — The matching value (comma-separated or JSON)
- **Is inclusive** — Checked = customer must match; unchecked = customer must NOT match

| Type | Value | Inclusive | Effect |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Yes | Only company employees can use it |
| shipping_country | US,CA | Yes | Only US and Canada customers |
| shipping_country | RU | No | Everyone EXCEPT Russia |
| day_of_week | monday,tuesday | Yes | Only valid on Mon and Tue |
| payment_method | stripe | Yes | Only for Stripe payments |

Combine multiple rows for layered restrictions. All inclusive restrictions must match, and no exclusive restrictions can match, for the voucher to apply.

## Expiry Strategies

Control when a voucher expires using the date and validity fields.

- **End date** — A hard cutoff date (e.g., Dec 31, 2026). The voucher stops working at midnight.
- **Days valid** — Rolling validity from the voucher's creation or first use. Overrides end date when set. Useful for welcome codes: "valid for 30 days after you receive it."

| Strategy | End Date | Days Valid | Use Case |
|----------|----------|------------|----------|
| Hard deadline | Set | (empty) | Seasonal campaigns, events |
| Rolling window | (empty) | 30 | Welcome codes, reward vouchers |
| No expiry | (empty) | (empty) | Ongoing codes, staff discounts |

## Preventing Abuse

Follow this checklist to keep your vouchers secure:

- Always set **Max uses per customer** to 1 unless there is a specific reason not to.
- Set **Min order value** on all fixed-amount vouchers.
- Add a **Max discount amount** on public percentage vouchers.
- Use hard-to-guess codes for high-value vouchers — avoid obvious codes like "DISCOUNT50".
- Monitor the usage analytics on each voucher card in the dashboard.
- Deactivate a voucher immediately if you see unusual redemption patterns.
- For high-value campaigns, use bulk-generated unique codes instead of a single shared code.

## Tips

- Start restrictive and loosen limits if redemption is too low — it is easier to relax rules than to tighten them after codes are in the wild.
- Test every voucher with a real checkout before distributing it to customers.
- Check the voucher analytics dashboard regularly to catch issues early.
- Combine multiple restrictions for layered protection — for example, per-customer limit + minimum order + discount cap + exclude sale items.
